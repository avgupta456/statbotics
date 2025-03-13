from typing import List, Optional

from sqlalchemy.orm.session import Session as SessionType
from sqlalchemy_cockroachdb import run_transaction  # type: ignore

from src.db.main import Session
from src.db.models.team_match import TeamMatch, TeamMatchORM
from src.db.read.main import common_filters


def get_team_match(team: int, match: str) -> Optional[TeamMatch]:
    def callback(session: SessionType):
        data = session.query(TeamMatchORM).filter(
            TeamMatchORM.team == team, TeamMatchORM.match == match
        )
        out_data: Optional[TeamMatchORM] = data.first()
        if out_data is None:
            return None
        return TeamMatch.from_dict(out_data.__dict__)

    return run_transaction(Session, callback)  # type: ignore


def get_team_matches(
    team: Optional[int] = None,
    year: Optional[int] = None,
    event: Optional[str] = None,
    week: Optional[int] = None,
    match: Optional[str] = None,
    elim: Optional[bool] = None,
    metric: Optional[str] = None,
    ascending: Optional[bool] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> List[TeamMatch]:
    @common_filters(TeamMatchORM, TeamMatch, metric, ascending, limit, offset)
    def callback(session: SessionType):
        data = session.query(TeamMatchORM)
        if team is not None:
            data = data.filter(TeamMatchORM.team == team)
        if year is not None:
            data = data.filter(TeamMatchORM.year == year)
        if event is not None:
            data = data.filter(TeamMatchORM.event == event)
        if week is not None:
            data = data.filter(TeamMatchORM.week == week)
        if match is not None:
            data = data.filter(TeamMatchORM.match == match)
        if elim is not None:
            data = data.filter(TeamMatchORM.elim == elim)

        return data

    return run_transaction(Session, callback)  # type: ignore


def get_num_team_matches() -> int:
    def callback(session: SessionType) -> int:
        return session.query(TeamMatchORM).count()

    return run_transaction(Session, callback)  # type: ignore
