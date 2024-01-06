from typing import Any, List, Optional

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from src.api import get_team_years_cached, get_year_cached  # get_team_matches_cached
from src.constants import CURR_YEAR
from src.db.models import TeamYear, Year  # TeamMatch
from src.site.helper import compress
from src.utils.decorators import async_fail_gracefully_singular

router = APIRouter()


@router.get("/team_years/{year}")
@async_fail_gracefully_singular
async def read_team_years(
    response: StreamingResponse,
    year: int,
    limit: Optional[int] = None,
    metric: Optional[str] = None,
    no_cache: bool = False,
) -> Any:
    year_obj: Optional[Year] = await get_year_cached(year=year, no_cache=no_cache)
    if year_obj is None:
        raise Exception("Year not found")

    team_years: List[TeamYear] = await get_team_years_cached(
        year=year,
        offseason=False,
        limit=limit,
        metric=metric,
        site=True,
        no_cache=no_cache,
    )
    team_years = [x for x in team_years if x.count > 0 or year >= CURR_YEAR]

    out = {
        "team_years": [x.to_dict() for x in team_years],
        "year": year_obj.to_dict(),
    }

    return compress(out)


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
