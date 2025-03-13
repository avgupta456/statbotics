from typing import List, Optional

from sqlalchemy import func
from sqlalchemy.future import select
from src.db.main import async_session
from src.db.models.team import Team, TeamORM


async def get_team(team: int) -> Optional[Team]:
    async with async_session() as session:
        async with session.begin():
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
        query = select(TeamORM)

        if country is not None:
            query = query.filter(TeamORM.country == country)
        if state is not None:
            query = query.filter(TeamORM.state == state)
        if district is not None:
            query = query.filter(TeamORM.district == district)
        if active is not None:
            query = query.filter(TeamORM.active == active)

        if metric is not None:
            column = getattr(TeamORM, metric, None)
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

        return [Team.from_dict(team.__dict__) for team in data]


async def get_num_teams() -> int:
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(select(func.count()).select_from(TeamORM))
            return result.scalar() or 0
