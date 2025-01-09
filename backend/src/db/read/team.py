from typing import List, Optional

from sqlalchemy.orm.session import Session as SessionType
from sqlalchemy_cockroachdb import run_transaction  # type: ignore

from src.db.main import Session
from src.db.models.team import Team, TeamORM
from src.db.read.main import common_filters


def get_team(team: int) -> Optional[Team]:
    def callback(session: SessionType):
        out_data = session.query(TeamORM).filter(TeamORM.team == team).first()
        return Team.from_dict(out_data.__dict__) if out_data else None

    return run_transaction(Session, callback)  # type: ignore


def get_teams(
    country: Optional[str] = None,
    state: Optional[str] = None,
    district: Optional[str] = None,
    active: Optional[bool] = None,
    metric: Optional[str] = None,
    ascending: Optional[bool] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> List[Team]:
    @common_filters(TeamORM, Team, metric, ascending, limit, offset)
    def callback(session: SessionType):
        data = session.query(TeamORM)
        if country is not None:
            data = data.filter(TeamORM.country == country)
        if state is not None:
            data = data.filter(TeamORM.state == state)
        if district is not None:
            data = data.filter(TeamORM.district == district)
        if active is not None:
            data = data.filter(TeamORM.active == active)

        return data

    return run_transaction(Session, callback)  # type: ignore


def get_num_teams() -> int:
    def callback(session: SessionType) -> int:
        return session.query(TeamORM).count()

    return run_transaction(Session, callback)  # type: ignore
