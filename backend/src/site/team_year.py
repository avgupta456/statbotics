from typing import Any, Dict, List, Optional

from fastapi import APIRouter
from fastapi.responses import Response

from src.api import get_team_matches_cached, get_team_years_cached, get_year_cached
from src.constants import CURR_YEAR
from src.db.models import TeamMatch, TeamYear, Year

# from src.site.helper import compress
from src.utils.decorators import (
    async_fail_gracefully_plural,
    async_fail_gracefully_singular,
)

router = APIRouter()


def _read_team_years(
    year: int, year_obj: Year, team_years: List[TeamYear]
) -> Dict[str, Any]:
    team_years = [x for x in team_years if x.count > 0 or year >= CURR_YEAR]

    return {
        "team_years": [x.to_dict() for x in team_years],
        "year": year_obj.to_dict(),
    }


@router.get("/team_years/{year}")
@async_fail_gracefully_singular
async def read_team_years(
    response: Response,
    year: int,
    limit: Optional[int] = None,
    metric: Optional[str] = None,
    no_cache: bool = False,
) -> Any:
    year_obj: Optional[Year] = await get_year_cached(year=year, no_cache=no_cache)
    if year_obj is None:
        raise Exception("Year not found")

    team_years: List[TeamYear] = await get_team_years_cached(
        year=year, limit=limit, metric=metric, site=True, no_cache=no_cache
    )

    return _read_team_years(year, year_obj, team_years)


@router.get("/team_year/{year}/{team}/matches")
@async_fail_gracefully_plural
async def read_team_matches(
    response: Response, year: int, team: int, no_cache: bool = False
) -> Any:
    team_matches: List[TeamMatch] = await get_team_matches_cached(
        team=team, year=year, no_cache=no_cache
    )

    team_matches = sorted(team_matches, key=lambda x: x.time)

    out = [x.to_dict() for x in team_matches]

    return out
