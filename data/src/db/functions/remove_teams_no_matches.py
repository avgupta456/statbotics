from sqlalchemy.orm import Session as SessionType
from sqlalchemy_cockroachdb import run_transaction  # type: ignore

from db.main import Session
from db.models.team import TeamORM
from db.models.team_event import TeamEventORM
from db.models.team_match import TeamMatchORM
from db.models.team_year import TeamYearORM


def remove_teams_with_no_matches() -> None:
    def callback(session: SessionType):
        teams = [
            x[0]
            for x in session.query(TeamMatchORM.team)  # type: ignore
            .group_by(TeamMatchORM.team)
            .all()
        ]

        """Filter teams, teamYears, teamEvents with no matches"""
        session.query(TeamEventORM).filter(TeamEventORM.team.notin_(teams)).delete()  # type: ignore
        session.query(TeamYearORM).filter(TeamYearORM.team.notin_(teams)).delete()  # type: ignore
        session.query(TeamORM).filter(TeamORM.team.notin_(teams)).delete()  # type: ignore

    return run_transaction(Session, callback)  # type: ignore
