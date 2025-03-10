from typing import List, Optional

from sqlalchemy import func
from sqlalchemy.future import select

from src.db.models.etag import ETag, ETagORM
from src.db.main import async_session


async def get_etags(
    year: Optional[int] = None, path: Optional[str] = None
) -> List[ETag]:
    async with async_session() as session:
        filters = []
        if year is not None:
            filters.append(ETagORM.year == year)
        if path is not None:
            filters.append(ETagORM.path == path)

        query = select(ETagORM).filter(*filters)

        result = await session.execute(query)
        return [ETag.from_dict(etag.__dict__) for etag in result.scalars()]


async def get_num_etags() -> int:
    async with async_session() as session:
        result = await session.execute(select(func.count()).select_from(ETagORM))
        return result.scalar() or 0
