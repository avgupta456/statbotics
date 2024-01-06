from datetime import timedelta
from typing import Any, Dict, List, Optional, Tuple

from fastapi import APIRouter, Response

from src.api.query import (
    alliance_query,
    ascending_query,
    elim_query,
    event_query,
    limit_query,
    match_query,
    metric_query,
    offseason_query,
    offset_query,
    team_query,
    week_query,
    year_query,
)
from src.db.models import Alliance
from src.db.read import get_alliance, get_alliances
from src.utils.alru_cache import alru_cache
from src.utils.decorators import (
    async_fail_gracefully_plural,
    async_fail_gracefully_singular,
)

router = APIRouter()


@router.get("/")
async def read_root_alliance():
    return {"name": "Alliance Router"}


@alru_cache(ttl=timedelta(minutes=5))
async def get_alliance_cached(
    match: str, alliance: str
) -> Tuple[bool, Optional[Alliance]]:
    return (True, get_alliance(match=match, alliance=alliance))


@alru_cache(ttl=timedelta(minutes=5))
async def get_alliances_cached(
    team: Optional[str] = None,
    year: Optional[int] = None,
    event: Optional[str] = None,
    week: Optional[int] = None,
    match: Optional[str] = None,
    alliance: Optional[str] = None,
    elim: Optional[bool] = None,
    offseason: Optional[bool] = None,
    metric: Optional[str] = None,
    ascending: Optional[bool] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> Tuple[bool, List[Alliance]]:
    return (
        True,
        get_alliances(
            team=team,
            year=year,
            event=event,
            week=week,
            match=match,
            alliance=alliance,
            elim=elim,
            offseason=offseason,
            metric=metric,
            ascending=ascending,
            limit=limit,
            offset=offset,
        ),
    )


@router.get(
    "/alliance/{match}/{alliance}",
    summary="Query a single alliance",
    description="Returns a single Alliance object. Requires a match key and alliance color, e.g. `2019ncwak_f1m1` and `red`.",
)
@async_fail_gracefully_singular
async def read_alliance(
    response: Response, match: str, alliance: str
) -> Dict[str, Any]:
    alliance_obj: Optional[Alliance] = await get_alliance_cached(
        match=match, alliance=alliance
    )
    if alliance_obj is None:
        raise Exception("Alliance not found")

    return alliance_obj.to_dict()


@router.get(
    "/alliances",
    summary="Query multiple alliances",
    description="Returns up to 1000 alliances at a time. Specify limit and offset to page through results.",
)
@async_fail_gracefully_plural
async def read_alliances(
    response: Response,
    team: Optional[str] = team_query,
    year: Optional[int] = year_query,
    event: Optional[str] = event_query,
    week: Optional[int] = week_query,
    match: Optional[str] = match_query,
    alliance: Optional[str] = alliance_query,
    elim: Optional[bool] = elim_query,
    offseason: Optional[bool] = offseason_query,
    metric: Optional[str] = metric_query,
    ascending: Optional[bool] = ascending_query,
    limit: Optional[int] = limit_query,
    offset: Optional[int] = offset_query,
) -> List[Dict[str, Any]]:
    alliances = await get_alliances_cached(
        team=team,
        year=year,
        event=event,
        week=week,
        match=match,
        alliance=alliance,
        elim=elim,
        offseason=offseason,
        metric=metric,
        ascending=ascending,
        limit=limit,
        offset=offset,
    )
    return [alliance.to_dict() for alliance in alliances]
