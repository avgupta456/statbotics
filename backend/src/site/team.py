from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Response

from src.site.aggregation import (
    get_matches,
    get_team,
    get_team_events,
    get_team_matches,
    get_team_year,
    get_team_years,
    get_teams,
    get_year,
)
from src.site.models import (
    APIMatch,
    APITeam,
    APITeamEvent,
    APITeamMatch,
    APITeamYear,
    APIYear,
)
from src.utils.decorators import async_fail_gracefully

router = APIRouter()


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


@router.get("/team/{team_num}/years")
@async_fail_gracefully
async def read_team_years(response: Response, team_num: int) -> List[Dict[str, Any]]:
    team_years: List[APITeamYear] = await get_team_years(team=team_num)
    return [
        {
            "year": x.year,
            "team": x.team,
            "norm_epa": x.norm_epa,
            "epa_rank": x.epa_rank,
            "epa_count": x.epa_count,
        }
        for x in team_years
    ]


@router.get("/team/{team_num}/{year}")
@async_fail_gracefully
async def read_team_year(
    response: Response, team_num: int, year: int
) -> Dict[str, Any]:
    year_obj: Optional[APIYear] = await get_year(year=year)
    if year_obj is None:
        raise Exception("Year not found")

    team_year: Optional[APITeamYear] = await get_team_year(
        team=team_num,
        year=year,
        score_mean=year_obj.score_mean,
        score_sd=year_obj.score_sd,
    )
    if team_year is None or team_year.offseason:
        raise Exception("TeamYear not found")

    team_events: List[APITeamEvent] = await get_team_events(
        year=year,
        score_mean=year_obj.score_mean,
        score_sd=year_obj.score_sd,
        team=team_num,
    )
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
