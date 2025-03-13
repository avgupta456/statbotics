from typing import List, Optional

from sqlalchemy import func
from sqlalchemy.future import select
from src.db.main import async_session
from src.db.models.team_event import TeamEvent, TeamEventORM


async def get_team_event(team: int, event: str) -> Optional[TeamEvent]:
    async with async_session() as session:
        async with session.begin():
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
        query = select(TeamEventORM)

        if team is not None:
            query = query.filter(TeamEventORM.team == team)
        if year is not None:
            query = query.filter(TeamEventORM.year == year)
        if event is not None:
            query = query.filter(TeamEventORM.event == event)
        if country is not None:
            query = query.filter(TeamEventORM.country == country)
        if state is not None:
            query = query.filter(TeamEventORM.state == state)
        if district is not None:
            query = query.filter(TeamEventORM.district == district)
        if type is not None:
            query = query.filter(TeamEventORM.type == type)
        if week is not None:
            query = query.filter(TeamEventORM.week == week)

        if metric is not None:
            column = getattr(TeamEventORM, metric, None)
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

        return [TeamEvent.from_dict(team_event.__dict__) for team_event in data]


async def get_num_team_events() -> int:
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(
                select(func.count()).select_from(TeamEventORM)
            )
            return result.scalar() or 0
