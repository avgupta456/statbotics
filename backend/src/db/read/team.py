from typing import List

from sqlalchemy.orm.session import Session as SessionType
from sqlalchemy_cockroachdb import run_transaction  # type: ignore

from src.db.main import Session
from src.db.models.team import Team, TeamORM


def get_teams() -> List[Team]:
    def callback(session: SessionType):
        out_data = session.query(TeamORM).all()
        return [Team.from_dict(x.__dict__) for x in out_data]

    return run_transaction(Session, callback)  # type: ignore


def get_num_teams() -> int:
    def callback(session: SessionType):
        return session.query(TeamORM).count()

    return run_transaction(Session, callback)  # type: ignore
