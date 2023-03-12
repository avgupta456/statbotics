from datetime import datetime
from typing import List, Tuple

from sqlalchemy.orm import Session as SessionType
from sqlalchemy_cockroachdb import run_transaction  # type: ignore

from src.constants import CURR_YEAR
from src.db.main import Session
from src.db.models.event import EventORM
from src.db.models.match import MatchORM, Match


def get_upcoming_matches() -> List[Tuple[Match, str]]:
    curr_timestamp = int(datetime.now().timestamp())

    def callback(session: SessionType):
        matches = (
            session.query(MatchORM, EventORM.name)  # type: ignore
            .filter(
                (MatchORM.year == CURR_YEAR)  # type: ignore
                & (MatchORM.status == "Upcoming")
                & (MatchORM.predicted_time > curr_timestamp)
                & (MatchORM.event == EventORM.key)  # type: ignore
            )
            .limit(100)
            .all()
        )

        return [
            (Match.from_dict(match.__dict__), event_name)
            for (match, event_name) in matches
        ]

    return run_transaction(Session, callback)  # type: ignore
