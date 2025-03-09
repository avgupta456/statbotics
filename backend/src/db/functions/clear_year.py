from src.db.main import async_session
from src.db.models.etag import ETagORM
from src.db.models.event import EventORM
from src.db.models.match import MatchORM
from src.db.models.team_event import TeamEventORM
from src.db.models.team_match import TeamMatchORM
from src.db.models.team_year import TeamYearORM
from src.db.models.year import YearORM


async def clear_year(year: int) -> None:
    async with async_session() as session:
        async with session.begin():
            for table in [
                ETagORM,
                YearORM,
                TeamYearORM,
                EventORM,
                TeamEventORM,
                MatchORM,
                TeamMatchORM,
            ]:
                await session.execute(
                    table.__table__.delete().where(table.year == year)
                )
            await session.commit()
