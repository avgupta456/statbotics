from datetime import timedelta
from typing import Any, Dict, List, Optional, Tuple

from fastapi import APIRouter, Response

from src.api.query import (
    ascending_query,
    elim_query,
    event_query,
    limit_query,
    match_query,
    metric_query,
    offset_query,
    team_query,
    week_query,
    year_query,
)
from src.db.models import TeamMatch
from src.db.read import get_team_match, get_team_matches
from src.utils.alru_cache import alru_cache
from src.utils.decorators import (
    async_fail_gracefully_plural,
    async_fail_gracefully_singular,
)

router = APIRouter()


@router.get("/")
async def read_root_team_match():
    return {"name": "Team Match V3 Router"}


@alru_cache(ttl=timedelta(minutes=2))
async def get_team_match_cached(
    team: int, match: str, no_cache: bool = False
) -> Tuple[bool, Optional[TeamMatch]]:
    return (True, get_team_match(team=team, match=match))


@alru_cache(ttl=timedelta(minutes=2))
async def get_team_matches_cached(
    team: Optional[int] = None,
    year: Optional[int] = None,
    event: Optional[str] = None,
    week: Optional[int] = None,
    match: Optional[str] = None,
    elim: Optional[bool] = None,
    metric: Optional[str] = None,
    ascending: Optional[bool] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
    site: bool = False,
    no_cache: bool = False,
) -> Tuple[bool, List[TeamMatch]]:
    if not site:
        limit = min(limit or 1000, 1000)

    return (
        True,
        get_team_matches(
            team=team,
            year=year,
            event=event,
            week=week,
            match=match,
            elim=elim,
            metric=metric,
            ascending=ascending,
            limit=limit,
            offset=offset,
        ),
    )


@router.get(
    "/team_match/{team}/{match}",
    summary="Query a single team match",
    description="Returns a single Team Match object. Requires a team number and match key, e.g. `5511` and `2019ncwak_f1m1`.",
)
@async_fail_gracefully_singular
async def read_team_match(response: Response, team: int, match: str) -> Dict[str, Any]:
    team_match_obj: Optional[TeamMatch] = await get_team_match_cached(
        team=team, match=match
    )
    if team_match_obj is None:
        raise Exception("Team Match not found")

    return team_match_obj.to_dict()


@router.get(
    "/team_matches",
    summary="Query multiple team matches",
    description="Returns up to 1000 team matches at a time. Specify limit and offset to page through results.",
)
@async_fail_gracefully_plural
async def read_team_matches(
    response: Response,
    team: Optional[int] = team_query,
    year: Optional[int] = year_query,
    event: Optional[str] = event_query,
    week: Optional[int] = week_query,
    match: Optional[str] = match_query,
    elim: Optional[bool] = elim_query,
    metric: Optional[str] = metric_query,
    ascending: Optional[bool] = ascending_query,
    limit: Optional[int] = limit_query,
    offset: Optional[int] = offset_query,
) -> List[Dict[str, Any]]:
    team_matches: List[TeamMatch] = await get_team_matches_cached(
        team=team,
        year=year,
        event=event,
        week=week,
        match=match,
        elim=elim,
        metric=metric,
        ascending=ascending,
        limit=limit,
        offset=offset,
    )
    return [team_match.to_dict() for team_match in team_matches]
