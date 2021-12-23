from typing import List

from sqlalchemy.orm.session import Session as SessionType
from sqlalchemy_cockroachdb import run_transaction  # type: ignore

from db.main import Session
from db.models.match import Match, MatchORM


def get_matches() -> List[Match]:
    def callback(session: SessionType):
        data = session.query(MatchORM).all()  # type: ignore
        return [Match.from_dict(x.__dict__) for x in data]

    return run_transaction(Session, callback)  # type: ignore


def get_num_matches() -> int:
    def callback(session: SessionType):
        return session.query(MatchORM).count()  # type: ignore

    return run_transaction(Session, callback)  # type: ignore
