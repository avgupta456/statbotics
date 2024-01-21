from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Response

from src.constants import CURR_YEAR
from src.api.v2.utils import format_team, inv_format_team
from src.db.models import TeamYear
from src.api.team_year import get_team_year_cached, get_team_years_cached
from src.utils.decorators import (
    async_fail_gracefully_plural,
    async_fail_gracefully_singular,
)

router = APIRouter()


def get_v2_team_year(team_year: TeamYear) -> Dict[str, Any]:
    # TODO: {auto,teleop,endgame,rp_1,rp_2}_epa_{start,pre_champs,mean,max}, epa_mean
    return {
        "year": team_year.year,
        "team": format_team(team_year.team),
        "offseason": team_year.offseason,
        "name": team_year.name,
        "state": team_year.state,
        "country": team_year.country,
        "district": team_year.district,
        "is_competing": team_year.year == CURR_YEAR or team_year.count > 0,
        "epa_start": team_year.epa_start,
        "epa_pre_champs": team_year.epa_pre_champs,
        "epa_end": team_year.epa,
        "epa_mean": None,
        "epa_max": team_year.epa_max,
        "epa_diff": team_year.epa - team_year.epa_start,
        "auto_epa_start": None,
        "auto_epa_pre_champs": None,
        "auto_epa_end": team_year.auto_epa,
        "auto_epa_mean": None,
        "auto_epa_max": None,
        "teleop_epa_start": None,
        "teleop_epa_pre_champs": None,
        "teleop_epa_end": team_year.teleop_epa,
        "teleop_epa_mean": None,
        "teleop_epa_max": None,
        "endgame_epa_start": None,
        "endgame_epa_pre_champs": None,
        "endgame_epa_end": team_year.endgame_epa,
        "endgame_epa_mean": None,
        "endgame_epa_max": None,
        "rp_1_epa_start": None,
        "rp_1_epa_pre_champs": None,
        "rp_1_epa_end": team_year.rp_1_epa,
        "rp_1_epa_mean": None,
        "rp_1_epa_max": None,
        "rp_2_epa_start": None,
        "rp_2_epa_pre_champs": None,
        "rp_2_epa_end": team_year.rp_2_epa,
        "rp_2_epa_mean": None,
        "rp_2_epa_max": None,
        "unitless_epa_end": team_year.unitless_epa,
        "norm_epa_end": team_year.norm_epa,
        "wins": team_year.wins,
        "losses": team_year.losses,
        "ties": team_year.ties,
        "count": team_year.count,
        "winrate": team_year.winrate,
        "full_wins": team_year.full_wins,
        "full_losses": team_year.full_losses,
        "full_ties": team_year.full_ties,
        "full_count": team_year.full_count,
        "full_winrate": team_year.full_winrate,
        "total_epa_rank": team_year.total_epa_rank,
        "total_epa_percentile": team_year.total_epa_percentile,
        "total_team_count": team_year.total_team_count,
        "country_epa_rank": team_year.country_epa_rank,
        "country_epa_percentile": team_year.country_epa_percentile,
        "country_team_count": team_year.country_team_count,
        "state_epa_rank": team_year.state_epa_rank,
        "state_epa_percentile": team_year.state_epa_percentile,
        "state_team_count": team_year.state_team_count,
        "district_epa_rank": team_year.district_epa_rank,
        "district_epa_percentile": team_year.district_epa_percentile,
        "district_team_count": team_year.district_team_count,
    }


@router.get("/")
async def read_root():
    return {"name": "Team Year Router"}


@router.get(
    "/team_year/{team}/{year}",
    description="Get a single TeamYear object containing EPA summary, winrates, and location rankings",
    response_description="A TeamYear object.",
)
@async_fail_gracefully_singular
async def read_team_year(
    response: Response,
    team: int,
    year: int,
) -> Dict[str, Any]:
    team_year_obj: Optional[TeamYear] = await get_team_year_cached(
        team=inv_format_team(team), year=year
    )
    if team_year_obj is None:
        raise Exception("TeamYear not found")

    return get_v2_team_year(team_year_obj)


@router.get(
    "/team_years/team/{team}",
    description="Get a list of TeamYear objects for a single team. Specify team number, ex: 254, 1114",
    response_description="A list of TeamYear objects. See /team_year/{team}/{year} for more information.",
)
@async_fail_gracefully_plural
async def read_team_years_team(
    response: Response,
    team: int,
) -> List[Dict[str, Any]]:
    team_years: List[TeamYear] = await get_team_years_cached(team=inv_format_team(team))
    return [get_v2_team_year(team_year) for team_year in team_years]


@router.get(
    "/team_years/year/{year}/district/{district}",
    description="Get a list of TeamYear objects from a single district. Specify lowercase district abbreviation, ex: fnc, fim",
    response_description="A list of TeamYear objects. See /team_year/{team}/{year} for more information.",
)
@async_fail_gracefully_plural
async def read_team_years_district(
    response: Response,
    year: int,
    district: str,
) -> List[Dict[str, Any]]:
    team_years: List[TeamYear] = await get_team_years_cached(
        year=year, district=district
    )
    return [get_v2_team_year(team_year) for team_year in team_years]


@router.get(
    "/team_years/year/{year}/state/{state}",
    description="Get a list of TeamYear objects from a single state. Specify lowercase state abbreviation, ex: ca, tx",
    response_description="A list of TeamYear objects. See /team_year/{team}/{year} for more information.",
)
@async_fail_gracefully_plural
async def read_team_years_state(
    response: Response,
    year: int,
    state: str,
) -> List[Dict[str, Any]]:
    team_years: List[TeamYear] = await get_team_years_cached(year=year, state=state)
    return [get_v2_team_year(team_year) for team_year in team_years]


@router.get(
    "/team_years",
    description="Get a list of TeamYear objects with optional filters.",
    response_description="A list of TeamYear objects. See /team_year/{team}/{year} for more information.",
)
@async_fail_gracefully_plural
async def read_team_years(
    response: Response,
    team: Optional[int] = None,
    year: Optional[int] = None,
    country: Optional[str] = None,
    district: Optional[str] = None,
    state: Optional[str] = None,
    offseason: Optional[bool] = False,
    metric: Optional[str] = None,
    ascending: Optional[bool] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> List[Dict[str, Any]]:
    team_years: List[TeamYear] = await get_team_years_cached(
        team=None if team is None else inv_format_team(team),
        year=year,
        country=country,
        district=district,
        state=state,
        offseason=offseason,
        metric=metric,
        ascending=ascending,
        limit=limit,
        offset=offset,
    )
    return [get_v2_team_year(team_year) for team_year in team_years]
