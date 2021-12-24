from typing import Dict

from sqlalchemy.orm import Session as SessionType
from sqlalchemy_cockroachdb import run_transaction  # type: ignore

from db.main import Session
from db.models.team_match import TeamMatchORM


def update_team_matches_elo(year: int, team_match_ids: Dict[int, float]):
    def callback(session: SessionType):
        data = session.query(TeamMatchORM).filter(TeamMatchORM.year_id == year).all()  # type: ignore
        for item in data:
            item.elo = team_match_ids[item.id]  # type: ignore

    run_transaction(Session, callback)  # type: ignore
