from typing import List, Optional

from sqlalchemy.orm.session import Session as SessionType  # type: ignore
from sqlalchemy_cockroachdb import run_transaction  # type: ignore

from src.db.main import Session
from src.db.models.match import Match, MatchORM
from src.db.read.main import common_filters


def get_match(match: str) -> Optional[Match]:
    def callback(session: SessionType):
        data = session.query(MatchORM).filter(MatchORM.key == match).first()  # type: ignore

        if data is None:
            return None

        return Match.from_dict(data.__dict__)  # type: ignore

    return run_transaction(Session, callback)  # type: ignore


def get_matches(
    team: Optional[str] = None,
    year: Optional[int] = None,
    event: Optional[str] = None,
    week: Optional[int] = None,
    elims: Optional[bool] = None,
    offseason: Optional[bool] = False,
    metric: Optional[str] = None,
    ascending: Optional[bool] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> List[Match]:
    @common_filters(MatchORM, Match, metric, ascending, limit, offset)
    def callback(session: SessionType):  # type: ignore
        data = session.query(MatchORM)  # type: ignore
        if team is not None:
            data = data.filter(  # type: ignore
                (MatchORM.red_1 == team)
                | (MatchORM.red_2 == team)
                | (MatchORM.red_3 == team)
                | (MatchORM.blue_1 == team)
                | (MatchORM.blue_2 == team)
                | (MatchORM.blue_3 == team)
            )
        if year is not None:
            data = data.filter(MatchORM.year == year)  # type: ignore
        if event is not None:
            data = data.filter(MatchORM.event == event)  # type: ignore
        if week is not None:
            data = data.filter(MatchORM.week == week)  # type: ignore
        if elims is not None:
            data = data.filter(MatchORM.playoff == elims)  # type: ignore
        if offseason is not None:
            data = data.filter(MatchORM.offseason == offseason)  # type: ignore

        return data  # type: ignore

    return run_transaction(Session, callback)  # type: ignore


def get_num_matches() -> int:
    def callback(session: SessionType) -> int:
        return session.query(MatchORM).count()  # type: ignore

    return run_transaction(Session, callback)  # type: ignore
