# type: ignore
from typing import Dict, List, Optional

from sqlalchemy import desc, func
from sqlalchemy.orm import Session as SessionType
from sqlalchemy_cockroachdb import run_transaction

from src.db.main import Session
from src.db.models.match import MatchORM, Match
from src.db.models.event import EventORM


def get_noteworthy_matches(
    year: int,
    country: Optional[str],
    state: Optional[str],
    district: Optional[str],
    playoff: Optional[bool],
    week: Optional[int],
) -> Dict[str, List[Match]]:
    def callback(session: SessionType):
        matches = session.query(
            MatchORM,
            EventORM.country,
            EventORM.state,
            EventORM.district,
            EventORM.week,
        ).filter(
            (MatchORM.year == year)
            & (MatchORM.status == "Completed")
            & (MatchORM.offseason is False)
            & (MatchORM.event == EventORM.key)
        )

        if country is not None:
            matches = matches.filter(EventORM.country == country)

        if state is not None:
            matches = matches.filter(EventORM.state == state)

        if district is not None:
            matches = matches.filter(EventORM.district == district)

        if playoff is not None:
            matches = matches.filter(MatchORM.playoff == playoff)

        if week is not None:
            matches = matches.filter(EventORM.week == week)

        high_epa_matches = (
            matches.add_columns(
                func.greatest(MatchORM.red_epa_sum, MatchORM.blue_epa_sum).label(
                    "max_epa"
                ),
            )
            .order_by(desc("max_epa"))
            .limit(10)
            .all()
        )

        high_score_matches = (
            matches.add_columns(
                func.greatest(MatchORM.red_no_fouls, MatchORM.blue_no_fouls).label(
                    "max_score"
                ),
            )
            .order_by(desc("max_score"))
            .limit(10)
            .all()
        )

        return {
            "high_epa": [
                Match.from_dict(match.__dict__) for (match, *args) in high_epa_matches
            ],
            "high_score": [
                Match.from_dict(match.__dict__) for (match, *args) in high_score_matches
            ],
        }

    return run_transaction(Session, callback)
