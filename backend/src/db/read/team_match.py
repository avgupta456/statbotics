from typing import List, Optional

from sqlalchemy import func
from sqlalchemy.future import select
from src.db.main import async_session
from src.db.models.team_match import TeamMatch, TeamMatchORM


async def get_team_match(team: int, match: str) -> Optional[TeamMatch]:
    async with async_session() as session:
        result = await session.execute(
            select(TeamMatchORM).where(
                TeamMatchORM.team == team, TeamMatchORM.match == match
            )
        )
        data = result.scalars().first()
        if data is None:
            return None

        return TeamMatch.from_dict(data.__dict__)


async def get_team_matches(
    team: Optional[int] = None,
    year: Optional[int] = None,
    event: Optional[str] = None,
    week: Optional[int] = None,
    match: Optional[str] = None,
    elim: Optional[bool] = None,
    metric: Optional[str] = None,
    ascending: Optional[bool] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> List[TeamMatch]:
    async with async_session() as session:
        filters = []

        if team is not None:
            filters.append(TeamMatchORM.team == team)
        if year is not None:
            filters.append(TeamMatchORM.year == year)
        if event is not None:
            filters.append(TeamMatchORM.event == event)
        if week is not None:
            filters.append(TeamMatchORM.week == week)
        if match is not None:
            filters.append(TeamMatchORM.match == match)
        if elim is not None:
            filters.append(TeamMatchORM.elim == elim)

        query = select(TeamMatchORM).filter(*filters)

        if metric and hasattr(TeamMatchORM, metric):
            column = getattr(TeamMatchORM, metric)
            query = query.order_by(column.asc() if ascending else column.desc())

        if limit is not None:
            query = query.limit(limit)
        if offset is not None:
            query = query.offset(offset)

        result = await session.execute(query)
        return [
            TeamMatch.from_dict(team_match.__dict__) for team_match in result.scalars()
        ]


async def get_num_team_matches() -> int:
    async with async_session() as session:
        result = await session.execute(select(func.count()).select_from(TeamMatchORM))
        return result.scalar() or 0
