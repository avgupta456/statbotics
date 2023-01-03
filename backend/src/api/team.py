from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Response

from src.api.aggregation.team_match import get_team_matches
from src.api.aggregation.team import get_team, get_teams
from src.api.aggregation.team_year import get_team_year
from src.api.aggregation.team_event import get_team_events
from src.api.aggregation.match import get_matches
from src.api.aggregation.year import get_year
from src.api.models.team import APITeam
from src.api.models.team_year import APITeamYear
from src.api.models.team_event import APITeamEvent
from src.api.models.match import APIMatch
from src.api.models.team_match import APITeamMatch
from src.api.models.year import APIYear
from src.utils.decorators import async_fail_gracefully

router = APIRouter()


@router.get("/")
async def read_root():
    return {"name": "Team Router"}


@router.get("/teams/all")
@async_fail_gracefully
async def read_all_teams(response: Response) -> List[Dict[str, Any]]:
    teams: List[APITeam] = await get_teams()
    return [{"num": x.num, "team": x.team} for x in teams if not x.offseason]


@router.get("/team/{team_num}")
@async_fail_gracefully
async def read_team(response: Response, team_num: int) -> Dict[str, Any]:
    team: Optional[APITeam] = await get_team(team=team_num)
    if team is None or team.offseason:
        raise Exception("Team not found")

    return team.to_dict()


@router.get("/team/{team_num}/{year}")
@async_fail_gracefully
async def read_team_year(
    response: Response, team_num: int, year: int
) -> Dict[str, Any]:
    year_obj: Optional[APIYear] = await get_year(year=year)
    if year_obj is None:
        raise Exception("Year not found")

    team_year: Optional[APITeamYear] = await get_team_year(team=team_num, year=year)
    if team_year is None or team_year.offseason:
        raise Exception("TeamYear not found")

    team_events: List[APITeamEvent] = await get_team_events(team=team_num, year=year)
    matches: List[APIMatch] = await get_matches(team=team_num, year=year)
    team_matches: List[APITeamMatch] = await get_team_matches(team=team_num, year=year)

    out = {
        "year": year_obj.to_dict(),
        "team_year": team_year.to_dict(),
        "team_events": [x.to_dict() for x in team_events],
        "matches": [x.to_dict() for x in matches],
        "team_matches": [x.to_dict() for x in team_matches],
    }

    return out
