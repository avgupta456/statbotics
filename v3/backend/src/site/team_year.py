from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Response

from src.constants import CURR_YEAR
from src.site.aggregation import get_team_years, get_year  # get_team_matches
from src.site.models import APITeamYear, APIYear  # APITeamMatch
from src.utils.decorators import async_fail_gracefully_singular

router = APIRouter()


@router.get("/team_years/{year}")
@async_fail_gracefully_singular
async def read_team_years(
    response: Response,
    year: int,
    limit: Optional[int] = None,
    metric: Optional[str] = None,
    no_cache: bool = False,
) -> Dict[str, Any]:
    year_obj: Optional[APIYear] = await get_year(year=year, no_cache=no_cache)
    if year_obj is None:
        raise Exception("Year not found")

    team_years: List[APITeamYear] = await get_team_years(
        year=year,
        limit=limit,
        metric=metric,
        no_cache=no_cache,
    )
    team_years = [x for x in team_years if x.count > 0 or year >= CURR_YEAR]

    out = {
        "team_years": [x.to_dict() for x in team_years],
        "year": year_obj.to_dict(),
    }

    return out


"""
@router.get("/team_year/{year}/{team}/matches")
@async_fail_gracefully
async def read_team_matches(
    response: Response, year: int, team: str, no_cache: bool = False
) -> List[Dict[str, Any]]:
    team_matches: List[APITeamMatch] = await get_team_matches(
        team=team, year=year, no_cache=no_cache
    )
    return [x.to_dict() for x in team_matches]
"""
