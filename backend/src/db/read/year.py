from typing import List, Optional

from sqlalchemy import func
from sqlalchemy.future import select
from src.db.main import async_session
from src.db.models.year import Year, YearORM


async def get_year(year: int) -> Optional[Year]:
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(select(YearORM).where(YearORM.year == year))
            data = result.scalars().first()
            if data is None:
                return None

            return Year.from_dict(data.__dict__)


async def get_years(
    metric: Optional[str] = None,
    ascending: Optional[bool] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> List[Year]:
    async with async_session() as session:
        query = select(YearORM)

        if metric is not None:
            column = getattr(YearORM, metric, None)
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

        return [Year.from_dict(year.__dict__) for year in data]


async def get_num_years() -> int:
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(select(func.count()).select_from(YearORM))
            return result.scalar() or 0
