from typing import List, Optional

from sqlalchemy.orm.session import Session as SessionType
from sqlalchemy_cockroachdb import run_transaction  # type: ignore

from db.main import Session
from db.models.team_year import TeamYear, TeamYearORM


def get_team_years(year: Optional[int] = None) -> List[TeamYear]:
    def callback(session: SessionType):
        if year == None:
            data = session.query(TeamYearORM).all()  # type: ignore
        else:
            data = session.query(TeamYearORM).filter(TeamYearORM.year_id == year).all()  # type: ignore
        return [TeamYear.from_dict(x.__dict__) for x in data]

    return run_transaction(Session, callback)  # type: ignore


def get_num_team_years() -> int:
    def callback(session: SessionType):
        return session.query(TeamYearORM).count()  # type: ignore

    return run_transaction(Session, callback)  # type: ignore
