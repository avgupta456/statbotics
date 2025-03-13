from datetime import timedelta
from typing import Any, Dict, List, Optional, Tuple

from fastapi import APIRouter, Response

from src.api.query import (
    ascending_query,
    country_query,
    district_query,
    event_type_query,
    limit_query,
    metric_query,
    offset_query,
    state_query,
    week_query,
    year_query,
)
from src.db.models import Event
from src.db.read import get_event, get_events
from src.utils.alru_cache import alru_cache
from src.utils.decorators import (
    async_fail_gracefully_plural,
    async_fail_gracefully_singular,
)

router = APIRouter()


@router.get("/")
async def read_root_event():
    return {"name": "Event V3 Router"}


@alru_cache(ttl=timedelta(minutes=2))
async def get_event_cached(
    event: str,
    no_cache: bool = False,
) -> Tuple[bool, Optional[Event]]:
    return (True, get_event(event_id=event))


@alru_cache(ttl=timedelta(minutes=2))
async def get_events_cached(
    year: Optional[int] = None,
    country: Optional[str] = None,
    state: Optional[str] = None,
    district: Optional[str] = None,
    type: Optional[str] = None,
    week: Optional[int] = None,
    metric: Optional[str] = None,
    ascending: Optional[bool] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
    site: bool = False,
    no_cache: bool = False,
) -> Tuple[bool, List[Event]]:
    if not site:
        limit = min(limit or 1000, 1000)

    return (
        True,
        get_events(
            year=year,
            country=country,
            state=state,
            district=district,
            type=type,
            week=week,
            metric=metric,
            ascending=ascending,
            limit=limit,
            offset=offset,
        ),
    )


@router.get(
    "/event/{event}",
    summary="Query a single event",
    description="Returns a single Event object. Requires an event key, e.g. `2019ncwak`.",
)
@async_fail_gracefully_singular
async def read_event(response: Response, event: str) -> Dict[str, Any]:
    event_obj: Optional[Event] = await get_event_cached(event=event)
    if event_obj is None:
        raise Exception("Event not found")

    return event_obj.to_dict()


@router.get(
    "/events",
    summary="Query multiple events",
    description="Returns up to 1000 events at a time. Specify limit and offset to page through results.",
)
@async_fail_gracefully_plural
async def read_events(
    response: Response,
    year: Optional[int] = year_query,
    country: Optional[str] = country_query,
    state: Optional[str] = state_query,
    district: Optional[str] = district_query,
    type: Optional[str] = event_type_query,
    week: Optional[int] = week_query,
    metric: Optional[str] = metric_query,
    ascending: Optional[bool] = ascending_query,
    limit: Optional[int] = limit_query,
    offset: Optional[int] = offset_query,
) -> List[Dict[str, Any]]:
    events = await get_events_cached(
        year=year,
        country=country,
        state=state,
        district=district,
        type=type,
        week=week,
        metric=metric,
        ascending=ascending,
        limit=limit,
        offset=offset,
    )
    return [event.to_dict() for event in events]
