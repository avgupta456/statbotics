from typing import Any, Dict, List, Optional

from fastapi import APIRouter
from fastapi.responses import Response

from src.api import (
    get_event_cached,
    get_events_cached,
    get_matches_cached,
    get_team_events_cached,
    get_team_matches_cached,
    get_year_cached,
)
from src.db.models import Event, Match, TeamEvent, TeamMatch, Year

# from src.site.helper import compress
from src.types.enums import EventStatus
from src.utils.decorators import (
    async_fail_gracefully_plural,
    async_fail_gracefully_singular,
)

router = APIRouter()


def _read_all_events(events: List[Event]) -> List[Dict[str, Any]]:
    return [{"key": x.key, "name": x.name} for x in events]


@router.get("/events/all")
@async_fail_gracefully_plural
async def read_all_events(response: Response, no_cache: bool = False) -> Any:
    events: List[Event] = await get_events_cached(no_cache=no_cache, site=True)
    return _read_all_events(events)


def _read_events(year_obj: Year, events: List[Event]) -> Dict[str, Any]:
    events = sorted(events, key=lambda x: x.time)
    return {
        "year": year_obj.to_dict(),
        "events": [x.to_dict() for x in events if x.status != EventStatus.INVALID],
    }


@router.get("/events/{year}")
@async_fail_gracefully_plural
async def read_events(response: Response, year: int, no_cache: bool = False) -> Any:
    year_obj: Optional[Year] = await get_year_cached(year=year, no_cache=no_cache)
    if year_obj is None:
        raise Exception("Year not found")

    events: List[Event] = await get_events_cached(year=year, no_cache=no_cache)
    return _read_events(year_obj, events)


def _read_event(
    year_obj: Year,
    event: Event,
    matches: List[Match],
    team_events: List[TeamEvent],
    team_matches: List[TeamMatch],
) -> Dict[str, Any]:
    team_matches = sorted(team_matches, key=lambda x: x.time)
    matches = sorted(matches, key=lambda x: x.time)

    return {
        "event": event.to_dict(),
        "matches": [x.to_dict() for x in matches],
        "team_events": [x.to_dict() for x in team_events],
        "team_matches": [x.to_dict() for x in team_matches],
        "year": year_obj.to_dict(),
    }


@router.get("/event/{event_id}")
@async_fail_gracefully_singular
async def read_event(response: Response, event_id: str, no_cache: bool = False) -> Any:
    event: Optional[Event] = await get_event_cached(event=event_id, no_cache=no_cache)
    if event is None:
        raise Exception("Event not found")

    year: Optional[Year] = await get_year_cached(year=event.year, no_cache=no_cache)
    if year is None:
        raise Exception("Year not found")

    team_events: List[TeamEvent] = await get_team_events_cached(
        year=year.year, event=event_id, no_cache=no_cache
    )
    matches: List[Match] = await get_matches_cached(event=event_id, no_cache=no_cache)
    team_matches: List[TeamMatch] = await get_team_matches_cached(
        event=event_id, no_cache=no_cache
    )

    return _read_event(year, event, matches, team_events, team_matches)


@router.get("/event/{event_id}/team_matches/{team}")
@async_fail_gracefully_plural
async def read_team_matches(
    response: Response, event_id: str, team: int, no_cache: bool = False
) -> Any:
    team_matches: List[TeamMatch] = await get_team_matches_cached(
        event=event_id, team=team, no_cache=no_cache
    )
    out = [x.to_dict() for x in sorted(team_matches, key=lambda x: x.time)]
    return out
