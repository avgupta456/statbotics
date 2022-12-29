from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Response

from src.api.aggregation.team_match import get_team_matches
from src.api.db.team import get_team, get_teams
from src.api.db.team_year import get_team_year
from src.db.models.team import Team
from src.db.models.team_year import TeamYear
from src.utils.decorators import async_fail_gracefully

router = APIRouter()


@router.get("/")
async def read_root():
    return {"name": "Team Router"}


@router.get("/teams/all")
@async_fail_gracefully
async def read_all_teams(response: Response) -> List[Dict[str, Any]]:
    return [{"num": x.team, "team": x.name} for x in await get_teams()]


@router.get("/team/{team_num}")
@async_fail_gracefully
async def read_team(response: Response, team_num: int) -> Dict[str, Any]:
    team: Optional[Team] = await get_team(team_num)

    if team is None:
        raise Exception("Team not found")

    return {
        "num": team_num,
        "team": team.name,
        "country": team.country,
        "state": team.state,
        "district": team.district,
        "rookie_year": 2008,  # TODO: Add to, get from DB
    }


@router.get("/team/{team_num}/{year}")
@async_fail_gracefully
async def read_team_year(
    response: Response, team_num: int, year: int
) -> Dict[str, Any]:
    team_year: Optional[TeamYear] = await get_team_year(team_num, year)

    if team_year is None:
        raise Exception("TeamYear not found")

    team_matches = await get_team_matches(team_num, year)

    out = {
        "num": team_num,
        "team": team_year.name,
        "year": year,
        "team_year": {
            "epa_rank": team_year.total_epa_rank,
            "epa_count": team_year.total_team_count,
            "country_epa_rank": team_year.country_epa_rank,
            "country_count": team_year.country_team_count,
            "state_epa_rank": team_year.state_epa_rank,
            "state_count": team_year.state_team_count,
            "district_epa_rank": team_year.district_epa_rank,
            "district_count": team_year.district_team_count,
            "wins": team_year.wins,
            "losses": team_year.losses,
            "ties": team_year.ties,
            "count": team_year.count,
            "epa": team_year.epa_end,
            "norm_epa": team_year.norm_epa_end,
            "auto_epa": team_year.auto_epa_end,
            "teleop_epa": team_year.teleop_epa_end,
            "endgame_epa": team_year.endgame_epa_end,
            "rp_1_epa": team_year.rp_1_epa_end,
            "rp_2_epa": team_year.rp_2_epa_end,
        },
        "matches": team_matches,
    }

    return out
