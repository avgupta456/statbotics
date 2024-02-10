from datetime import timedelta
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Response

from src.db.models import Event
from src.db.read import get_event, get_events
from src.utils.alru_cache import alru_cache
from src.utils.decorators import (
    async_fail_gracefully_api_plural,
    async_fail_gracefully_api_singular,
)

router = APIRouter()


@router.get("/")
async def read_root():
    return {"name": "Event Router"}


@alru_cache(ttl=timedelta(hours=1))
async def get_event_cached(event: str) -> Optional[Event]:
    return (True, get_event(event_id=event))  # type: ignore


@alru_cache(ttl=timedelta(hours=1))
async def get_events_cached(
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
    return (  # type: ignore
        True,
        get_events(
            year=year,
            country=country,
            district=district,
            state=state,
            type=type,
            week=week,
            offseason=offseason,
            metric=metric,
            ascending=ascending,
            limit=limit,
            offset=offset,
        ),
    )


@router.get(
    "/event/{event}",
    description="Get a single Event object containing event location, dates, EPA stats, prediction stats. Specify event key ex: 2019ncwak, 2022cmptx",
    response_description="An Event object.",
)
@async_fail_gracefully_api_singular
async def read_event(response: Response, event: str) -> Dict[str, Any]:
    event_obj: Optional[Event] = await get_event_cached(event=event)
    if event_obj is None:
        raise Exception("Event not found")

    return event_obj.as_dict()


@router.get(
    "/events/year/{year}",
    description="Get a list of Event objects for a single year. Specify year, ex: 2019, 2020",
    response_description="A list of Event objects. See /event/{event} for more information.",
)
@async_fail_gracefully_api_plural
async def read_events_year(response: Response, year: int) -> List[Dict[str, Any]]:
    events: List[Event] = await get_events_cached(year=year)
    return [event.as_dict() for event in events]


@router.get(
    "/events/year/{year}/district/{district}",
    description="Get a list of Event objects for a single (year, district) pair. Specify year as four-digit number, district as lowercase abbreviation.",
    response_description="A list of Event objects. See /event/{event} for more information.",
)
@async_fail_gracefully_api_plural
async def read_events_year_district(
    response: Response, year: int, district: str
) -> List[Dict[str, Any]]:
    events: List[Event] = await get_events_cached(year=year, district=district)
    return [event.as_dict() for event in events]


@router.get(
    "/events/year/{year}/state/{state}",
    description="Get a list of Event objects for a single (year, state) pair. Specify year as four-digit number, state as uppercase two-letter abbreviation.",
    response_description="A list of Event objects. See /event/{event} for more information.",
)
@async_fail_gracefully_api_plural
async def read_events_year_state(
    response: Response, year: int, state: str
) -> List[Dict[str, Any]]:
    events: List[Event] = await get_events_cached(year=year, state=state)
    return [event.as_dict() for event in events]


@router.get(
    "/events/district/{district}",
    description="Get a list of Event objects for a single district. Specify district as lowercase abbreviation, ex fnc, fim.",
    response_description="A list of Event objects. See /event/{event} for more information.",
)
@async_fail_gracefully_api_plural
async def read_events_district(
    response: Response, district: str
) -> List[Dict[str, Any]]:
    events: List[Event] = await get_events_cached(district=district)
    return [event.as_dict() for event in events]


@router.get(
    "/events/state/{state}",
    description="Get a list of Event objects for a single state. Specify state as uppercase two-letter abbreviation, ex CA, TX.",
    response_description="A list of Event objects. See /event/{event} for more information.",
)
@async_fail_gracefully_api_plural
async def read_events_state(response: Response, state: str) -> List[Dict[str, Any]]:
    events: List[Event] = await get_events_cached(state=state)
    return [event.as_dict() for event in events]


@router.get(
    "/events",
    description="Get a list of all Event objects with optional filters.",
    response_description="A list of Event objects. See /event/{event} for more information.",
)
@async_fail_gracefully_api_plural
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
    events: List[Event] = await get_events_cached(
        year=year,
        country=country,
        district=district,
        state=state,
        type=type,
        week=week,
        offseason=offseason,
        metric=metric,
        ascending=ascending,
        limit=limit,
        offset=offset,
    )
    return [event.as_dict() for event in events]
