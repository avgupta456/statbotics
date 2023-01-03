from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Response

from src.api.aggregation.team_match import get_team_matches
from src.api.aggregation.year import get_year
from src.api.aggregation.team_year import get_team_years
from src.api.models.team_year import APITeamYear
from src.api.models.year import APIYear
from src.api.models.team_match import APITeamMatch
from src.utils.decorators import async_fail_gracefully

router = APIRouter()


@router.get("/")
async def read_root():
    return {"name": "Team Year Router"}


@router.get("/team_years/{year}")
@async_fail_gracefully
async def read_team_years(response: Response, year: int) -> Dict[str, Any]:
    team_years: List[APITeamYear] = await get_team_years(year=year)
    team_years = [x for x in team_years if x.count > 0]

    year_obj: Optional[APIYear] = await get_year(year=year)
    if year_obj is None:
        raise Exception("Year not found")

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
