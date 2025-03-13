from datetime import timedelta
from typing import Any, Dict, List, Optional, Tuple

from fastapi import APIRouter, Response

from src.api.query import ascending_query, limit_query, metric_query, offset_query
from src.db.models import Year
from src.db.read import get_year, get_years
from src.utils.alru_cache import alru_cache
from src.utils.decorators import (
    async_fail_gracefully_plural,
    async_fail_gracefully_singular,
)

router = APIRouter()


@router.get("/")
async def read_root_year():
    return {"name": "Year V3 Router"}


@alru_cache(ttl=timedelta(minutes=2))
async def get_year_cached(
    year: int, no_cache: bool = False
) -> Tuple[bool, Optional[Year]]:
    return (True, get_year(year=year))


@alru_cache(ttl=timedelta(minutes=2))
async def get_years_cached(
    metric: Optional[str] = None,
    ascending: Optional[bool] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
    site: bool = False,
    no_cache: bool = False,
) -> Tuple[bool, List[Year]]:
    if not site:
        limit = min(limit or 1000, 1000)

    return (
        True,
        get_years(metric=metric, ascending=ascending, limit=limit, offset=offset),
    )


@router.get(
    "/year/{year}",
    summary="Query a single year",
    description="Returns a single Year object. Requires a four-digit year, e.g. `2019`.",
)
@async_fail_gracefully_singular
async def read_year(
    response: Response,
    year: int,
) -> Dict[str, Any]:
    year_obj: Optional[Year] = await get_year_cached(year=year)
    if year_obj is None:
        raise Exception("Year not found")

    return year_obj.to_dict()


@router.get(
    "/years",
    summary="Query multiple years",
    response_description="Returns a list of Years since 2002. Older data is not available.",
)
@async_fail_gracefully_plural
async def read_years(
    response: Response,
    metric: Optional[str] = metric_query,
    ascending: Optional[bool] = ascending_query,
    limit: Optional[int] = limit_query,
    offset: Optional[int] = offset_query,
) -> List[Dict[str, Any]]:
    years: List[Year] = await get_years_cached(
        metric=metric, ascending=ascending, limit=limit, offset=offset
    )
    return [year.to_dict() for year in years]
