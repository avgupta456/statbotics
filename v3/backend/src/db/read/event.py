from typing import List, Optional

from sqlalchemy.orm.session import Session as SessionType  # type: ignore
from sqlalchemy_cockroachdb import run_transaction  # type: ignore

from src.db.main import Session
from src.db.models.event import Event, EventORM
from src.db.read.main import common_filters


def get_event(event_id: str) -> Optional[Event]:
    def callback(session: SessionType):
        data = session.query(EventORM).filter(EventORM.key == event_id).first()  # type: ignore
        if data is None:
            return None
        return Event.from_dict(data.__dict__)  # type: ignore

    return run_transaction(Session, callback)  # type: ignore


def get_events(
    year: Optional[int] = None,
    country: Optional[str] = None,
    district: Optional[str] = None,
    state: Optional[str] = None,
    type: Optional[int] = None,
    week: Optional[int] = None,
    offseason: Optional[bool] = False,
    metric: Optional[str] = None,
    ascending: Optional[bool] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> List[Event]:
    print(metric, ascending, limit, offset)

    @common_filters(EventORM, Event, metric, ascending, limit, offset)
    def callback(session: SessionType):  # type: ignore
        data = session.query(EventORM)  # type: ignore
        if year is not None:
            data = data.filter(EventORM.year == year)  # type: ignore
        if country is not None:
            data = data.filter(EventORM.country == country)  # type: ignore
        if district is not None:
            data = data.filter(EventORM.district == district)  # type: ignore
        if state is not None:
            data = data.filter(EventORM.state == state)  # type: ignore
        if type is not None:
            data = data.filter(EventORM.type == type)  # type: ignore
        if week is not None:
            data = data.filter(EventORM.week == week)  # type: ignore
        if offseason is not None:
            data = data.filter(EventORM.offseason == offseason)  # type: ignore

        return data  # type: ignore

    return run_transaction(Session, callback)  # type: ignore


def get_num_events() -> int:
    def callback(session: SessionType) -> int:
        return session.query(EventORM).count()  # type: ignore

    return run_transaction(Session, callback)  # type: ignore
