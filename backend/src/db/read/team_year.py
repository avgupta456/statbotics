from typing import List, Optional

from sqlalchemy.orm.session import Session as SessionType
from sqlalchemy_cockroachdb import run_transaction  # type: ignore

from src.db.main import Session
from src.db.models.team_year import TeamYear, TeamYearORM
from src.db.read.main import common_filters


def get_team_year(team: int, year: int) -> Optional[TeamYear]:
    def callback(session: SessionType):
        data = session.query(TeamYearORM).filter(
            TeamYearORM.team == team, TeamYearORM.year == year
        )
        out_data: Optional[TeamYearORM] = data.first()
        if out_data is None:
            return None
        return TeamYear.from_dict(out_data.__dict__)

    return run_transaction(Session, callback)  # type: ignore


def get_team_years(
    team: Optional[int] = None,
    teams: Optional[List[str]] = None,
    year: Optional[int] = None,
    country: Optional[str] = None,
    state: Optional[str] = None,
    district: Optional[str] = None,
    metric: Optional[str] = None,
    ascending: Optional[bool] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> List[TeamYear]:
    @common_filters(TeamYearORM, TeamYear, metric, ascending, limit, offset)
    def callback(session: SessionType):
        data = session.query(TeamYearORM)
        if team is not None:
            data = data.filter(TeamYearORM.team == team)
        if teams is not None:
            data = data.filter(TeamYearORM.team.in_(teams))
        if year is not None:
            data = data.filter(TeamYearORM.year == year)
        if country is not None:
            data = data.filter(TeamYearORM.country == country)
        if state is not None:
            data = data.filter(TeamYearORM.state == state)
        if district is not None:
            data = data.filter(TeamYearORM.district == district)

        return data

    return run_transaction(Session, callback)  # type: ignore


def get_num_team_years() -> int:
    def callback(session: SessionType) -> int:
        return session.query(TeamYearORM).count()

    return run_transaction(Session, callback)  # type: ignore
