from typing import Any, Dict, List, Optional, Tuple

from fastapi import APIRouter, Response

from src.site.aggregation import (
    get_event,
    get_match,
    get_noteworthy_matches,
    get_team_events,
    get_team_matches,
    get_upcoming_matches,
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
async def read_upcoming_matches(
    response: Response,
    country: Optional[str] = None,
    state: Optional[str] = None,
    district: Optional[str] = None,
    playoff: Optional[str] = None,
    minutes: int = -1,
    limit: int = 100,
    metric: str = "predicted_time",
) -> List[Dict[str, Any]]:
    upcoming_matches: List[Tuple[APIMatch, str, Dict[int, float]]] = []
    upcoming_matches = await get_upcoming_matches(
        country=country,
        state=state,
        district=district,
        playoff={None: None, "quals": False, "elims": True}[playoff],
        minutes=minutes,
        limit=limit,
        metric=metric,
    )

    return [
        {
            "match": match.to_dict(),
            "event_name": event_name,
            "team_matches": team_matches,
        }
        for (match, event_name, team_matches) in upcoming_matches
    ]


@router.get("/noteworthy_matches/{year}")
@async_fail_gracefully
async def read_noteworthy_matches(
    response: Response,
    year: int,
    country: Optional[str] = None,
    state: Optional[str] = None,
    district: Optional[str] = None,
    playoff: Optional[str] = None,
    week: Optional[int] = None,
) -> Dict[str, List[Any]]:
    noteworthy_matches: Dict[str, List[APIMatch]] = {}
    noteworthy_matches = await get_noteworthy_matches(
        year=year,
        country=country,
        state=state,
        district=district,
        playoff={None: None, "quals": False, "elims": True}[playoff],
        week=week,
    )

    return {k: [x.to_dict() for x in v] for k, v in noteworthy_matches.items()}
