from typing import List, Optional

from sqlalchemy import func
from sqlalchemy.future import select

from src.db.models.etag import ETag, ETagORM
from src.db.main import async_session


async def get_etags(
    year: Optional[int] = None, path: Optional[str] = None
) -> List[ETag]:
    async with async_session() as session:
        query = select(ETagORM)

        if year is not None:
            query = query.filter(ETagORM.year == year)
        if path is not None:
            query = query.filter(ETagORM.path == path)

        result = await session.execute(query)
        etags_orm = result.scalars().all()

        return [ETag.from_dict(etag.__dict__) for etag in etags_orm]


async def get_num_etags() -> int:
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(select(func.count()).select_from(ETagORM))
            return result.scalar() or 0
