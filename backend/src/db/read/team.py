from typing import List, Optional

from sqlalchemy.orm.session import Session as SessionType
from sqlalchemy_cockroachdb import run_transaction  # type: ignore

from src.db.main import Session
from src.db.models.team import Team, TeamORM


def get_team(team: int) -> Optional[Team]:
    def callback(session: SessionType):
        out_data = session.query(TeamORM).filter(TeamORM.team == team).first()  # type: ignore
        return Team.from_dict(out_data.__dict__) if out_data else None

    return run_transaction(Session, callback)  # type: ignore


def get_teams(
    district: Optional[str] = None, state: Optional[str] = None
) -> List[Team]:
    def callback(session: SessionType):
        data = session.query(TeamORM)
        if district is not None:
            data = data.filter(TeamORM.district == district)  # type: ignore
        if state is not None:
            data = data.filter(TeamORM.state == state)  # type: ignore
        out_data: List[TeamORM] = data.all()
        return [Team.from_dict(x.__dict__) for x in out_data]

    return run_transaction(Session, callback)  # type: ignore


def get_num_teams() -> int:
    def callback(session: SessionType):
        return session.query(TeamORM).count()

    return run_transaction(Session, callback)  # type: ignore
