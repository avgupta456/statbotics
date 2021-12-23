from typing import List

from sqlalchemy.orm.session import Session as SessionType
from sqlalchemy_cockroachdb import run_transaction  # type: ignore

from db.main import Session
from db.models.team_match import TeamMatch, TeamMatchORM


def get_team_matches() -> List[TeamMatch]:
    def callback(session: SessionType):
        data = session.query(TeamMatchORM).all()  # type: ignore
        return [TeamMatch.from_dict(x.__dict__) for x in data]

    return run_transaction(Session, callback)  # type: ignore


def get_num_team_matches() -> int:
    def callback(session: SessionType):
        return session.query(TeamMatchORM).count()  # type: ignore

    return run_transaction(Session, callback)  # type: ignore
