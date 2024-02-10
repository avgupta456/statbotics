from datetime import timedelta
from typing import List, Optional, Tuple

from src.db.models import Event
from src.db.read import get_event as _get_event, get_events as _get_events
from src.site.v2.models import APIEvent
from src.utils.alru_cache import alru_cache


def get_event_status_str(event: Event) -> str:
    if event.status != "Ongoing":
        return event.status

    if event.qual_matches == 0:
        return "Scheduled Unreleased"
    elif event.current_match == 0:
        return "Schedule Released"
    elif (event.current_match or -1) < (event.qual_matches or -1):
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
        qual_matches=event.qual_matches or -1,
        current_match=event.current_match or -1,
        epa_acc=event.epa_acc,
        epa_mse=event.epa_mse,
        epa_max=event.epa_max,
        epa_top8=event.epa_top_8,
        epa_top24=event.epa_top_24,
        epa_mean=event.epa_mean,
    )


@alru_cache(ttl=timedelta(minutes=1))
async def get_event(
    event: str, no_cache: bool = False
) -> Tuple[bool, Optional[APIEvent]]:
    event_obj = _get_event(event_id=event)

    # If invalid, do not cache
    if event_obj is None:
        return (False, None)

    # If valid, cache
    return (True, unpack_event(event_obj))


@alru_cache(ttl=timedelta(minutes=1))
async def get_events(
    year: Optional[int] = None,
    offseason: Optional[bool] = False,
    no_cache: bool = False,
) -> Tuple[bool, List[APIEvent]]:
    event_objs: List[Event] = _get_events(year=year, offseason=offseason)

    events = [unpack_event(event) for event in event_objs]
    return (True, events)
