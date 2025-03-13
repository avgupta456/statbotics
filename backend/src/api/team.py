from datetime import timedelta
from typing import Any, Dict, List, Optional, Tuple

from fastapi import APIRouter, Response

from src.api.query import (
    active_query,
    ascending_query,
    country_query,
    district_query,
    limit_query,
    metric_query,
    offset_query,
    state_query,
)
from src.db.models import Team
from src.db.read import get_team, get_teams
from src.utils.alru_cache import alru_cache
from src.utils.decorators import (
    async_fail_gracefully_plural,
    async_fail_gracefully_singular,
)

router = APIRouter()


@router.get("/")
async def read_root_team():
    return {"name": "Team V3 Router"}


@alru_cache(ttl=timedelta(minutes=2))
async def get_team_cached(
    team: int, no_cache: bool = False
) -> Tuple[bool, Optional[Team]]:
    return (True, get_team(team=team))


@alru_cache(ttl=timedelta(minutes=2))
async def get_teams_cached(
    country: Optional[str] = None,
    state: Optional[str] = None,
    district: Optional[str] = None,
    active: Optional[bool] = None,
    metric: Optional[str] = None,
    ascending: Optional[bool] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
    site: bool = False,
    no_cache: bool = False,
) -> Tuple[bool, List[Team]]:
    if not site:
        limit = min(limit or 1000, 1000)

    return (
        True,
        get_teams(
            country=country,
            state=state,
            district=district,
            active=active,
            metric=metric,
            ascending=ascending,
            limit=limit,
            offset=offset,
        ),
    )


@router.get(
    "/team/{team}",
    summary="Query a single team",
    description="Returns a single Team object. Requires a team number (no prefix).",
)
@async_fail_gracefully_singular
async def read_team(
    response: Response,
    team: int,
) -> Dict[str, Any]:
    team_obj: Optional[Team] = await get_team_cached(team=team)
    if team_obj is None:
        raise Exception("Team not found")

    return team_obj.to_dict()


@router.get(
    "/teams",
    summary="Query multiple teams",
    description="Returns up to 1000 teams at a time. Specify limit and offset to page through results.",
)
@async_fail_gracefully_plural
async def read_teams(
    response: Response,
    country: Optional[str] = country_query,
    state: Optional[str] = state_query,
    district: Optional[str] = district_query,
    active: Optional[bool] = active_query,
    metric: str = metric_query,
    ascending: bool = ascending_query,
    limit: int = limit_query,
    offset: int = offset_query,
) -> List[Dict[str, Any]]:
    teams: List[Team] = await get_teams_cached(
        country=country,
        state=state,
        district=district,
        active=active,
        metric=metric,
        ascending=ascending,
        limit=limit,
        offset=offset,
    )
    return [team.to_dict() for team in teams]
