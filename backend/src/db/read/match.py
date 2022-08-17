from typing import List, Optional

from sqlalchemy.orm.session import Session as SessionType
from sqlalchemy_cockroachdb import run_transaction

from src.db.main import Session
from src.db.models.event import EventORM
from src.db.models.match import Match, MatchORM


def get_matches(
    year: Optional[int] = None,
    week: Optional[int] = None,
    event_id: Optional[int] = None,
) -> List[Match]:
    def callback(session: SessionType):
        data = session.query(MatchORM)
        if year is not None:
            data = data.filter(MatchORM.year == year)
        if week is not None:
            data = data.join(EventORM).filter(EventORM.week == week)
        if event_id is not None:
            data = data.filter(MatchORM.event_id == event_id)
        out_data: List[MatchORM] = data.all()

        return [Match.from_dict(x.__dict__) for x in out_data]

    return run_transaction(Session, callback)


def get_num_matches() -> int:
    def callback(session: SessionType):
        return session.query(MatchORM).count()

    return run_transaction(Session, callback)
