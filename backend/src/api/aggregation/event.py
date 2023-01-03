from datetime import timedelta
from typing import Optional

from src.api.models import APIEvent
from src.db.models import Event
from src.db.read import get_event as _get_event
from src.utils.alru_cache import alru_cache


def unpack_event(event: Event) -> APIEvent:
    return APIEvent(
        event_name=event.name,
        year=event.year,
    )


@alru_cache(ttl=timedelta(minutes=5))
async def get_event(event: str, no_cache: bool = False) -> Optional[APIEvent]:
    event_obj = _get_event(event)

    # If invalid, do not cache
    if event_obj is None:
        return (False, None)  # type: ignore

    # If valid, cache
    return (True, unpack_event(event_obj))  # type: ignore
