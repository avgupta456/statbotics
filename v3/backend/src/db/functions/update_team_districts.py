# type: ignore

from typing import List

from sqlalchemy.orm import Session as SessionType
from sqlalchemy_cockroachdb import run_transaction

from src.db.main import Session
from src.db.models.team import TeamORM
from src.db.models.team_event import TeamEventORM
from src.db.models.team_year import TeamYearORM


def update_team_districts() -> None:
    def callback(session: SessionType):
        teams: List[TeamORM] = [
            x[0]
            for x in session.query(TeamEventORM.team).group_by(TeamEventORM.team).all()
        ]

        session.query(TeamORM).filter(TeamORM.team.in_(teams)).update(
            {
                TeamORM.district: session.query(TeamYearORM.district)
                .filter(TeamYearORM.team == TeamORM.team)
                .order_by(TeamYearORM.year.desc())
                .limit(1)
                .as_scalar()
            },
            synchronize_session=False,
        )

    return run_transaction(Session, callback)
