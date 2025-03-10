from typing import List, Optional

from sqlalchemy import func
from sqlalchemy.future import select
from src.db.main import async_session
from src.db.models.team_event import TeamEvent, TeamEventORM


async def get_team_event(team: int, event: str) -> Optional[TeamEvent]:
    async with async_session() as session:
        result = await session.execute(
            select(TeamEventORM).where(
                TeamEventORM.team == team, TeamEventORM.event == event
            )
        )
        data = result.scalars().first()
        if data is None:
            return None

        return TeamEvent.from_dict(data.__dict__)


async def get_team_events(
    team: Optional[int] = None,
    year: Optional[int] = None,
    event: Optional[str] = None,
    country: Optional[str] = None,
    state: Optional[str] = None,
    district: Optional[str] = None,
    type: Optional[str] = None,
    week: Optional[int] = None,
    metric: Optional[str] = None,
    ascending: Optional[bool] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> List[TeamEvent]:
    async with async_session() as session:
        filters = []

        if team is not None:
            filters.append(TeamEventORM.team == team)
        if year is not None:
            filters.append(TeamEventORM.year == year)
        if event is not None:
            filters.append(TeamEventORM.event == event)
        if country is not None:
            filters.append(TeamEventORM.country == country)
        if state is not None:
            filters.append(TeamEventORM.state == state)
        if district is not None:
            filters.append(TeamEventORM.district == district)
        if type is not None:
            filters.append(TeamEventORM.type == type)
        if week is not None:
            filters.append(TeamEventORM.week == week)

        query = select(TeamEventORM).filter(*filters)

        if metric and hasattr(TeamEventORM, metric):
            column = getattr(TeamEventORM, metric)
            query = query.order_by(column.asc() if ascending else column.desc())

        if limit is not None:
            query = query.limit(limit)
        if offset is not None:
            query = query.offset(offset)

        result = await session.execute(query)
        return [
            TeamEvent.from_dict(team_event.__dict__) for team_event in result.scalars()
        ]


async def get_num_team_events() -> int:
    async with async_session() as session:
        result = await session.execute(select(func.count()).select_from(TeamEventORM))
        return result.scalar() or 0
