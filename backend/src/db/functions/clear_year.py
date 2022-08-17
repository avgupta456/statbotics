from sqlalchemy.orm import Session as SessionType
from sqlalchemy_cockroachdb import run_transaction

from src.db.main import Session
from src.db.models.team_match import TeamMatchORM
from src.db.models.match import MatchORM
from src.db.models.team_event import TeamEventORM
from src.db.models.event import EventORM


def clear_year(year: int):
    def callback(session: SessionType):
        # delete all data from a given year
        for table in [TeamMatchORM, MatchORM, TeamEventORM, EventORM]:
            session.query(table).filter(table.year == year).delete(
                synchronize_session=False
            )

    run_transaction(Session, callback)
