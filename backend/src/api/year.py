from datetime import timedelta
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Response

from src.db.models import Year
from src.db.read import get_year, get_years
from src.utils.alru_cache import alru_cache
from src.utils.decorators import (
    async_fail_gracefully_api_singular,
    async_fail_gracefully_api_plural,
)

router = APIRouter()


@router.get("/")
async def read_root():
    return {"name": "Year Router"}


@alru_cache(ttl=timedelta(hours=1))
async def get_year_cached(year: int) -> Optional[Year]:
    return (True, get_year(year=year))  # type: ignore


@alru_cache(ttl=timedelta(hours=1))
async def get_years_cached(
    metric: Optional[str] = None,
    ascending: Optional[bool] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> List[Year]:
    return (True, get_years(metric=metric, ascending=ascending, limit=limit, offset=offset))  # type: ignore


@router.get(
    "/year/{year}",
    description="Get a single Year object containing EPA percentiles, Week 1 match score statistics, and prediction accuracy. After 2016, separated into components and ranking points included.",
    response_description="A Year object.",
)
@async_fail_gracefully_api_singular
async def read_year(
    response: Response,
    year: int,
) -> Dict[str, Any]:
    year_obj: Optional[Year] = await get_year_cached(year=year)
    if year_obj is None:
        raise Exception("Year not found")

    return year_obj.as_dict()


@router.get(
    "/years",
    description="Get a list of Year objects from 2002 to 2023. Specify a four-digit year, ex: 2019",
    response_description="A list of Year objects. See /year/{year} for more information.",
)
@async_fail_gracefully_api_plural
async def read_years(
    response: Response,
    metric: Optional[str] = None,
    ascending: Optional[bool] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> List[Dict[str, Any]]:
    years: List[Year] = await get_years_cached(
        metric=metric, ascending=ascending, limit=limit, offset=offset
    )
    return [year.as_dict() for year in years]
