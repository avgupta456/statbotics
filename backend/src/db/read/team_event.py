from typing import List, Optional

from sqlalchemy.orm.session import Session as SessionType
from sqlalchemy_cockroachdb import run_transaction  # type: ignore

from src.db.main import Session
from src.db.models.team_event import TeamEvent, TeamEventORM
from src.db.read.main import common_filters


def get_team_event(team: int, event: str) -> Optional[TeamEvent]:
    def callback(session: SessionType):
        data = session.query(TeamEventORM).filter(
            TeamEventORM.team == team, TeamEventORM.event == event
        )
        out_data: Optional[TeamEventORM] = data.first()
        if out_data is None:
            return None
        return TeamEvent.from_dict(out_data.__dict__)

    return run_transaction(Session, callback)  # type: ignore


def get_team_events(
    team: Optional[int] = None,
    year: Optional[int] = None,
    event: Optional[str] = None,
    country: Optional[str] = None,
    state: Optional[str] = None,
    district: Optional[str] = None,
    type: Optional[str] = None,
    week: Optional[int] = None,
    metric: Optional[str] = None,
    ascending: Optional[bool] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> List[TeamEvent]:
    @common_filters(TeamEventORM, TeamEvent, metric, ascending, limit, offset)
    def callback(session: SessionType):
        data = session.query(TeamEventORM)
        if team is not None:
            data = data.filter(TeamEventORM.team == team)
        if year is not None:
            data = data.filter(TeamEventORM.year == year)
        if event is not None:
            data = data.filter(TeamEventORM.event == event)
        if country is not None:
            data = data.filter(TeamEventORM.country == country)
        if state is not None:
            data = data.filter(TeamEventORM.state == state)
        if district is not None:
            data = data.filter(TeamEventORM.district == district)
        if type is not None:
            data = data.filter(TeamEventORM.type == type)
        if week is not None:
            data = data.filter(TeamEventORM.week == week)

        return data

    return run_transaction(Session, callback)  # type: ignore


def get_num_team_events() -> int:
    def callback(session: SessionType) -> int:
        return session.query(TeamEventORM).count()

    return run_transaction(Session, callback)  # type: ignore
