from datetime import timedelta
from typing import List, Optional

from src.api.models import APIEvent
from src.db.models import Event
from src.db.read import get_event as _get_event, get_events as _get_events
from src.utils.alru_cache import alru_cache


def unpack_event(event: Event) -> APIEvent:
    return APIEvent(
        key=event.key,
        name=event.name,
        year=event.year,
        week=event.week,
        start_date=event.start_date,
        end_date=event.end_date,
        country=event.country,
        state=event.state,
        district=event.district,
        status=event.status,
    )


@alru_cache(ttl=timedelta(minutes=5))
async def get_event(event: str, no_cache: bool = False) -> Optional[APIEvent]:
    event_obj = _get_event(event)

    # If invalid, do not cache
    if event_obj is None:
        return (False, None)  # type: ignore

    # If valid, cache
    return (True, unpack_event(event_obj))  # type: ignore


@alru_cache(ttl=timedelta(minutes=5))
async def get_events(
    year: Optional[int] = None, no_cache: bool = False
) -> List[APIEvent]:
    event_objs: List[Event] = _get_events(year=year)

    events = [unpack_event(event) for event in event_objs]
    return (True, events)  # type: ignore
