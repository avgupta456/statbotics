from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Response

from src.api.event import get_event_cached, get_events_cached
from src.api.v2.utils import format_type
from src.db.models import Event
from src.utils.decorators import (
    async_fail_gracefully_plural,
    async_fail_gracefully_singular,
)

router = APIRouter()


def get_v2_event(event: Event) -> Dict[str, Any]:
    return {
        "key": event.key,
        "year": event.year,
        "name": event.name,
        "time": event.time,
        "state": event.state,
        "country": event.country,
        "district": event.district,
        "start_date": event.start_date,
        "end_date": event.end_date,
        "type": format_type(event.type),
        "week": event.week,
        "offseason": event.offseason,
        "video": event.video,
        "status": event.status,
        "qual_matches": event.qual_matches,
        "epa_max": event.epa_max,
        "epa_top8": event.epa_top_8,
        "epa_top24": event.epa_top_24,
        "epa_mean": event.epa_mean,
        "epa_sd": event.epa_sd,
        "epa_acc": event.epa_acc,
        "epa_mse": event.epa_mse,
        "rp_1_acc": event.epa_rp_1_acc,
        "rp_1_mse": None,
        "rp_2_acc": event.epa_rp_2_acc,
        "rp_2_mse": None,
    }


@router.get("/")
async def read_root():
    return {"name": "Event Router"}


@router.get(
    "/event/{event}",
    description="Get a single Event object containing event location, dates, EPA stats, prediction stats. Specify event key ex: 2019ncwak, 2022cmptx",
    response_description="An Event object.",
)
@async_fail_gracefully_singular
async def read_event(response: Response, event: str) -> Dict[str, Any]:
    event_obj: Optional[Event] = await get_event_cached(event=event)
    if event_obj is None:
        raise Exception("Event not found")

    return get_v2_event(event_obj)


@router.get(
    "/events/year/{year}",
    description="Get a list of Event objects for a single year. Specify year, ex: 2019, 2020",
    response_description="A list of Event objects. See /event/{event} for more information.",
)
@async_fail_gracefully_plural
async def read_events_year(response: Response, year: int) -> List[Dict[str, Any]]:
    events: List[Event] = await get_events_cached(year=year)
    return [get_v2_event(event) for event in events]


@router.get(
    "/events/year/{year}/district/{district}",
    description="Get a list of Event objects for a single (year, district) pair. Specify year as four-digit number, district as lowercase abbreviation.",
    response_description="A list of Event objects. See /event/{event} for more information.",
)
@async_fail_gracefully_plural
async def read_events_year_district(
    response: Response, year: int, district: str
) -> List[Dict[str, Any]]:
    events: List[Event] = await get_events_cached(year=year, district=district)
    return [get_v2_event(event) for event in events]


@router.get(
    "/events/year/{year}/state/{state}",
    description="Get a list of Event objects for a single (year, state) pair. Specify year as four-digit number, state as uppercase two-letter abbreviation.",
    response_description="A list of Event objects. See /event/{event} for more information.",
)
@async_fail_gracefully_plural
async def read_events_year_state(
    response: Response, year: int, state: str
) -> List[Dict[str, Any]]:
    events: List[Event] = await get_events_cached(year=year, state=state)
    return [get_v2_event(event) for event in events]


@router.get(
    "/events/district/{district}",
    description="Get a list of Event objects for a single district. Specify district as lowercase abbreviation, ex fnc, fim.",
    response_description="A list of Event objects. See /event/{event} for more information.",
)
@async_fail_gracefully_plural
async def read_events_district(
    response: Response, district: str
) -> List[Dict[str, Any]]:
    events: List[Event] = await get_events_cached(district=district)
    return [get_v2_event(event) for event in events]


@router.get(
    "/events/state/{state}",
    description="Get a list of Event objects for a single state. Specify state as uppercase two-letter abbreviation, ex CA, TX.",
    response_description="A list of Event objects. See /event/{event} for more information.",
)
@async_fail_gracefully_plural
async def read_events_state(response: Response, state: str) -> List[Dict[str, Any]]:
    events: List[Event] = await get_events_cached(state=state)
    return [get_v2_event(event) for event in events]


@router.get(
    "/events",
    description="Get a list of all Event objects with optional filters.",
    response_description="A list of Event objects. See /event/{event} for more information.",
)
@async_fail_gracefully_plural
async def read_events(
    response: Response,
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
) -> List[Dict[str, Any]]:
    if type is not None:
        raise Exception("Event type filter not supported")
    events: List[Event] = await get_events_cached(
        year=year,
        country=country,
        district=district,
        state=state,
        week=week,
        offseason=offseason,
        metric=metric,
        ascending=ascending,
        limit=limit,
        offset=offset,
    )
    return [get_v2_event(event) for event in events]
