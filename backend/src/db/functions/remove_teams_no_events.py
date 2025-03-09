from typing import List

from sqlalchemy.future import select
from sqlalchemy import delete

from src.constants import CURR_YEAR
from src.db.main import async_session
from src.db.models.team import TeamORM
from src.db.models.team_event import TeamEventORM
from src.db.models.team_year import TeamYearORM


async def remove_teams_with_no_events() -> None:
    async with async_session() as session:
        async with session.begin():
            teams: List[int] = [
                x[0]
                for x in await session.execute(
                    select(TeamEventORM.team).group_by(TeamEventORM.team)
                )
            ]

            await session.execute(
                delete(TeamYearORM).where(
                    (TeamYearORM.team.notin_(teams)) & (TeamYearORM.year < CURR_YEAR)
                )
            )

            await session.execute(
                delete(TeamORM).where(
                    (TeamORM.team.notin_(teams)) & (TeamORM.rookie_year < CURR_YEAR)
                )
            )

            await session.commit()
