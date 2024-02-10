from typing import Any, Optional

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from src.db.functions import get_noteworthy_matches, get_upcoming_matches
from src.site.helper import compress
from src.utils.decorators import (
    async_fail_gracefully_plural,
    async_fail_gracefully_singular,
)

# from src.constants import CURR_YEAR
# from src.site.aggregation import (
# get_event,
# get_match,
# get_noteworthy_matches,
# get_team_events,
# get_team_matches,
# get_upcoming_matches,
# get_year,
# )
# from src.site.models import APIEvent, APIMatch, APITeamEvent, APITeamMatch, APIYear
# from src.utils.decorators import async_fail_gracefully

router = APIRouter()


"""
@router.get("/match/{match_id}")
@async_fail_gracefully
async def read_match(
    response: Response, match_id: str, no_cache: bool = False
) -> Dict[str, Any]:
    match: Optional[APIMatch] = await get_match(match=match_id, no_cache=no_cache)
    if match is None:
        raise Exception("Match not found")

    event: Optional[APIEvent] = await get_event(event=match.event, no_cache=no_cache)
    if event is None:
        raise Exception("Event not found")

    year: Optional[APIYear] = await get_year(year=match.year, no_cache=no_cache)
    if year is None:
        raise Exception("Year not found")

    team_matches: List[APITeamMatch] = await get_team_matches(
        match=match_id, no_cache=no_cache
    )
    team_nums = [x.num for x in team_matches]

    team_events: List[APITeamEvent] = await get_team_events(
        year=year.year,
        score_mean=year.score_mean,
        score_sd=year.score_sd,
        event=match.event,
        no_cache=no_cache,
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
"""


@router.get("/upcoming_matches")
@async_fail_gracefully_plural
async def read_upcoming_matches(
    response: StreamingResponse,
    country: Optional[str] = None,
    state: Optional[str] = None,
    district: Optional[str] = None,
    elim: Optional[str] = None,
    minutes: int = -1,
    limit: int = 100,
    metric: str = "predicted_time",
    no_cache: bool = False,
) -> Any:
    upcoming_matches = get_upcoming_matches(
        country=country,
        state=state,
        district=district,
        elim={None: None, "qual": False, "elim": True}[elim],
        minutes=minutes,
        limit=limit,
        metric=metric,
    )

    data = [{"match": m, "event_name": e} for m, e in upcoming_matches]

    return compress(data)


@router.get("/noteworthy_matches/{year}")
@async_fail_gracefully_singular
async def read_noteworthy_matches(
    response: StreamingResponse,
    year: int,
    country: Optional[str] = None,
    state: Optional[str] = None,
    district: Optional[str] = None,
    elim: Optional[str] = None,
    week: Optional[int] = None,
    no_cache: bool = False,
) -> Any:
    noteworthy_matches = get_noteworthy_matches(
        year=year,
        country=country,
        state=state,
        district=district,
        elim={None: None, "qual": False, "elim": True}[elim],
        week=week,
    )

    data = {k: [x.to_dict() for x in v] for k, v in noteworthy_matches.items()}

    return compress(data)
