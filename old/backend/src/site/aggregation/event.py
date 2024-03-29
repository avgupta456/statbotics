from datetime import timedelta
from typing import List, Optional

from src.db.models import Event
from src.db.read import get_event as _get_event, get_events as _get_events
from src.site.models import APIEvent
from src.utils.alru_cache import alru_cache


def get_event_status_str(event: Event) -> str:
    if event.status != "Ongoing":
        return event.status

    if event.qual_matches == 0:
        return "Scheduled Unreleased"
    elif event.current_match == 0:
        return "Schedule Released"
    elif event.current_match < event.qual_matches:
        return "Qual " + str(event.current_match)
    elif event.current_match == event.qual_matches:
        return "Quals Over"
    else:
        return "Elims Ongoing"


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
        offseason=event.offseason,
        status=event.status,
        status_str=get_event_status_str(event),
        qual_matches=event.qual_matches,
        current_match=event.current_match,
        epa_acc=event.epa_acc,
        epa_mse=event.epa_mse,
        epa_max=event.epa_max,
        epa_top8=event.epa_top8,
        epa_top24=event.epa_top24,
        epa_mean=event.epa_mean,
    )


@alru_cache(ttl=timedelta(minutes=1))
async def get_event(event: str, no_cache: bool = False) -> Optional[APIEvent]:
    event_obj = _get_event(event_id=event)

    # If invalid, do not cache
    if event_obj is None:
        return (False, None)  # type: ignore

    # If valid, cache
    return (True, unpack_event(event_obj))  # type: ignore


@alru_cache(ttl=timedelta(minutes=1))
async def get_events(
    year: Optional[int] = None,
    offseason: Optional[bool] = False,
    no_cache: bool = False,
) -> List[APIEvent]:
    event_objs: List[Event] = _get_events(year=year, offseason=offseason)

    events = [unpack_event(event) for event in event_objs]
    return (True, events)  # type: ignore
