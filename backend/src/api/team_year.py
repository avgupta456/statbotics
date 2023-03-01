from datetime import timedelta
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Response

from src.db.models import TeamYear
from src.db.read import get_team_year, get_team_years
from src.utils.alru_cache import alru_cache
from src.utils.decorators import (
    async_fail_gracefully_api_plural,
    async_fail_gracefully_api_singular,
)

router = APIRouter()


@router.get("/")
async def read_root():
    return {"name": "Team Year Router"}


@alru_cache(ttl=timedelta(hours=1))
async def get_team_year_cached(team: str, year: int) -> Optional[TeamYear]:
    return (True, get_team_year(team=team, year=year))  # type: ignore


@alru_cache(ttl=timedelta(hours=1))
async def get_team_years_cached(
    team: Optional[int] = None,
    year: Optional[int] = None,
    country: Optional[str] = None,
    district: Optional[str] = None,
    state: Optional[str] = None,
    metric: Optional[str] = None,
    ascending: Optional[bool] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> List[TeamYear]:
    return (  # type: ignore
        True,
        get_team_years(
            team=team,
            year=year,
            country=country,
            district=district,
            state=state,
            metric=metric,
            ascending=ascending,
            limit=limit,
            offset=offset,
        ),
    )


@router.get(
    "/team_year/{team}/{year}",
    description="Get a single TeamYear object containing EPA summary, winrates, and location rankings",
    response_description="A TeamYear object.",
)
@async_fail_gracefully_api_singular
async def read_team_year(
    response: Response,
    team: int,
    year: int,
) -> Dict[str, Any]:
    team_year_obj: Optional[TeamYear] = await get_team_year_cached(team=team, year=year)
    if team_year_obj is None:
        raise Exception("TeamYear not found")

    return team_year_obj.as_dict()


@router.get(
    "/team_years/team/{team}",
    description="Get a list of TeamYear objects for a single team. Specify team number, ex: 254, 1114",
    response_description="A list of TeamYear objects. See /team_year/{team}/{year} for more information.",
)
@async_fail_gracefully_api_plural
async def read_team_years_team(
    response: Response,
    team: int,
) -> List[Dict[str, Any]]:
    team_years: List[TeamYear] = await get_team_years_cached(team=team)
    return [team_year.as_dict() for team_year in team_years]


@router.get(
    "/team_years/year/{year}/district/{district}",
    description="Get a list of TeamYear objects from a single district. Specify lowercase district abbreviation, ex: fnc, fim",
    response_description="A list of TeamYear objects. See /team_year/{team}/{year} for more information.",
)
@async_fail_gracefully_api_plural
async def read_team_years_district(
    response: Response,
    year: int,
    district: str,
) -> List[Dict[str, Any]]:
    team_years: List[TeamYear] = await get_team_years_cached(
        year=year, district=district
    )
    return [team_year.as_dict() for team_year in team_years]


@router.get(
    "/team_years/year/{year}/state/{state}",
    description="Get a list of TeamYear objects from a single state. Specify lowercase state abbreviation, ex: ca, tx",
    response_description="A list of TeamYear objects. See /team_year/{team}/{year} for more information.",
)
@async_fail_gracefully_api_plural
async def read_team_years_state(
    response: Response,
    year: int,
    state: str,
) -> List[Dict[str, Any]]:
    team_years: List[TeamYear] = await get_team_years_cached(year=year, state=state)
    return [team_year.as_dict() for team_year in team_years]


@router.get(
    "/team_years",
    description="Get a list of TeamYear objects with optional filters.",
    response_description="A list of TeamYear objects. See /team_year/{team}/{year} for more information.",
)
@async_fail_gracefully_api_plural
async def read_team_years(
    response: Response,
    team: Optional[int] = None,
    year: Optional[int] = None,
    country: Optional[str] = None,
    district: Optional[str] = None,
    state: Optional[str] = None,
    metric: Optional[str] = None,
    ascending: Optional[bool] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> List[Dict[str, Any]]:
    team_years: List[TeamYear] = await get_team_years_cached(
        team=team,
        year=year,
        country=country,
        district=district,
        state=state,
        metric=metric,
        ascending=ascending,
        limit=limit,
        offset=offset,
    )
    return [team_year.as_dict() for team_year in team_years]
