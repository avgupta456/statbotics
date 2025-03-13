from typing import List, Optional

from sqlalchemy import func
from sqlalchemy.future import select
from src.db.main import async_session
from src.db.models.match import Match, MatchORM


async def get_match(match: str) -> Optional[Match]:
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(
                select(MatchORM).where(MatchORM.key == match)
            )
            data = result.scalars().first()
            if data is None:
                return None

            return Match.from_dict(data.__dict__)


async def get_matches(
    team: Optional[int] = None,
    year: Optional[int] = None,
    event: Optional[str] = None,
    week: Optional[int] = None,
    elim: Optional[bool] = None,
    metric: Optional[str] = None,
    ascending: Optional[bool] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> List[Match]:
    async with async_session() as session:
        query = select(MatchORM)

        if team is not None:
            query = query.filter(
                (MatchORM.red_1 == team)
                | (MatchORM.red_2 == team)
                | (MatchORM.red_3 == team)
                | (MatchORM.blue_1 == team)
                | (MatchORM.blue_2 == team)
                | (MatchORM.blue_3 == team)
            )
        if year is not None:
            query = query.filter(MatchORM.year == year)
        if event is not None:
            query = query.filter(MatchORM.event == event)
        if week is not None:
            query = query.filter(MatchORM.week == week)
        if elim is not None:
            query = query.filter(MatchORM.elim == elim)

        if metric is not None:
            column = getattr(MatchORM, metric, None)
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

        return [Match.from_dict(match.__dict__) for match in data]


async def get_num_matches() -> int:
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(select(func.count()).select_from(MatchORM))
            return result.scalar() or 0
