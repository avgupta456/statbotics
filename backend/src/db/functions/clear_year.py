from sqlalchemy.orm import Session as SessionType
from sqlalchemy_cockroachdb import run_transaction  # type: ignore

from src.db.main import Session
from src.db.models.etag import ETagORM
from src.db.models.event import EventORM
from src.db.models.match import MatchORM
from src.db.models.team_event import TeamEventORM
from src.db.models.team_match import TeamMatchORM
from src.db.models.team_year import TeamYearORM
from src.db.models.year import YearORM


def clear_year(year: int) -> None:
    def callback(session: SessionType):
        # delete all data from a given year
        for table in [
            ETagORM,
            YearORM,
            TeamYearORM,
            EventORM,
            TeamEventORM,
            MatchORM,
            TeamMatchORM,
        ]:
            session.query(table).filter(table.year == year).delete(
                synchronize_session=False
            )

    run_transaction(Session, callback)
