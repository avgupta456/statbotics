from typing import List, Optional

from sqlalchemy import func
from sqlalchemy.future import select
from src.db.main import async_session
from src.db.models.team_year import TeamYear, TeamYearORM


async def get_team_year(team: int, year: int) -> Optional[TeamYear]:
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(
                select(TeamYearORM).where(
                    TeamYearORM.team == team, TeamYearORM.year == year
                )
            )
            data = result.scalars().first()
            if data is None:
                return None

            return TeamYear.from_dict(data.__dict__)


async def get_team_years(
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
    async with async_session() as session:
        query = select(TeamYearORM)

        if team is not None:
            query = query.filter(TeamYearORM.team == team)
        if teams is not None:
            query = query.filter(TeamYearORM.team.in_(teams))
        if year is not None:
            query = query.filter(TeamYearORM.year == year)
        if country is not None:
            query = query.filter(TeamYearORM.country == country)
        if state is not None:
            query = query.filter(TeamYearORM.state == state)
        if district is not None:
            query = query.filter(TeamYearORM.district == district)

        if metric is not None:
            column = getattr(TeamYear, metric, None)
            if column:
                if ascending:
                    query = query.order_by(column.asc())
                else:
                    query = query.order_by(column.desc())

        if limit is not None:
            query = query.limit(limit)
        if offset is not None:
            query = query.offset(offset)

        result = await session.execute(query)
        data = result.scalars().all()

        return [TeamYear.from_dict(team_year.__dict__) for team_year in data]


async def get_num_team_years() -> int:
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(
                select(func.count()).select_from(TeamYearORM)
            )
            return result.scalar() or 0
