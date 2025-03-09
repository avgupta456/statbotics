from datetime import datetime
from typing import List, Optional, Tuple

from sqlalchemy import func, text
from sqlalchemy.future import select

from src.constants import CURR_YEAR
from src.db.main import async_session
from src.db.models.event import EventORM
from src.db.models.match import Match, MatchORM
from src.types.enums import EventStatus


async def get_upcoming_matches(
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

    async with async_session() as session:
        async with session.begin():
            stmt = (
                select(
                    MatchORM,
                    EventORM.name,
                    EventORM.country,
                    EventORM.state,
                    EventORM.district,
                )
                .add_columns(
                    func.greatest(
                        MatchORM.epa_red_score_pred, MatchORM.epa_blue_score_pred
                    ).label("max_epa"),
                    (MatchORM.epa_red_score_pred + MatchORM.epa_blue_score_pred).label(
                        "sum_epa"
                    ),
                    func.abs(
                        MatchORM.epa_red_score_pred - MatchORM.epa_blue_score_pred
                    ).label("diff_epa"),
                )
                .join(EventORM, MatchORM.event == EventORM.key)
                .filter(
                    (MatchORM.year == CURR_YEAR)
                    & (MatchORM.status == EventStatus.UPCOMING)
                    & (MatchORM.predicted_time > curr_timestamp)
                    & (MatchORM.predicted_time < curr_timestamp + 60 * minutes)
                )
            )

            if country is not None:
                stmt = stmt.filter(EventORM.country == country)

            if state is not None:
                stmt = stmt.filter(EventORM.state == state)

            if district == "regionals":
                stmt = stmt.filter(EventORM.district.is_(None))
            elif district is not None:
                stmt = stmt.filter(EventORM.district == district)

            if elim is not None:
                stmt = stmt.filter(MatchORM.elim == elim)

            if metric in ["max_epa", "sum_epa"]:
                stmt = stmt.order_by(text(f"{metric} DESC"))
            elif metric in ["time", "diff_epa"]:
                stmt = stmt.order_by(text(f"{metric} ASC"))

            stmt = stmt.limit(limit)

            result = await session.execute(stmt)
            matches = result.all()

            return [
                (Match.from_dict(match.__dict__), event_name)
                for match, event_name, *_args in matches
            ]
