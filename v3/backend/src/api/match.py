from datetime import timedelta
from typing import Any, Dict, List, Optional, Tuple

from fastapi import APIRouter, Response

from src.db.models import Match
from src.db.read import get_match, get_matches
from src.utils.alru_cache import alru_cache
from src.utils.decorators import (
    async_fail_gracefully_api_plural,
    async_fail_gracefully_api_singular,
)

router = APIRouter()


@router.get("/")
async def read_root():
    return {"name": "Match Router"}


@alru_cache(ttl=timedelta(hours=1))
async def get_match_cached(match: str) -> Tuple[bool, Optional[Match]]:
    return (True, get_match(match=match))


@alru_cache(ttl=timedelta(hours=1))
async def get_matches_cached(
    team: Optional[str] = None,
    year: Optional[int] = None,
    event: Optional[str] = None,
    week: Optional[int] = None,
    elim: Optional[bool] = None,
    offseason: Optional[bool] = False,
    metric: Optional[str] = None,
    ascending: Optional[bool] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> Tuple[bool, List[Match]]:
    return (
        True,
        get_matches(
            team=team,
            year=year,
            event=event,
            week=week,
            elim=elim,
            offseason=offseason,
            metric=metric,
            ascending=ascending,
            limit=limit,
            offset=offset,
        ),
    )


@router.get(
    "/match/{match}",
    description="Get a single Match object containing teams, score prediction, and actual results. Specify match key ex: 2019ncwak_f1m1",
    response_description="A Match object.",
)
@async_fail_gracefully_api_singular
async def read_match(response: Response, match: str) -> Dict[str, Any]:
    match_obj: Optional[Match] = await get_match_cached(match=match)
    if match_obj is None:
        raise Exception("Match not found")

    return match_obj.to_dict()


@router.get(
    "/matches/event/{event}",
    description="Get a list of Match objects for a single event. Specify event key ex: 2019ncwak, 2022cmptx",
    response_description="A list of Match objects. See /match/{match} for more information.",
)
@async_fail_gracefully_api_plural
async def read_matches_event(response: Response, event: str) -> List[Dict[str, Any]]:
    matches: List[Match] = await get_matches_cached(event=event)
    return [match.to_dict() for match in matches]


@router.get(
    "/matches/team/{team}/year/{year}",
    description="Get a list of Match objects for a single team in a single year. Specify team number and year, ex: 254, 2019",
    response_description="A list of Match objects. See /match/{match} for more information.",
)
@async_fail_gracefully_api_plural
async def read_matches_team_year(
    response: Response, team: int, year: int
) -> List[Dict[str, Any]]:
    matches: List[Match] = await get_matches_cached(team=team, year=year)
    return [match.to_dict() for match in matches]


@router.get(
    "/matches/team/{team}/event/{event}",
    description="Get a list of Match objects for a single team in a single event. Specify team number and event key, ex: 5511, 2019ncwak",
    response_description="A list of Match objects. See /match/{match} for more information.",
)
@async_fail_gracefully_api_plural
async def read_matches_team_event(
    response: Response, team: int, event: str
) -> List[Dict[str, Any]]:
    matches: List[Match] = await get_matches_cached(team=team, event=event)
    return [match.to_dict() for match in matches]


@router.get(
    "/matches",
    description="Get a list of Matches with optional filters",
    response_description="A list of Match objects. See /match/{match} for more information.",
)
@async_fail_gracefully_api_plural
async def read_matches(
    response: Response,
    team: Optional[str] = None,
    year: Optional[int] = None,
    event: Optional[str] = None,
    week: Optional[int] = None,
    elim: Optional[bool] = None,
    offseason: Optional[bool] = False,
    metric: Optional[str] = None,
    ascending: Optional[bool] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> List[Dict[str, Any]]:
    matches: List[Match] = await get_matches_cached(
        team=team,
        year=year,
        event=event,
        week=week,
        elim=elim,
        offseason=offseason,
        metric=metric,
        ascending=ascending,
        limit=limit,
        offset=offset,
    )
    return [match.to_dict() for match in matches]
