from typing import List, Optional

from sqlalchemy.orm.session import Session as SessionType
from sqlalchemy_cockroachdb import run_transaction  # type: ignore

from src.db.main import Session
from src.db.models.team_event import TeamEvent, TeamEventORM


def get_team_event(team: int, event: str) -> Optional[TeamEvent]:
    def callback(session: SessionType):
        data = session.query(TeamEventORM).filter(  # type: ignore
            TeamEventORM.team == team, TeamEventORM.event == event
        )
        out_data: Optional[TeamEventORM] = data.first()
        if out_data is None:
            return None
        return TeamEvent.from_dict(out_data.__dict__)

    return run_transaction(Session, callback)  # type: ignore


def get_team_events(
    year: Optional[int] = None,
    event: Optional[int] = None,
    team: Optional[int] = None,
    district: Optional[str] = None,
    state: Optional[str] = None,
) -> List[TeamEvent]:
    def callback(session: SessionType):
        data = session.query(TeamEventORM)
        if year is not None:
            data = data.filter(TeamEventORM.year == year)  # type: ignore
        if event is not None:
            data = data.filter(TeamEventORM.event == event)  # type: ignore
        if team is not None:
            data = data.filter(TeamEventORM.team == team)  # type: ignore
        if district is not None:
            data = data.filter(TeamEventORM.district == district)  # type: ignore
        if state is not None:
            data = data.filter(TeamEventORM.state == state)  # type: ignore
        out_data: List[TeamEventORM] = data.all()
        return [TeamEvent.from_dict(x.__dict__) for x in out_data]

    return run_transaction(Session, callback)  # type: ignore


def get_num_team_events() -> int:
    def callback(session: SessionType):
        return session.query(TeamEventORM).count()

    return run_transaction(Session, callback)  # type: ignore
