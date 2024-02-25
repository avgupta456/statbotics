from datetime import datetime
from typing import List, Optional, Tuple

from sqlalchemy import func, text
from sqlalchemy.orm import Session as SessionType
from sqlalchemy_cockroachdb import run_transaction  # type: ignore

from src.constants import CURR_YEAR
from src.db.main import Session
from src.db.models.event import EventORM
from src.db.models.match import Match, MatchORM
from src.types.enums import EventStatus


def get_upcoming_matches(
    country: Optional[str],
    state: Optional[str],
    district: Optional[str],
    elim: Optional[bool],
    minutes: int,
    limit: int,
    metric: str,
) -> List[Tuple[Match, str]]:
    curr_timestamp = int(datetime.now().timestamp()) - 60 * 5  # 5 minutes

    if minutes == -1:
        minutes = 60 * 24 * 7  # 1 week

    def callback(session: SessionType):
        matches = session.query(
            MatchORM,
            EventORM.name,
            EventORM.country,
            EventORM.state,
            EventORM.district,
        ).add_columns(
            func.greatest(MatchORM.epa_red_score_pred, MatchORM.epa_blue_score_pred).label("max_epa"),  # type: ignore
            (MatchORM.epa_red_score_pred + MatchORM.epa_blue_score_pred).label("sum_epa"),  # type: ignore
            func.abs(MatchORM.epa_red_score_pred - MatchORM.epa_blue_score_pred).label("diff_epa"),  # type: ignore
        )

        matches = matches.filter(
            (MatchORM.year == CURR_YEAR)
            & (MatchORM.status == EventStatus.UPCOMING)
            & (MatchORM.predicted_time > curr_timestamp)
            & (MatchORM.predicted_time < curr_timestamp + 60 * minutes)
            & (MatchORM.event == EventORM.key)
        )

        if country is not None:
            matches = matches.filter(EventORM.country == country)

        if state is not None:
            matches = matches.filter(EventORM.state == state)

        if district == "regionals":
            matches = matches.filter(EventORM.district.is_(None))
        elif district is not None:
            matches = matches.filter(EventORM.district == district)

        if elim is not None:
            matches = matches.filter(MatchORM.elim == elim)

        if metric in ["max_epa", "sum_epa"]:
            # sort desc
            matches = matches.order_by(text(f"{metric} DESC"))
        elif metric in ["time", "diff_epa"]:
            # sort asc
            matches = matches.order_by(text(f"{metric} ASC"))

        matches = matches.limit(limit).all()

        return [
            (Match.from_dict(match.__dict__), event_name)
            for (match, event_name, *_args) in matches
        ]

    return run_transaction(Session, callback)  # type: ignore
