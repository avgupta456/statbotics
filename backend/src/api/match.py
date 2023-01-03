from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Response

from src.api.aggregation.year import get_year
from src.api.aggregation.event import get_event
from src.api.aggregation.match import get_match
from src.api.aggregation.team_match import get_team_matches
from src.api.models.match import APIMatch
from src.api.models.team_match import APITeamMatch
from src.api.models.event import APIEvent
from src.api.models.year import APIYear
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
