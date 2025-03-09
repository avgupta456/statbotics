from typing import List, Optional

from sqlalchemy import func
from sqlalchemy.future import select
from src.db.main import async_session
from src.db.models.event import Event, EventORM


async def get_event(event_id: str) -> Optional[Event]:
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(
                select(EventORM).where(EventORM.key == event_id)
            )
            data = result.scalars().first()
            if data is None:
                return None

            return Event.from_dict(data.__dict__)


async def get_events(
    year: Optional[int] = None,
    country: Optional[str] = None,
    state: Optional[str] = None,
    district: Optional[str] = None,
    type: Optional[str] = None,
    week: Optional[int] = None,
    metric: Optional[str] = None,
    ascending: Optional[bool] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> List[Event]:
    async with async_session() as session:
        query = select(EventORM)

        if year is not None:
            query = query.filter(EventORM.year == year)
        if country is not None:
            query = query.filter(EventORM.country == country)
        if state is not None:
            query = query.filter(EventORM.state == state)
        if district is not None:
            query = query.filter(EventORM.district == district)
        if type is not None:
            query = query.filter(EventORM.type == type)
        if week is not None:
            query = query.filter(EventORM.week == week)

        if metric is not None:
            column = getattr(EventORM, metric, None)
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
        return [Event.from_dict(event.__dict__) for event in data]


async def get_num_events() -> int:
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(select(func.count()).select_from(EventORM))
            return result.scalar() or 0
