from typing import Any, Dict, List

from fastapi import APIRouter, Response

from src.api.aggregation.team_match import get_team_matches
from src.api.aggregation.year import get_year_stats
from src.api.db.team_year import get_team_years
from src.db.models.team_year import TeamYear
from src.utils.decorators import async_fail_gracefully

router = APIRouter()


@router.get("/")
async def read_root():
    return {"name": "Team Year Router"}


@router.get("/team_years/{year}")
@async_fail_gracefully
async def read_team_years(response: Response, year: int) -> Dict[str, Any]:
    team_year_objs: List[TeamYear] = await get_team_years(year)

    team_years = [
        {
            "num": x.team,
            "team": x.name,
            "state": x.state,
            "country": x.country,
            "district": x.district,
            "epa_rank": x.epa_rank,
            "country_epa_rank": x.country_epa_rank,
            "state_epa_rank": x.state_epa_rank,
            "district_epa_rank": x.district_epa_rank,
            "norm_epa": x.norm_epa_end,
            "total_epa": x.epa_end,
            "auto_epa": x.auto_epa_end,
            "teleop_epa": x.teleop_epa_end,
            "endgame_epa": x.endgame_epa_end,
            "rp_1_epa": x.rp_1_epa_end,
            "rp_2_epa": x.rp_2_epa_end,
            "wins": x.wins,
            "losses": x.losses,
            "ties": x.ties,
            "count": x.count,
        }
        for x in team_year_objs
    ]

    year_stats = await get_year_stats(year)

    out = {
        "team_years": team_years,
        "year_stats": year_stats,
    }

    return out


@router.get("/team_year/{year}/{team}")
@async_fail_gracefully
async def read_team_matches(
    response: Response, year: int, team: int
) -> List[Dict[str, Any]]:
    return await get_team_matches(year=year, team=team)
