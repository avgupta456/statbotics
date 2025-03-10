from typing import List, Optional

from sqlalchemy import func
from sqlalchemy.future import select
from src.db.main import async_session
from src.db.models.team_year import TeamYear, TeamYearORM


async def get_team_year(team: int, year: int) -> Optional[TeamYear]:
    async with async_session() as session:
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
        filters = []

        if team is not None:
            filters.append(TeamYearORM.team == team)
        if teams:
            filters.append(TeamYearORM.team.in_(teams))
        if year is not None:
            filters.append(TeamYearORM.year == year)
        if country is not None:
            filters.append(TeamYearORM.country == country)
        if state is not None:
            filters.append(TeamYearORM.state == state)
        if district is not None:
            filters.append(TeamYearORM.district == district)

        query = select(TeamYearORM).filter(*filters)

        if metric and hasattr(TeamYearORM, metric):
            column = getattr(TeamYearORM, metric)
            query = query.order_by(column.asc() if ascending else column.desc())

        if limit is not None:
            query = query.limit(limit)
        if offset is not None:
            query = query.offset(offset)

        result = await session.execute(query)
        return [
            TeamYear.from_dict(team_year.__dict__) for team_year in result.scalars()
        ]


async def get_num_team_years() -> int:
    async with async_session() as session:
        result = await session.execute(select(func.count()).select_from(TeamYearORM))
        return result.scalar() or 0
