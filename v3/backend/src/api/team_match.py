from datetime import timedelta
from typing import Any, Dict, List, Optional, Tuple

from fastapi import APIRouter, Response

from src.db.models import TeamMatch
from src.db.read import get_team_match, get_team_matches
from src.utils.alru_cache import alru_cache
from src.utils.decorators import (
    async_fail_gracefully_api_plural,
    async_fail_gracefully_api_singular,
)

router = APIRouter()


@router.get("/")
async def read_root():
    return {"name": "Team Match Router"}


@alru_cache(ttl=timedelta(hours=1))
async def get_team_match_cached(
    team: str, match: str
) -> Tuple[bool, Optional[TeamMatch]]:
    return (True, get_team_match(team=team, match=match))


@alru_cache(ttl=timedelta(hours=1))
async def get_team_matches_cached(
    team: Optional[str] = None,
    year: Optional[int] = None,
    event: Optional[str] = None,
    week: Optional[int] = None,
    match: Optional[str] = None,
    elim: Optional[bool] = None,
    offseason: Optional[bool] = False,
    metric: Optional[str] = None,
    ascending: Optional[bool] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> Tuple[bool, List[TeamMatch]]:
    return (
        True,
        get_team_matches(
            team=team,
            year=year,
            event=event,
            week=week,
            match=match,
            elim=elim,
            offseason=offseason,
            metric=metric,
            ascending=ascending,
            limit=limit,
            offset=offset,
        ),
    )


@router.get(
    "/team_match/{team}/{match}",
    description="Get a single Team Match object containing team and EPA predictions. Specify team number and match key ex: 5511, 2019ncwak_f1m1",
    response_description="A Team Match object.",
)
@async_fail_gracefully_api_singular
async def read_team_match(response: Response, team: str, match: str) -> Dict[str, Any]:
    team_match_obj: Optional[TeamMatch] = await get_team_match_cached(
        team=team, match=match
    )
    if team_match_obj is None:
        raise Exception("Team Match not found")

    return team_match_obj.to_dict()


@router.get(
    "/team_matches/team/{team}/year/{year}",
    description="Get a list of Team Match objects for a single team and year. Specify team number and year ex: 5511, 2019. Note, includes offseason events.",
    response_description="A list of Team Match objects. See /team_match/{team}/{match} for more information.",
)
@async_fail_gracefully_api_plural
async def read_team_matches_team_year(
    response: Response, team: str, year: int
) -> List[Dict[str, Any]]:
    team_matches: List[TeamMatch] = await get_team_matches_cached(team=team, year=year)
    return [team_match.to_dict() for team_match in team_matches]


@router.get(
    "/team_matches/team/{team}/event/{event}",
    description="Get a list of Team Match objects for a single team and event. Specify team number and event key ex: 5511, 2019ncwak",
    response_description="A list of Team Match objects. See /team_match/{team}/{match} for more information.",
)
@async_fail_gracefully_api_plural
async def read_team_matches_team_event(
    response: Response, team: str, event: str
) -> List[Dict[str, Any]]:
    team_matches: List[TeamMatch] = await get_team_matches_cached(
        team=team, event=event
    )
    return [team_match.to_dict() for team_match in team_matches]


@router.get(
    "/team_matches/event/{event}",
    description="Get a list of Team Match objects for a single event. Specify event key ex: 2019ncwak",
    response_description="A list of Team Match objects. See /team_match/{team}/{match} for more information.",
)
@async_fail_gracefully_api_plural
async def read_team_matches_event(
    response: Response, event: str
) -> List[Dict[str, Any]]:
    team_matches: List[TeamMatch] = await get_team_matches_cached(event=event)
    return [team_match.to_dict() for team_match in team_matches]


@router.get(
    "/team_matches",
    description="Get a list of Team Match objects with optional filters",
    response_description="A list of Team Match objects. See /team_match/{team}/{match} for more information.",
)
@async_fail_gracefully_api_plural
async def read_team_matches(
    response: Response,
    team: Optional[str] = None,
    year: Optional[int] = None,
    event: Optional[str] = None,
    week: Optional[int] = None,
    match: Optional[str] = None,
    elim: Optional[bool] = None,
    offseason: Optional[bool] = False,
    metric: Optional[str] = None,
    ascending: Optional[bool] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> List[Dict[str, Any]]:
    team_matches: List[TeamMatch] = await get_team_matches_cached(
        team=team,
        year=year,
        event=event,
        week=week,
        match=match,
        elim=elim,
        offseason=offseason,
        metric=metric,
        ascending=ascending,
        limit=limit,
        offset=offset,
    )
    return [team_match.to_dict() for team_match in team_matches]
