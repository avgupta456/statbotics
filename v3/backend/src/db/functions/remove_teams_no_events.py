from typing import List

from sqlalchemy.orm import Session as SessionType
from sqlalchemy_cockroachdb import run_transaction  # type: ignore

from src.constants import CURR_YEAR
from src.db.main import Session
from src.db.models.team import TeamORM
from src.db.models.team_event import TeamEventORM
from src.db.models.team_year import TeamYearORM


def remove_teams_with_no_events() -> None:
    def callback(session: SessionType):
        teams: List[TeamORM] = [
            x[0]
            for x in session.query(TeamEventORM.team).group_by(TeamEventORM.team).all()
        ]

        # Filter teamYears with no events
        session.query(TeamYearORM).filter(
            (TeamYearORM.team.notin_(teams)) & (TeamYearORM.year < CURR_YEAR)
        ).delete()

        # Filter teams with no events
        session.query(TeamORM).filter(
            (TeamORM.team.notin_(teams)) & (TeamORM.rookie_year < CURR_YEAR)
        ).delete()

    run_transaction(Session, callback)
