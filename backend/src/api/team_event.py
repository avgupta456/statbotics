from datetime import timedelta
from typing import Any, Dict, List, Optional, Tuple

from fastapi import APIRouter, Response

from src.api.query import (
    ascending_query,
    country_query,
    district_query,
    event_query,
    event_type_query,
    limit_query,
    metric_query,
    offset_query,
    state_query,
    team_query,
    week_query,
    year_query,
)
from src.db.models import TeamEvent
from src.db.read import get_team_event, get_team_events
from src.utils.alru_cache import alru_cache
from src.utils.decorators import (
    async_fail_gracefully_plural,
    async_fail_gracefully_singular,
)

router = APIRouter()


@router.get("/")
async def read_root_team_event():
    return {"name": "Team Event V3 Router"}


@alru_cache(ttl=timedelta(minutes=2))
async def get_team_event_cached(
    team: int, event: str, no_cache: bool = False
) -> Tuple[bool, Optional[TeamEvent]]:
    return (True, get_team_event(team=team, event=event))


@alru_cache(ttl=timedelta(minutes=2))
async def get_team_events_cached(
    team: Optional[int] = None,
    year: Optional[int] = None,
    event: Optional[str] = None,
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
) -> Tuple[bool, List[TeamEvent]]:
    if not site:
        limit = min(limit or 1000, 1000)

    return (
        True,
        get_team_events(
            team=team,
            year=year,
            event=event,
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
    "/team_event/{team}/{event}",
    summary="Query a single team event",
    description="Returns a single Team Event object. Requires a team number and event key, e.g. `5511` and `2019ncwak`.",
)
@async_fail_gracefully_singular
async def read_team_event(response: Response, team: int, event: str) -> Dict[str, Any]:
    team_event_obj: Optional[TeamEvent] = await get_team_event_cached(
        team=team, event=event
    )
    if team_event_obj is None:
        raise Exception("Team Event not found")

    return team_event_obj.to_dict()


@router.get(
    "/team_events",
    summary="Query multiple team events",
    description="Returns up to 1000 team events at a time. Specify limit and offset to page through results.",
)
@async_fail_gracefully_plural
async def read_team_events(
    response: Response,
    team: Optional[int] = team_query,
    year: Optional[int] = year_query,
    event: Optional[str] = event_query,
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
    team_events: List[TeamEvent] = await get_team_events_cached(
        team=team,
        year=year,
        event=event,
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
    return [team_event.to_dict() for team_event in team_events]
