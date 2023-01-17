from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Response

from src.constants import CURR_YEAR
from src.site.aggregation import get_team_matches, get_team_years, get_year
from src.site.models import APITeamMatch, APITeamYear, APIYear
from src.utils.decorators import async_fail_gracefully

router = APIRouter()


@router.get("/team_years/{year}")
@async_fail_gracefully
async def read_team_years(response: Response, year: int) -> Dict[str, Any]:
    year_obj: Optional[APIYear] = await get_year(year=year)
    if year_obj is None:
        raise Exception("Year not found")

    team_years: List[APITeamYear] = await get_team_years(
        year=year, score_mean=year_obj.score_mean, score_sd=year_obj.score_sd
    )
    team_years = [x for x in team_years if x.count > 0 or year == CURR_YEAR]

    out = {
        "team_years": [x.to_dict() for x in team_years],
        "year": year_obj.to_dict(),
    }

    return out


@router.get("/team_year/{year}/{team}/matches")
@async_fail_gracefully
async def read_team_matches(
    response: Response, year: int, team: int
) -> List[Dict[str, Any]]:
    team_matches: List[APITeamMatch] = await get_team_matches(team=team, year=year)
    return [x.to_dict() for x in team_matches]
