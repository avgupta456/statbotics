from typing import List, Optional

from sqlalchemy.orm.session import Session as SessionType  # type: ignore
from sqlalchemy_cockroachdb import run_transaction  # type: ignore

from src.db.main import Session
from src.db.models.team_year import TeamYear, TeamYearORM


def get_team_year(team: int, year: int) -> Optional[TeamYear]:
    def callback(session: SessionType):
        data = session.query(TeamYearORM).filter(  # type: ignore
            TeamYearORM.team == team, TeamYearORM.year == year
        )
        out_data: Optional[TeamYearORM] = data.first()  # type: ignore
        if out_data is None:
            return None
        return TeamYear.from_dict(out_data.__dict__)  # type: ignore

    return run_transaction(Session, callback)  # type: ignore


def get_team_years(
    team: Optional[int] = None,
    teams: Optional[List[int]] = None,
    year: Optional[int] = None,
    country: Optional[str] = None,
    district: Optional[str] = None,
    state: Optional[str] = None,
    offseason: Optional[bool] = False,
    metric: Optional[str] = None,
    ascending: Optional[bool] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> List[TeamYear]:
    def callback(session: SessionType):
        data = session.query(TeamYearORM)  # type: ignore
        if team is not None:
            data = data.filter(TeamYearORM.team == team)  # type: ignore
        if teams is not None:
            data = data.filter(TeamYearORM.team.in_(teams))  # type: ignore
        if year is not None:
            data = data.filter(TeamYearORM.year == year)  # type: ignore
        if country is not None:
            data = data.filter(TeamYearORM.country == country)  # type: ignore
        if district is not None:
            data = data.filter(TeamYearORM.district == district)  # type: ignore
        if state is not None:
            data = data.filter(TeamYearORM.state == state)  # type: ignore
        if offseason is not None:
            data = data.filter(TeamYearORM.offseason == offseason)  # type: ignore
        if metric is not None:
            data = data.filter(TeamYearORM.__dict__[metric] != None)  # type: ignore  # noqa: E711
            if ascending is not None and ascending:
                data = data.order_by(TeamYearORM.__dict__[metric].asc())  # type: ignore
            else:
                data = data.order_by(TeamYearORM.__dict__[metric].desc())  # type: ignore
        if limit is not None:
            data = data.limit(limit)  # type: ignore
        if offset is not None:
            data = data.offset(offset)  # type: ignore
        out_data: List[TeamYearORM] = data.all()  # type: ignore
        return [TeamYear.from_dict(x.__dict__) for x in out_data]  # type: ignore

    return run_transaction(Session, callback)  # type: ignore


def get_num_team_years() -> int:
    def callback(session: SessionType) -> int:
        return session.query(TeamYearORM).count()  # type: ignore

    return run_transaction(Session, callback)  # type: ignore
