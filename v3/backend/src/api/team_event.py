from datetime import timedelta
from typing import Any, Dict, List, Optional, Tuple

from fastapi import APIRouter, Response

from src.db.models import TeamEvent
from src.db.read import get_team_event, get_team_events
from src.utils.alru_cache import alru_cache
from src.utils.decorators import (
    async_fail_gracefully_api_plural,
    async_fail_gracefully_api_singular,
)

router = APIRouter()


@router.get("/")
async def read_root():
    return {"name": "Team Event Router"}


@alru_cache(ttl=timedelta(hours=1))
async def get_team_event_cached(
    team: str, event: str
) -> Tuple[bool, Optional[TeamEvent]]:
    return (True, get_team_event(team=team, event=event))


@alru_cache(ttl=timedelta(hours=1))
async def get_team_events_cached(
    team: Optional[str] = None,
    year: Optional[int] = None,
    event: Optional[str] = None,
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
) -> Tuple[bool, List[TeamEvent]]:
    return (
        True,
        get_team_events(
            team=team,
            year=year,
            event=event,
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
    "/team_event/{team}/{event}",
    description="Get a single Team Event object containing event metadata, EPA statistics, and winrate. Specify team number and event key ex: 5511, 2019ncwak",
    response_description="A Team Event object.",
)
@async_fail_gracefully_api_singular
async def read_team_event(response: Response, team: str, event: str) -> Dict[str, Any]:
    team_event_obj: Optional[TeamEvent] = await get_team_event_cached(
        team=team, event=event
    )
    if team_event_obj is None:
        raise Exception("Team Event not found")

    return team_event_obj.to_dict()


@router.get(
    "/team_events/team/{team}",
    description="Get a list of Team Event objects for a single team. Specify team number, ex: 5511",
    response_description="A list of Team Event objects. See /team_event/{team}/{event} for more information.",
)
@async_fail_gracefully_api_plural
async def read_team_events_team(response: Response, team: str) -> List[Dict[str, Any]]:
    team_events: List[TeamEvent] = await get_team_events_cached(team=team)
    return [team_event.to_dict() for team_event in team_events]


@router.get(
    "/team_events/team/{team}/year/{year}",
    description="Get a list of Team Event objects for a single team and year. Specify team number and year, ex: 5511, 2019",
    response_description="A list of Team Event objects. See /team_event/{team}/{event} for more information.",
)
@async_fail_gracefully_api_plural
async def read_team_events_team_year(
    response: Response, team: str, year: int
) -> List[Dict[str, Any]]:
    team_events: List[TeamEvent] = await get_team_events_cached(team=team, year=year)
    return [team_event.to_dict() for team_event in team_events]


@router.get(
    "/team_events/event/{event}",
    description="Get a list of Team Event objects for a single event. Specify event key, ex: 2019ncwak",
    response_description="A list of Team Event objects. See /team_event/{team}/{event} for more information.",
)
@async_fail_gracefully_api_plural
async def read_team_events_event(
    response: Response, event: str
) -> List[Dict[str, Any]]:
    team_events: List[TeamEvent] = await get_team_events_cached(event=event)
    return [team_event.to_dict() for team_event in team_events]


@router.get(
    "/team_events/year/{year}/district/{district}",
    description="Get a list of Team Event objects for a single year and district. Specify year and district, ex: 2019, fnc",
    response_description="A list of Team Event objects. See /team_event/{team}/{event} for more information.",
)
@async_fail_gracefully_api_plural
async def read_team_events_year_district(
    response: Response, year: int, district: str
) -> List[Dict[str, Any]]:
    team_events: List[TeamEvent] = await get_team_events_cached(
        year=year, district=district
    )
    return [team_event.to_dict() for team_event in team_events]


@router.get(
    "/team_events/year/{year}/state/{state}",
    description="Get a list of Team Event objects for a single year and state. Specify year and state, ex: 2019, NC",
    response_description="A list of Team Event objects. See /team_event/{team}/{event} for more information.",
)
@async_fail_gracefully_api_plural
async def read_team_events_year_state(
    response: Response, year: int, state: str
) -> List[Dict[str, Any]]:
    team_events: List[TeamEvent] = await get_team_events_cached(year=year, state=state)
    return [team_event.to_dict() for team_event in team_events]


@router.get(
    "/team_events",
    description="Get a list of all Team Event objects with optional filters.",
    response_description="A list of Team Event objects. See /team_event/{team}/{event} for more information.",
)
@async_fail_gracefully_api_plural
async def read_team_events(
    response: Response,
    team: Optional[str] = None,
    year: Optional[int] = None,
    event: Optional[str] = None,
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
    team_events: List[TeamEvent] = await get_team_events_cached(
        team=team,
        year=year,
        event=event,
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
    return [team_event.to_dict() for team_event in team_events]
