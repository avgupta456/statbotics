from typing import List, Optional

from sqlalchemy.orm.session import Session as SessionType  # type: ignore
from sqlalchemy_cockroachdb import run_transaction  # type: ignore

from src.db.main import Session
from src.db.models.team import Team, TeamORM
from src.db.read.main import common_filters


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
    @common_filters(TeamORM, Team, metric, ascending, limit, offset)
    def callback(session: SessionType):  # type: ignore
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

        return data  # type: ignore

    return run_transaction(Session, callback)  # type: ignore


def get_num_teams() -> int:
    def callback(session: SessionType) -> int:
        return session.query(TeamORM).count()  # type: ignore

    return run_transaction(Session, callback)  # type: ignore
