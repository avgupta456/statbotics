from sqlalchemy.orm import Session as SessionType
from sqlalchemy_cockroachdb import run_transaction  # type: ignore

from src.db.main import Session
from src.db.models.team import TeamORM
from src.db.models.team_year import TeamYearORM


def update_team_districts() -> None:
    def callback(session: SessionType):
        session.query(TeamORM).update(
            {
                TeamORM.district: session.query(TeamYearORM.district)  # type: ignore
                .filter(TeamYearORM.team == TeamORM.team)
                .order_by(TeamYearORM.year.desc())
                .limit(1)
                .as_scalar()
            },
            synchronize_session=False,
        )

    run_transaction(Session, callback)
