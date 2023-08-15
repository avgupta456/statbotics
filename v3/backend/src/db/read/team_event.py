from typing import List, Optional

from sqlalchemy.orm.session import Session as SessionType  # type: ignore
from sqlalchemy_cockroachdb import run_transaction  # type: ignore

from src.db.main import Session
from src.db.models.team_event import TeamEvent, TeamEventORM


def get_team_event(team: int, event: str) -> Optional[TeamEvent]:
    def callback(session: SessionType):
        data = session.query(TeamEventORM).filter(  # type: ignore
            TeamEventORM.team == team, TeamEventORM.event == event
        )
        out_data: Optional[TeamEventORM] = data.first()  # type: ignore
        if out_data is None:
            return None
        return TeamEvent.from_dict(out_data.__dict__)  # type: ignore

    return run_transaction(Session, callback)  # type: ignore


def get_team_events(
    team: Optional[int] = None,
    year: Optional[int] = None,
    event: Optional[str] = None,
    country: Optional[str] = None,
    district: Optional[str] = None,
    state: Optional[str] = None,
    type: Optional[int] = None,
    week: Optional[int] = None,
    offseason: Optional[bool] = False,
    metric: Optional[str] = None,
    ascending: Optional[bool] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> List[TeamEvent]:
    def callback(session: SessionType):
        data = session.query(TeamEventORM)  # type: ignore
        if team is not None:
            data = data.filter(TeamEventORM.team == team)  # type: ignore
        if year is not None:
            data = data.filter(TeamEventORM.year == year)  # type: ignore
        if event is not None:
            data = data.filter(TeamEventORM.event == event)  # type: ignore
        if country is not None:
            data = data.filter(TeamEventORM.country == country)  # type: ignore
        if district is not None:
            data = data.filter(TeamEventORM.district == district)  # type: ignore
        if state is not None:
            data = data.filter(TeamEventORM.state == state)  # type: ignore
        if type is not None:
            data = data.filter(TeamEventORM.type == type)  # type: ignore
        if week is not None:
            data = data.filter(TeamEventORM.week == week)  # type: ignore
        if offseason is not None:
            data = data.filter(TeamEventORM.offseason == offseason)  # type: ignore
        if metric is not None:
            data = data.filter(TeamEventORM.__dict__[metric] != None)  # type: ignore  # noqa: E711
            if ascending is not None and ascending:
                data = data.order_by(TeamEventORM.__dict__[metric].asc())  # type: ignore
            else:
                data = data.order_by(TeamEventORM.__dict__[metric].desc())  # type: ignore
        if limit is not None:
            data = data.limit(limit)  # type: ignore
        if offset is not None:
            data = data.offset(offset)  # type: ignore
        out_data: List[TeamEventORM] = data.all()  # type: ignore
        return [TeamEvent.from_dict(x.__dict__) for x in out_data]  # type: ignore

    return run_transaction(Session, callback)  # type: ignore


def get_num_team_events() -> int:
    def callback(session: SessionType) -> int:
        return session.query(TeamEventORM).count()  # type: ignore

    return run_transaction(Session, callback)  # type: ignore
