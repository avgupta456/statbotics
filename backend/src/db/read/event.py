from typing import List, Optional

from sqlalchemy.orm.session import Session as SessionType
from sqlalchemy_cockroachdb import run_transaction  # type: ignore

from src.db.main import Session
from src.db.models.event import Event, EventORM


def get_event(event_id: str) -> Optional[Event]:
    def callback(session: SessionType):
        data = session.query(EventORM).filter(EventORM.key == event_id).first()  # type: ignore
        if data is None:
            return None
        return Event.from_dict(data.__dict__)

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
    def callback(session: SessionType):
        data = session.query(EventORM)
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
        if metric is not None:
            data = data.filter(EventORM.__dict__[metric] != None)  # type: ignore  # noqa: E711
            if ascending is not None and ascending:
                data = data.order_by(EventORM.__dict__[metric].asc())  # type: ignore
            else:
                data = data.order_by(EventORM.__dict__[metric].desc())  # type: ignore
        if limit is not None:
            data = data.limit(limit)  # type: ignore
        if offset is not None:
            data = data.offset(offset)  # type: ignore
        out_data: List[EventORM] = data.all()
        return [Event.from_dict(x.__dict__) for x in out_data]

    return run_transaction(Session, callback)  # type: ignore


def get_num_events() -> int:
    def callback(session: SessionType):
        return session.query(EventORM).count()

    return run_transaction(Session, callback)  # type: ignore
