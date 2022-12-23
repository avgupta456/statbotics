from datetime import timedelta
from typing import Optional

from src.db.models.event import Event
from src.db.read.event import get_event as _get_event
from src.utils.alru_cache import alru_cache


@alru_cache(ttl=timedelta(minutes=5))
async def get_event(event_id: str, no_cache: bool = False) -> Optional[Event]:
    event = _get_event(event_id)

    # If invalid, do not cache
    if event is None:
        return (False, None)  # type: ignore

    # If valid, cache
    return (True, event)  # type: ignore
