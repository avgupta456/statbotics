from typing import List, Optional

from sqlalchemy.orm.session import Session as SessionType
from sqlalchemy_cockroachdb import run_transaction  # type: ignore

from src.db.main import Session
from src.db.models.team_event import TeamEvent, TeamEventORM


def get_team_events(
    year: Optional[int] = None,
    event: Optional[int] = None,
    team: Optional[int] = None,
) -> List[TeamEvent]:
    def callback(session: SessionType):
        data = session.query(TeamEventORM)
        if year is not None:
            data = data.filter(TeamEventORM.year == year)  # type: ignore
        if event is not None:
            data = data.filter(TeamEventORM.event == event)  # type: ignore
        if team is not None:
            data = data.filter(TeamEventORM.team == team)  # type: ignore
        out_data: List[TeamEventORM] = data.all()
        return [TeamEvent.from_dict(x.__dict__) for x in out_data]

    return run_transaction(Session, callback)  # type: ignore


def get_num_team_events() -> int:
    def callback(session: SessionType):
        return session.query(TeamEventORM).count()

    return run_transaction(Session, callback)  # type: ignore
