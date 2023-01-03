from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Response

from src.api.aggregation.year import get_year
from src.api.aggregation.match import get_matches
from src.api.aggregation.event import get_event
from src.api.aggregation.team_event import get_team_events
from src.api.aggregation.team_match import get_team_matches
from src.api.models.event import APIEvent
from src.api.models.team_event import APITeamEvent
from src.api.models.team_match import APITeamMatch
from src.api.models.match import APIMatch
from src.api.models.year import APIYear
from src.data.nepa import get_epa_to_norm_epa_func
from src.utils.decorators import async_fail_gracefully

router = APIRouter()


@router.get("/")
async def read_root():
    return {"name": "Event Router"}


@router.get("/event/{event_id}")
@async_fail_gracefully
async def read_event(response: Response, event_id: str) -> Dict[str, Any]:
    event: Optional[APIEvent] = await get_event(event=event_id)
    if event is None:
        raise Exception("Event not found")

    year: Optional[APIYear] = await get_year(year=event.year)
    if year is None:
        raise Exception("Year not found")

    epa_to_norm_epa = get_epa_to_norm_epa_func(event.year)
    team_events: List[APITeamEvent] = await get_team_events(
        event=event_id, epa_to_norm_epa=epa_to_norm_epa
    )
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
