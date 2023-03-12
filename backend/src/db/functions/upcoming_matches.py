from datetime import datetime
from typing import List

from sqlalchemy.orm import Session as SessionType
from sqlalchemy_cockroachdb import run_transaction  # type: ignore

from src.constants import CURR_YEAR
from src.db.main import Session
from src.db.models.match import MatchORM, Match


def get_upcoming_matches() -> List[Match]:
    curr_timestamp = int(datetime.now().timestamp())

    def callback(session: SessionType):
        matches = (
            session.query(MatchORM)  # type: ignore
            .filter(
                (MatchORM.year == CURR_YEAR)  # type: ignore
                & (MatchORM.status == "Upcoming")
                & (MatchORM.predicted_time > curr_timestamp)
            )
            .limit(100)
            .all()
        )

        return [Match.from_dict(x.__dict__) for x in matches]

    return run_transaction(Session, callback)  # type: ignore
