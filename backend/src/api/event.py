from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Response

from src.api.aggregation import (
    get_event,
    get_events,
    get_matches,
    get_team_events,
    get_team_matches,
    get_year,
)
from src.api.models import APIEvent, APIMatch, APITeamEvent, APITeamMatch, APIYear
from src.utils.decorators import async_fail_gracefully

router = APIRouter()


@router.get("/")
async def read_root():
    return {"name": "Event Router"}


@router.get("/events/{year}")
@async_fail_gracefully
async def read_events(response: Response, year: int) -> List[Dict[str, Any]]:
    events: List[APIEvent] = await get_events(year=year)
    return [x.to_dict() for x in events]


@router.get("/event/{event_id}")
@async_fail_gracefully
async def read_event(response: Response, event_id: str) -> Dict[str, Any]:
    event: Optional[APIEvent] = await get_event(event=event_id)
    if event is None:
        raise Exception("Event not found")

    year: Optional[APIYear] = await get_year(year=event.year)
    if year is None:
        raise Exception("Year not found")

    team_events: List[APITeamEvent] = await get_team_events(event=event_id)
    matches: List[APIMatch] = await get_matches(event=event_id)
    team_matches: List[APITeamMatch] = await get_team_matches(event=event_id)

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
    response: Response, event_id: str, team: int
) -> List[Dict[str, Any]]:
    team_matches: List[APITeamMatch] = await get_team_matches(event=event_id, team=team)
    return [x.to_dict() for x in team_matches]
