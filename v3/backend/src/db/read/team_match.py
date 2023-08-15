from typing import List, Optional

from sqlalchemy.orm.session import Session as SessionType  # type: ignore
from sqlalchemy_cockroachdb import run_transaction  # type: ignore

from src.db.main import Session
from src.db.models.event import EventORM
from src.db.models.team_match import TeamMatch, TeamMatchORM


def get_team_match(team: int, match: str) -> Optional[TeamMatch]:
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
    team: Optional[int] = None,
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
    def callback(session: SessionType):
        data = session.query(TeamMatchORM)  # type: ignore
        if team is not None:
            data = data.filter(TeamMatchORM.team == team)  # type: ignore
        if year is not None:
            data = data.filter(TeamMatchORM.year == year)  # type: ignore
        if event is not None:
            data = data.filter(TeamMatchORM.event == event)  # type: ignore
        if week is not None:
            data = data.join(EventORM).filter(EventORM.week == week)  # type: ignore
        if match is not None:
            data = data.filter(TeamMatchORM.match == match)  # type: ignore
        if elims is not None:
            data = data.filter(TeamMatchORM.playoff == elims)  # type: ignore
        if offseason is not None:
            data = data.filter(TeamMatchORM.offseason == offseason)  # type: ignore
        if metric is not None:
            data = data.filter(TeamMatchORM.__dict__[metric] != None)  # type: ignore  # noqa: E711
            if ascending is not None and ascending:
                data = data.order_by(TeamMatchORM.__dict__[metric].asc())  # type: ignore
            else:
                data = data.order_by(TeamMatchORM.__dict__[metric].desc())  # type: ignore
        if limit is not None:
            data = data.limit(limit)  # type: ignore
        if offset is not None:
            data = data.offset(offset)  # type: ignore
        out_data: List[TeamMatchORM] = data.all()  # type: ignore
        return [TeamMatch.from_dict(x.__dict__) for x in out_data]  # type: ignore

    return run_transaction(Session, callback)  # type: ignore


def get_num_team_matches() -> int:
    def callback(session: SessionType) -> int:
        return session.query(TeamMatchORM).count()  # type: ignore

    return run_transaction(Session, callback)  # type: ignore
