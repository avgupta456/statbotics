from typing import List, Optional

from sqlalchemy.orm.session import Session as SessionType  # type: ignore
from sqlalchemy_cockroachdb import run_transaction  # type: ignore

from src.db.main import Session
from src.db.models.team_match import TeamMatch, TeamMatchORM
from src.db.read.main import common_filters


def get_team_match(team: str, match: str) -> Optional[TeamMatch]:
    def callback(session: SessionType):
        data = session.query(TeamMatchORM).filter(  # type: ignore
            TeamMatchORM.team == team, TeamMatchORM.match == match
        )
        out_data: Optional[TeamMatchORM] = data.first()  # type: ignore
        if out_data is None:
            return None
        return TeamMatch.from_dict(out_data.__dict__)  # type: ignore

    return run_transaction(Session, callback)  # type: ignore


def get_team_matches(
    team: Optional[str] = None,
    year: Optional[int] = None,
    event: Optional[str] = None,
    week: Optional[int] = None,
    match: Optional[str] = None,
    elims: Optional[bool] = None,
    offseason: Optional[bool] = False,
    metric: Optional[str] = None,
    ascending: Optional[bool] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> List[TeamMatch]:
    @common_filters(TeamMatchORM, TeamMatch, metric, ascending, limit, offset)
    def callback(session: SessionType):  # type: ignore
        data = session.query(TeamMatchORM)  # type: ignore
        if team is not None:
            data = data.filter(TeamMatchORM.team == team)  # type: ignore
        if year is not None:
            data = data.filter(TeamMatchORM.year == year)  # type: ignore
        if event is not None:
            data = data.filter(TeamMatchORM.event == event)  # type: ignore
        if week is not None:
            data = data.filter(TeamMatchORM.week == week)  # type: ignore
        if match is not None:
            data = data.filter(TeamMatchORM.match == match)  # type: ignore
        if elims is not None:
            data = data.filter(TeamMatchORM.playoff == elims)  # type: ignore
        if offseason is not None:
            data = data.filter(TeamMatchORM.offseason == offseason)  # type: ignore

        return data  # type: ignore

    return run_transaction(Session, callback)  # type: ignore


def get_num_team_matches() -> int:
    def callback(session: SessionType) -> int:
        return session.query(TeamMatchORM).count()  # type: ignore

    return run_transaction(Session, callback)  # type: ignore
