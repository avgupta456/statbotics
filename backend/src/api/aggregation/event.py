from datetime import timedelta
from typing import Optional

from src.api.models.event import APIEvent
from src.db.models.event import Event
from src.db.read.event import get_event as _get_event
from src.utils.alru_cache import alru_cache


def unpack_event(event: Event) -> APIEvent:
    return APIEvent(
        event_name=event.name,
    )


@alru_cache(ttl=timedelta(minutes=5))
async def get_event(event_id: str, no_cache: bool = False) -> Optional[APIEvent]:
    event = _get_event(event_id)

    # If invalid, do not cache
    if event is None:
        return (False, None)  # type: ignore

    # If valid, cache
    return (True, unpack_event(event))  # type: ignore
