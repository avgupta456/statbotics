from typing import List, Optional

from sqlalchemy import func
from sqlalchemy.future import select
from src.db.main import async_session
from src.db.models.team import Team, TeamORM


async def get_team(team: int) -> Optional[Team]:
    async with async_session() as session:
        result = await session.execute(select(TeamORM).where(TeamORM.team == team))
        data = result.scalars().first()
        if data is None:
            return None

        return Team.from_dict(data.__dict__)


async def get_teams(
    country: Optional[str] = None,
    state: Optional[str] = None,
    district: Optional[str] = None,
    active: Optional[bool] = None,
    metric: Optional[str] = None,
    ascending: Optional[bool] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> List[Team]:
    async with async_session() as session:
        filters = []

        if country is not None:
            filters.append(TeamORM.country == country)
        if state is not None:
            filters.append(TeamORM.state == state)
        if district is not None:
            filters.append(TeamORM.district == district)
        if active is not None:
            filters.append(TeamORM.active == active)

        query = select(TeamORM).filter(*filters)

        if metric and hasattr(TeamORM, metric):
            column = getattr(TeamORM, metric)
            query = query.order_by(column.asc() if ascending else column.desc())

        if limit is not None:
            query = query.limit(limit)
        if offset is not None:
            query = query.offset(offset)

        result = await session.execute(query)
        return [Team.from_dict(team.__dict__) for team in result.scalars()]


async def get_num_teams() -> int:
    async with async_session() as session:
        result = await session.execute(select(func.count()).select_from(TeamORM))
        return result.scalar() or 0
