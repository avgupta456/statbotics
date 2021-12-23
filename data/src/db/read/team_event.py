from typing import List

from sqlalchemy.orm.session import Session as SessionType
from sqlalchemy_cockroachdb import run_transaction  # type: ignore

from db.main import Session
from db.models.team_event import TeamEvent, TeamEventORM


def get_team_events() -> List[TeamEvent]:
    def callback(session: SessionType):
        data = session.query(TeamEventORM).all()  # type: ignore
        return [TeamEvent.from_dict(x.__dict__) for x in data]

    return run_transaction(Session, callback)  # type: ignore


def get_num_team_events() -> int:
    def callback(session: SessionType):
        return session.query(TeamEventORM).count()  # type: ignore

    return run_transaction(Session, callback)  # type: ignore
