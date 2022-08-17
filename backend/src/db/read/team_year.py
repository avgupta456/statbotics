from typing import List, Optional

from sqlalchemy.orm.session import Session as SessionType
from sqlalchemy_cockroachdb import run_transaction

from src.db.main import Session
from src.db.models.team_year import TeamYear, TeamYearORM


def get_team_years(year: Optional[int] = None) -> List[TeamYear]:
    def callback(session: SessionType):
        data = session.query(TeamYearORM)
        if year is not None:
            data = data.filter(TeamYearORM.year == year)
        out_data: List[TeamYearORM] = data.all()
        return [TeamYear.from_dict(x.__dict__) for x in out_data]

    return run_transaction(Session, callback)


def get_num_team_years() -> int:
    def callback(session: SessionType):
        return session.query(TeamYearORM).count()

    return run_transaction(Session, callback)
