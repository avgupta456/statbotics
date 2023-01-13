from typing import List, Optional

from sqlalchemy.orm.session import Session as SessionType
from sqlalchemy_cockroachdb import run_transaction  # type: ignore

from src.db.main import Session
from src.db.models.team_match import TeamMatch, TeamMatchORM


def get_team_match(team: int, match: str) -> Optional[TeamMatch]:
    def callback(session: SessionType):
        data = session.query(TeamMatchORM).filter(  # type: ignore
            TeamMatchORM.team == team, TeamMatchORM.match == match
        )
        out_data: Optional[TeamMatchORM] = data.first()
        if out_data is None:
            return None
        return TeamMatch.from_dict(out_data.__dict__)

    return run_transaction(Session, callback)  # type: ignore


def get_team_matches(
    year: Optional[int] = None,
    event: Optional[str] = None,
    team: Optional[int] = None,
    match: Optional[str] = None,
) -> List[TeamMatch]:
    def callback(session: SessionType):
        data = session.query(TeamMatchORM)
        if year is not None:
            data = data.filter(TeamMatchORM.year == year)  # type: ignore
        if event is not None:
            data = data.filter(TeamMatchORM.event == event)  # type: ignore
        if team is not None:
            data = data.filter(TeamMatchORM.team == team)  # type: ignore
        if match is not None:
            data = data.filter(TeamMatchORM.match == match)  # type: ignore
        out_data: List[TeamMatchORM] = data.all()
        return [TeamMatch.from_dict(x.__dict__) for x in out_data]

    return run_transaction(Session, callback)  # type: ignore


def get_num_team_matches() -> int:
    def callback(session: SessionType):
        return session.query(TeamMatchORM).count()

    return run_transaction(Session, callback)  # type: ignore
