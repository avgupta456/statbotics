from datetime import timedelta
from typing import Any, Dict, List, Optional, Tuple

from fastapi import APIRouter, Response

from src.api.query import (
    ascending_query,
    country_query,
    district_query,
    limit_query,
    metric_query,
    offseason_query,
    offset_query,
    state_query,
    team_query,
    year_query,
)
from src.db.models import TeamYear
from src.db.read import get_team_year, get_team_years
from src.utils.alru_cache import alru_cache
from src.utils.decorators import (
    async_fail_gracefully_api_plural,
    async_fail_gracefully_api_singular,
)

router = APIRouter()


@router.get("/")
async def read_root_team_year():
    return {"name": "Team Year Router"}


@alru_cache(ttl=timedelta(minutes=5))
async def get_team_year_cached(team: str, year: int) -> Tuple[bool, Optional[TeamYear]]:
    return (True, get_team_year(team=team, year=year))


@alru_cache(ttl=timedelta(minutes=5))
async def get_team_years_cached(
    team: Optional[str] = None,
    year: Optional[int] = None,
    country: Optional[str] = None,
    district: Optional[str] = None,
    state: Optional[str] = None,
    offseason: Optional[bool] = None,
    metric: Optional[str] = None,
    ascending: Optional[bool] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> Tuple[bool, List[TeamYear]]:
    return (
        True,
        get_team_years(
            team=team,
            year=year,
            country=country,
            district=district,
            state=state,
            offseason=offseason,
            metric=metric,
            ascending=ascending,
            limit=limit,
            offset=offset,
        ),
    )


@router.get(
    "/team_year/{team}/{year}",
    summary="Query a single team year",
    description="Returns a single Team Year object. Requires a team number and year.",
)
@async_fail_gracefully_api_singular
async def read_team_year(
    response: Response,
    team: str,
    year: int,
) -> Dict[str, Any]:
    team_year_obj: Optional[TeamYear] = await get_team_year_cached(team=team, year=year)
    if team_year_obj is None:
        raise Exception("TeamYear not found")

    return team_year_obj.to_dict()


@router.get(
    "/team_years",
    summary="Query multiple team years",
    description="Returns up to 1000 team years at a time. Specify limit and offset to page through results.",
)
@async_fail_gracefully_api_plural
async def read_team_years(
    response: Response,
    team: Optional[str] = team_query,
    year: Optional[int] = year_query,
    country: Optional[str] = country_query,
    district: Optional[str] = district_query,
    state: Optional[str] = state_query,
    offseason: Optional[bool] = offseason_query,
    metric: Optional[str] = metric_query,
    ascending: Optional[bool] = ascending_query,
    limit: Optional[int] = limit_query,
    offset: Optional[int] = offset_query,
) -> List[Dict[str, Any]]:
    team_years: List[TeamYear] = await get_team_years_cached(
        team=team,
        year=year,
        country=country,
        district=district,
        state=state,
        offseason=offseason,
        metric=metric,
        ascending=ascending,
        limit=limit,
        offset=offset,
    )
    return [team_year.to_dict() for team_year in team_years]
