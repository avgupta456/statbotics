from typing import List

from sqlalchemy.orm.session import Session as SessionType
from sqlalchemy_cockroachdb import run_transaction  # type: ignore

from db.main import Session
from db.models.team import Team, TeamORM


def get_teams() -> List[Team]:
    def callback(session: SessionType):
        data = session.query(TeamORM).all()  # type: ignore
        return [Team.from_dict(x.__dict__) for x in data]

    return run_transaction(Session, callback)  # type: ignore


def get_num_teams() -> int:
    def callback(session: SessionType):
        return session.query(TeamORM).count()  # type: ignore

    return run_transaction(Session, callback)  # type: ignore
