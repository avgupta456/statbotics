from typing import List, Optional

from sqlalchemy.orm.session import Session as SessionType
from sqlalchemy_cockroachdb import run_transaction  # type: ignore

from db.main import Session
from db.models.event import EventORM
from db.models.match import Match, MatchORM


def get_matches(
    year: Optional[int] = None,
    week: Optional[int] = None,
    event_id: Optional[int] = None,
) -> List[Match]:
    def callback(session: SessionType):
        data = session.query(MatchORM)  # type: ignore
        if year is not None:
            data = data.filter(MatchORM.year == year)  # type: ignore
        if week is not None:
            data = data.join(EventORM).filter(EventORM.week == week)  # type: ignore
        if event_id is not None:
            data = data.filter(MatchORM.event_id == event_id)  # type: ignore
        data: List[MatchORM] = data.all()  # type: ignore

        return [Match.from_dict(x.__dict__) for x in data]

    return run_transaction(Session, callback)  # type: ignore


def get_num_matches() -> int:
    def callback(session: SessionType):
        return session.query(MatchORM).count()  # type: ignore

    return run_transaction(Session, callback)  # type: ignore
