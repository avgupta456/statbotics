from typing import Any, Dict, List, Optional

from fastapi import APIRouter
from fastapi.responses import Response

from src.api import (
    get_event_cached,
    get_events_cached,
    get_matches_cached,
    get_team_events_cached,
    get_team_year_cached,
    get_year_cached,
)
from src.db.models import Event, Match, TeamEvent, Year

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


def _build_team_matches_from_matches(matches: List[Match]) -> List[Dict[str, Any]]:
    """Build per-team match entries from Match.team_epas for event/match page responses."""
    team_matches = []
    for match in matches:
        if not match.team_epas:
            continue
        red_teams = set(match.get_red())
        for team_str, epa_data in match.team_epas.items():
            team_num = int(team_str)
            alliance = "red" if team_num in red_teams else "blue"
            team_matches.append(
                {
                    "match": match.key,
                    "event": match.event,
                    "team": team_num,
                    "alliance": alliance,
                    "time": match.time,
                    "week": match.week,
                    "elim": match.elim,
                    "status": match.status,
                    **epa_data,
                }
            )
    return team_matches


def _read_event(
    year_obj: Year,
    event: Event,
    matches: List[Match],
    team_events: List[TeamEvent],
) -> Dict[str, Any]:
    matches = sorted(matches, key=lambda x: x.time)
    team_matches = _build_team_matches_from_matches(matches)

    return {
        "event": event.to_dict(),
        "matches": [x.to_dict() for x in matches],
        "team_events": [x.to_dict() for x in team_events],
        "team_matches": team_matches,
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

    return _read_event(year, event, matches, team_events)


@router.get("/event/{event_id}/team_matches/{team}")
@async_fail_gracefully_plural
async def read_team_matches(
    response: Response, event_id: str, team: int, no_cache: bool = False
) -> Any:
    year = int(event_id[:4])
    team_year = await get_team_year_cached(team=team, year=year, no_cache=no_cache)
    if team_year is None:
        return []

    team_matches = sorted(
        [tm for tm in (team_year.team_matches or []) if tm["event"] == event_id],
        key=lambda x: x["time"],
    )
    return [{"team": team, **tm} for tm in team_matches]
