# type: ignore
from typing import Dict, List, Optional

from sqlalchemy import asc, desc, func
from sqlalchemy.orm import Session as SessionType
from sqlalchemy_cockroachdb import run_transaction

from src.db.main import Session
from src.db.models.event import EventORM
from src.db.models.match import Match, MatchORM


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
            & (MatchORM.offseason == False)  # noqa: E712
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

        high_score_matches = (
            matches.add_columns(
                func.greatest(MatchORM.red_no_fouls, MatchORM.blue_no_fouls).label(
                    "max_score"
                ),
            )
            .order_by(desc("max_score"), asc("time"))
            .limit(10)
            .all()
        )

        combined_score_matches = (
            matches.add_columns(
                (MatchORM.red_no_fouls + MatchORM.blue_no_fouls).label("sum_score")
            )
            .order_by(desc("sum_score"), asc("time"))
            .limit(10)
            .all()
        )

        high_losing_scores = (
            matches.filter((MatchORM.red_score != MatchORM.blue_score))
            .add_columns(
                func.least(MatchORM.red_score, MatchORM.blue_score).label(
                    "losing_score"
                ),
            )
            .order_by(desc("losing_score"), asc("time"))
            .limit(10)
            .all()
        )

        return {
            "high_score": [
                Match.from_dict(match.__dict__) for (match, *args) in high_score_matches
            ],
            "combined_score": [
                Match.from_dict(match.__dict__)
                for (match, *args) in combined_score_matches
            ],
            "losing_score": [
                Match.from_dict(match.__dict__) for (match, *args) in high_losing_scores
            ],
        }

    return run_transaction(Session, callback)
