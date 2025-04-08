from typing import Any, Dict, List, Optional, Tuple

from fastapi import APIRouter
from fastapi.responses import Response

from src.api import (
    get_event_cached,
    get_match_cached,
    get_team_events_cached,
    get_team_matches_cached,
    get_year_cached,
)
from src.db.functions import get_noteworthy_matches, get_upcoming_matches
from src.db.models import Event, Match, TeamEvent, TeamMatch, Year

# from src.site.helper import compress
from src.utils.decorators import (
    async_fail_gracefully_plural,
    async_fail_gracefully_singular,
)

router = APIRouter()


@router.get("/match/{match_id}")
@async_fail_gracefully_singular
async def read_match(response: Response, match_id: str, no_cache: bool = False) -> Any:
    match: Optional[Match] = await get_match_cached(match=match_id, no_cache=no_cache)
    if match is None:
        raise Exception("Match not found")

    event: Optional[Event] = await get_event_cached(
        event=match.event, no_cache=no_cache
    )
    if event is None:
        raise Exception("Event not found")

    year: Optional[Year] = await get_year_cached(year=match.year, no_cache=no_cache)
    if year is None:
        raise Exception("Year not found")

    team_matches: List[TeamMatch] = await get_team_matches_cached(
        match=match_id, no_cache=no_cache
    )
    team_nums = [x.team for x in team_matches]

    team_events: List[TeamEvent] = await get_team_events_cached(
        year=year.year, event=match.event, no_cache=no_cache
    )
    team_events = [x for x in team_events if x.team in team_nums]

    out = {
        "year": year.to_dict(),
        "event": event.to_dict(),
        "team_events": [x.to_dict() for x in team_events],
        "match": match.to_dict(),
        "team_matches": [x.to_dict() for x in team_matches],
    }

    return out


def _read_upcoming_matches(
    upcoming_matches: List[Tuple[Match, str]],
) -> List[Dict[str, Any]]:
    return [{"match": m.to_dict(), "event_name": e} for m, e in upcoming_matches]


@router.get("/upcoming_matches")
@async_fail_gracefully_plural
async def read_upcoming_matches(
    response: Response,
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

    return _read_upcoming_matches(upcoming_matches)


def _read_noteworthy_matches(
    noteworthy_matches: Dict[str, List[Match]],
) -> Dict[str, Any]:
    return {k: [x.to_dict() for x in v] for k, v in noteworthy_matches.items()}


@router.get("/noteworthy_matches/{year}")
@async_fail_gracefully_singular
async def read_noteworthy_matches(
    response: Response,
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

    return _read_noteworthy_matches(noteworthy_matches)
