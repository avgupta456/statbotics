from typing import List, Optional

from sqlalchemy.orm.session import Session as SessionType  # type: ignore
from sqlalchemy_cockroachdb import run_transaction  # type: ignore

from src.db.main import Session
from src.db.models.team import Team, TeamORM


def get_team(team: int) -> Optional[Team]:
    def callback(session: SessionType):
        out_data = session.query(TeamORM).filter(TeamORM.team == team).first()  # type: ignore
        return Team.from_dict(out_data.__dict__) if out_data else None  # type: ignore

    return run_transaction(Session, callback)  # type: ignore


def get_teams(
    country: Optional[str] = None,
    district: Optional[str] = None,
    state: Optional[str] = None,
    active: Optional[bool] = None,
    offseason: Optional[bool] = False,
    metric: Optional[str] = None,
    ascending: Optional[bool] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> List[Team]:
    def callback(session: SessionType):
        data = session.query(TeamORM)  # type: ignore
        if country is not None:
            data = data.filter(TeamORM.country == country)  # type: ignore
        if district is not None:
            data = data.filter(TeamORM.district == district)  # type: ignore
        if state is not None:
            data = data.filter(TeamORM.state == state)  # type: ignore
        if active is not None:
            data = data.filter(TeamORM.active == active)  # type: ignore
        if offseason is not None:
            data = data.filter(TeamORM.offseason == offseason)  # type: ignore
        if metric is not None:
            data = data.filter(TeamORM.__dict__[metric] != None)  # type: ignore  # noqa: E711
            if ascending is not None and ascending:
                data = data.order_by(TeamORM.__dict__[metric].asc())  # type: ignore
            else:
                data = data.order_by(TeamORM.__dict__[metric].desc())  # type: ignore
        if limit is not None:
            data = data.limit(limit)  # type: ignore
        if offset is not None:
            data = data.offset(offset)  # type: ignore

        out_data: List[TeamORM] = data.all()  # type: ignore
        return [Team.from_dict(x.__dict__) for x in out_data]  # type: ignore

    return run_transaction(Session, callback)  # type: ignore


def get_num_teams() -> int:
    def callback(session: SessionType) -> int:
        return session.query(TeamORM).count()  # type: ignore

    return run_transaction(Session, callback)  # type: ignore
