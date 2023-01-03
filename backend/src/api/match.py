from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Response

from src.api.aggregation import get_year, get_event, get_match, get_team_matches
from src.api.models import APIMatch, APITeamMatch, APIEvent, APIYear
from src.utils.decorators import async_fail_gracefully

router = APIRouter()


@router.get("/")
async def read_root():
    return {"name": "Match Router"}


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

    out = {
        "match": match.to_dict(),
        "event": event.to_dict(),
        "year": year.to_dict(),
        "team_matches": [x.to_dict() for x in team_matches],
    }

    return out
