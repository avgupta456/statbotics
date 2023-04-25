from typing import List, Optional

from sqlalchemy.orm.session import Session as SessionType
from sqlalchemy_cockroachdb import run_transaction  # type: ignore

from src.db.main import Session
from src.db.models.event import EventORM
from src.db.models.match import Match, MatchORM


def get_match(match: str) -> Optional[Match]:
    def callback(session: SessionType):
        data = session.query(MatchORM).filter(MatchORM.key == match).first()  # type: ignore

        if data is None:
            return None

        return Match.from_dict(data.__dict__)

    return run_transaction(Session, callback)  # type: ignore


def get_matches(
    team: Optional[int] = None,
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
    def callback(session: SessionType):
        data = session.query(MatchORM)
        if team is not None:
            data = data.filter(  # type: ignore
                (MatchORM.red_1 == team)  # type: ignore
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
            data = data.join(EventORM).filter(EventORM.week == week)  # type: ignore
        if elims is not None:
            data = data.filter(MatchORM.playoff == elims)  # type: ignore
        if offseason is not None:
            data = data.filter(MatchORM.offseason == offseason)  # type: ignore
        if metric is not None:
            data = data.filter(MatchORM.__dict__[metric] != None)  # type: ignore  # noqa: E711
            if ascending is not None and ascending:
                data = data.order_by(MatchORM.__dict__[metric].asc())  # type: ignore
            else:
                data = data.order_by(MatchORM.__dict__[metric].desc())  # type: ignore
        if limit is not None:
            data = data.limit(limit)  # type: ignore
        if offset is not None:
            data = data.offset(offset)  # type: ignore
        out_data: List[MatchORM] = data.all()

        return [Match.from_dict(x.__dict__) for x in out_data]

    return run_transaction(Session, callback)  # type: ignore


def get_num_matches() -> int:
    def callback(session: SessionType):
        return session.query(MatchORM).count()

    return run_transaction(Session, callback)  # type: ignore
