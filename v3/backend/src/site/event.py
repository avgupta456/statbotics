from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Response

from src.site.aggregation import (
    get_event,
    get_events,
    get_matches,
    get_team_events,
    get_team_matches,
    get_year,
)
from src.site.hypo_event import read_hypothetical_event as _read_hypothetical_event
from src.site.models import APIEvent, APIMatch, APITeamEvent, APITeamMatch, APIYear
from src.utils.decorators import async_fail_gracefully

router = APIRouter()


@router.get("/events/all")
@async_fail_gracefully
async def read_all_events(
    response: Response, no_cache: bool = False
) -> List[Dict[str, Any]]:
    events: List[APIEvent] = await get_events(no_cache=no_cache)
    return [{"key": event.key, "name": event.name} for event in events]


@router.get("/events/{year}")
@async_fail_gracefully
async def read_events(
    response: Response, year: int, no_cache: bool = False
) -> Dict[str, Any]:
    year_obj: Optional[APIYear] = await get_year(year=year, no_cache=no_cache)
    if year_obj is None:
        raise Exception("Year not found")

    events: List[APIEvent] = await get_events(
        year=year, offseason=None, no_cache=no_cache
    )
    return {"year": year_obj.to_dict(), "events": [x.to_dict() for x in events]}


@router.get("/event/{event_id}")
@async_fail_gracefully
async def read_event(
    response: Response, event_id: str, no_cache: bool = False
) -> Dict[str, Any]:
    event: Optional[APIEvent] = await get_event(event=event_id, no_cache=no_cache)
    if event is None:
        raise Exception("Event not found")

    year: Optional[APIYear] = await get_year(year=event.year, no_cache=no_cache)
    if year is None:
        raise Exception("Year not found")

    team_events: List[APITeamEvent] = await get_team_events(
        year=year.year,
        score_mean=year.score_mean / (1 + year.foul_rate),
        score_sd=year.score_sd,
        event=event_id,
        offseason=event.offseason,
        no_cache=no_cache,
    )
    matches: List[APIMatch] = await get_matches(
        event=event_id, offseason=event.offseason, no_cache=no_cache
    )
    team_matches: List[APITeamMatch] = await get_team_matches(
        event=event_id, offseason=event.offseason, no_cache=no_cache
    )

    out = {
        "event": event.to_dict(),
        "matches": [x.to_dict() for x in matches],
        "team_events": [x.to_dict() for x in team_events],
        "team_matches": [x.to_dict() for x in team_matches],
        "year": year.to_dict(),
    }

    return out


@router.get("/event/{event_id}/team_matches/{team}")
@async_fail_gracefully
async def read_team_matches(
    response: Response, event_id: str, team: str, no_cache: bool = False
) -> List[Dict[str, Any]]:
    team_matches: List[APITeamMatch] = await get_team_matches(
        event=event_id, team=team, no_cache=no_cache
    )
    return [x.to_dict() for x in team_matches]


@router.get("/event/hypothetical/{event_id}")
@async_fail_gracefully
async def read_hypothetical_event(
    response: Response, event_id: str, no_cache: bool = False
) -> Dict[str, Any]:
    return await _read_hypothetical_event(event_id, no_cache=no_cache)
