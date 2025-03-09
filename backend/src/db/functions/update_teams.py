from sqlalchemy import update
from sqlalchemy.future import select

from src.db.main import async_session
from src.db.models.team import TeamORM
from src.db.models.team_year import TeamYearORM


async def update_team_districts() -> None:
    async with async_session() as session:
        async with session.begin():
            # Subquery to get the most recent district for each team
            stmt = (
                select(TeamYearORM.district)
                .filter(TeamYearORM.team == TeamORM.team)
                .order_by(TeamYearORM.year.desc())
                .limit(1)
                .scalar_subquery()
            )

            # Perform the update operation using the `update()` method on the table
            await session.execute(
                update(TeamORM)
                .where(TeamORM.team == TeamORM.team)
                .values({TeamORM.district: stmt})
            )
