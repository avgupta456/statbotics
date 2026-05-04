from typing import Dict, List, Optional

from sqlalchemy import asc, desc, func
from sqlalchemy.orm import Session as SessionType
from sqlalchemy_cockroachdb import run_transaction  # type: ignore

from src.db.main import Session
from src.db.models.event import EventORM
from src.db.models.match import Match, MatchORM
from src.types.enums import MatchStatus


def get_noteworthy_matches(
    year: int,
    country: Optional[str],
    state: Optional[str],
    district: Optional[str],
    elim: Optional[bool],
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
            & (MatchORM.status == MatchStatus.COMPLETED)
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

        if week is not None:
            matches = matches.filter(EventORM.week == week)

        red_score_col = MatchORM.red_score if year < 2016 else MatchORM.red_no_foul
        blue_score_col = MatchORM.blue_score if year < 2016 else MatchORM.blue_no_foul

        high_score_matches = (
            matches.add_columns(
                func.greatest(red_score_col, blue_score_col).label("max_score")
            )
            .order_by(desc("max_score"), asc(MatchORM.time))  # type: ignore
            .limit(30)
            .all()
        )

        combined_score_matches = (
            matches.add_columns((red_score_col + blue_score_col).label("sum_score"))  # type: ignore
            .order_by(desc("sum_score"), asc(MatchORM.time))  # type: ignore
            .limit(30)
            .all()
        )

        high_losing_scores = (
            matches.add_columns(
                func.least(MatchORM.red_score, MatchORM.blue_score).label(
                    "losing_score"
                ),
            )
            .order_by(desc("losing_score"), asc(MatchORM.time))  # type: ignore
            .limit(30)
            .all()
        )

        extra = {}
        if year >= 2016:
            high_auto_score_matches = (
                matches.add_columns(
                    func.greatest(MatchORM.red_auto, MatchORM.blue_auto).label(
                        "max_auto_score"
                    )
                )
                .order_by(desc("max_auto_score"), asc("time"))  # type: ignore
                .limit(30)
                .all()
            )

            high_teleop_score_matches = (
                matches.add_columns(
                    func.greatest(MatchORM.red_teleop, MatchORM.blue_teleop).label(
                        "max_teleop_score"
                    )
                )
                .order_by(desc("max_teleop_score"), asc("time"))  # type: ignore
                .limit(30)
                .all()
            )

            high_endgame_score_matches = (
                matches.add_columns(
                    func.greatest(MatchORM.red_endgame, MatchORM.blue_endgame).label(
                        "max_endgame_score"
                    )
                )
                .order_by(desc("max_endgame_score"), asc("time"))  # type: ignore
                .limit(30)
                .all()
            )

            extra = {
                "high_auto_score": [
                    Match.from_dict(match.__dict__)
                    for (match, *_args) in high_auto_score_matches
                ],
                "high_teleop_score": [
                    Match.from_dict(match.__dict__)
                    for (match, *_args) in high_teleop_score_matches
                ],
                "high_endgame_score": [
                    Match.from_dict(match.__dict__)
                    for (match, *_args) in high_endgame_score_matches
                ],
            }

        return {
            "high_score": [
                Match.from_dict(match.__dict__)
                for (match, *_args) in high_score_matches
            ],
            "combined_score": [
                Match.from_dict(match.__dict__)
                for (match, *_args) in combined_score_matches
            ],
            "losing_score": [
                Match.from_dict(match.__dict__)
                for (match, *_args) in high_losing_scores
            ],
            **extra,
        }

    return run_transaction(Session, callback)  # type: ignore
