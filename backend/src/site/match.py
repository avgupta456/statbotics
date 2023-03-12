from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Response

from src.site.aggregation import (
    get_event,
    get_match,
    get_upcoming_matches,
    get_team_events,
    get_team_matches,
    get_year,
)
from src.site.models import APIEvent, APIMatch, APITeamEvent, APITeamMatch, APIYear
from src.utils.decorators import async_fail_gracefully

router = APIRouter()


@router.get("/match/{match_id}")
@async_fail_gracefully
async def read_match(response: Response, match_id: str) -> Dict[str, Any]:
    match: Optional[APIMatch] = await get_match(match=match_id)
    if match is None:
        raise Exception("Match not found")

    event: Optional[APIEvent] = await get_event(event=match.event)
    if event is None:
        raise Exception("Event not found")

    year: Optional[APIYear] = await get_year(year=match.year)
    if year is None:
        raise Exception("Year not found")

    team_matches: List[APITeamMatch] = await get_team_matches(match=match_id)
    team_nums = [x.num for x in team_matches]

    team_events: List[APITeamEvent] = await get_team_events(
        year=year.year,
        score_mean=year.score_mean,
        score_sd=year.score_sd,
        event=match.event,
    )
    team_events = [x for x in team_events if x.num in team_nums]

    out = {
        "year": year.to_dict(),
        "event": event.to_dict(),
        "team_events": [x.to_dict() for x in team_events],
        "match": match.to_dict(),
        "team_matches": [x.to_dict() for x in team_matches],
    }

    return out


@router.get("/upcoming_matches")
@async_fail_gracefully
async def read_upcoming_matches(response: Response) -> List[Dict[str, Any]]:
    matches: List[APIMatch] = await get_upcoming_matches()
    return [x.to_dict() for x in matches]
