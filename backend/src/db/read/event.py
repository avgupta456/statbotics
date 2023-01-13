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
    district: Optional[str] = None,
    state: Optional[str] = None,
) -> List[Event]:
    def callback(session: SessionType):
        data = session.query(EventORM)
        if year is not None:
            data = data.filter(EventORM.year == year)  # type: ignore
        if district is not None:
            data = data.filter(EventORM.district == district)  # type: ignore
        if state is not None:
            data = data.filter(EventORM.state == state)  # type: ignore
        out_data: List[EventORM] = data.all()
        return [Event.from_dict(x.__dict__) for x in out_data]

    return run_transaction(Session, callback)  # type: ignore


def get_num_events() -> int:
    def callback(session: SessionType):
        return session.query(EventORM).count()

    return run_transaction(Session, callback)  # type: ignore
