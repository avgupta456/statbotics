from typing import List, Optional

from sqlalchemy.orm.session import Session as SessionType
from sqlalchemy_cockroachdb import run_transaction  # type: ignore

from src.db.main import Session
from src.db.models.event import Event, EventORM
from src.db.read.main import common_filters


def get_event(event_id: str) -> Optional[Event]:
    def callback(session: SessionType):
        data = session.query(EventORM).filter(EventORM.key == event_id).first()
        if data is None:
            return None
        return Event.from_dict(data.__dict__)

    return run_transaction(Session, callback)  # type: ignore


def get_events(
    year: Optional[int] = None,
    country: Optional[str] = None,
    state: Optional[str] = None,
    district: Optional[str] = None,
    type: Optional[str] = None,
    week: Optional[int] = None,
    metric: Optional[str] = None,
    ascending: Optional[bool] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> List[Event]:
    @common_filters(EventORM, Event, metric, ascending, limit, offset)
    def callback(session: SessionType):
        data = session.query(EventORM)
        if year is not None:
            data = data.filter(EventORM.year == year)
        if country is not None:
            data = data.filter(EventORM.country == country)
        if state is not None:
            data = data.filter(EventORM.state == state)
        if district is not None:
            data = data.filter(EventORM.district == district)
        if type is not None:
            data = data.filter(EventORM.type == type)
        if week is not None:
            data = data.filter(EventORM.week == week)

        return data

    return run_transaction(Session, callback)  # type: ignore


def get_num_events() -> int:
    def callback(session: SessionType) -> int:
        return session.query(EventORM).count()

    return run_transaction(Session, callback)  # type: ignore
