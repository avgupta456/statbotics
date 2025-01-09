from datetime import timedelta
from typing import Any, Dict, List, Optional, Tuple

from fastapi import APIRouter, Response

from src.api.query import (
    ascending_query,
    elim_query,
    event_query,
    limit_query,
    metric_query,
    offset_query,
    team_query,
    week_query,
    year_query,
)
from src.db.models import Match
from src.db.read import get_match, get_matches
from src.utils.alru_cache import alru_cache
from src.utils.decorators import (
    async_fail_gracefully_plural,
    async_fail_gracefully_singular,
)

router = APIRouter()


@router.get("/")
async def read_root_match():
    return {"name": "Match V3 Router"}


@alru_cache(ttl=timedelta(minutes=2))
async def get_match_cached(
    match: str, no_cache: bool = False
) -> Tuple[bool, Optional[Match]]:
    return (True, get_match(match=match))


@alru_cache(ttl=timedelta(minutes=2))
async def get_matches_cached(
    team: Optional[int] = None,
    year: Optional[int] = None,
    event: Optional[str] = None,
    week: Optional[int] = None,
    elim: Optional[bool] = None,
    metric: Optional[str] = None,
    ascending: Optional[bool] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
    site: bool = False,
    no_cache: bool = False,
) -> Tuple[bool, List[Match]]:
    if not site:
        limit = min(limit or 1000, 1000)

    return (
        True,
        get_matches(
            team=team,
            year=year,
            event=event,
            week=week,
            elim=elim,
            metric=metric,
            ascending=ascending,
            limit=limit,
            offset=offset,
        ),
    )


@router.get(
    "/match/{match}",
    summary="Query a single match",
    description="Returns a single Match object. Requires a match key, e.g. `2019ncwak_f1m1`.",
)
@async_fail_gracefully_singular
async def read_match(response: Response, match: str) -> Dict[str, Any]:
    match_obj: Optional[Match] = await get_match_cached(match=match)
    if match_obj is None:
        raise Exception("Match not found")

    return match_obj.to_dict()


@router.get(
    "/matches",
    summary="Query multiple matches",
    description="Returns up to 1000 matches at a time. Specify limit and offset to page through results.",
)
@async_fail_gracefully_plural
async def read_matches(
    response: Response,
    team: Optional[int] = team_query,
    year: Optional[int] = year_query,
    event: Optional[str] = event_query,
    week: Optional[int] = week_query,
    elim: Optional[bool] = elim_query,
    metric: Optional[str] = metric_query,
    ascending: Optional[bool] = ascending_query,
    limit: Optional[int] = limit_query,
    offset: Optional[int] = offset_query,
) -> List[Dict[str, Any]]:
    matches: List[Match] = await get_matches_cached(
        team=team,
        year=year,
        event=event,
        week=week,
        elim=elim,
        metric=metric,
        ascending=ascending,
        limit=limit,
        offset=offset,
    )
    return [match.to_dict() for match in matches]
