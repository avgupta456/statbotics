from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Response

from src.api.team import get_team_cached, get_teams_cached
from src.api.v2.utils import format_team, inv_format_team
from src.db.models import Team
from src.utils.decorators import (
    async_fail_gracefully_plural,
    async_fail_gracefully_singular,
)

router = APIRouter()


def get_v2_team(team: Team) -> Dict[str, Any]:
    return {
        "team": format_team(team.team),
        "name": team.name,
        "offseason": team.offseason,
        "state": team.state,
        "country": team.country,
        "district": team.district,
        "rookie_year": team.rookie_year,
        "active": team.active,
        "norm_epa": team.norm_epa,
        "norm_epa_recent": team.norm_epa_recent,
        "norm_epa_mean": team.norm_epa_mean,
        "norm_epa_max": team.norm_epa_max,
        "wins": team.wins,
        "losses": team.losses,
        "ties": team.ties,
        "count": team.count,
        "winrate": team.winrate,
        "full_wins": team.full_wins,
        "full_losses": team.full_losses,
        "full_ties": team.full_ties,
        "full_count": team.full_count,
        "full_winrate": team.full_winrate,
    }


@router.get("/")
async def read_root_team():
    return {"name": "Team Router"}


@router.get(
    "/team/{team}",
    description="Get a single Team object containing team name, location, normalized EPA statistics, and winrate.",
    response_description="A Team object.",
)
@async_fail_gracefully_singular
async def read_team(
    response: Response,
    team: int,
) -> Dict[str, Any]:
    team_obj: Optional[Team] = await get_team_cached(team=inv_format_team(team))
    if team_obj is None:
        raise Exception("Team not found")

    return get_v2_team(team_obj)


@router.get(
    "/teams/district/{district}",
    description="Get a list of Team objects from a single district. Specify lowercase district abbreviation, ex: fnc, fim",
    response_description="A list of Team objects. See /team/{team} for more information.",
)
@async_fail_gracefully_plural
async def read_teams_district(
    response: Response,
    district: str,
) -> List[Dict[str, Any]]:
    teams: List[Team] = await get_teams_cached(district=district)
    return [get_v2_team(team) for team in teams]


@router.get(
    "/teams/state/{state}",
    description="Get a list of Team objects from a single state. Specify uppercase state abbreviation, ex: NC, CA",
    response_description="A list of Team objects. See /team/{team} for more information.",
)
@async_fail_gracefully_plural
async def read_teams_state(
    response: Response,
    state: str,
) -> List[Dict[str, Any]]:
    teams: List[Team] = await get_teams_cached(state=state)
    return [get_v2_team(team) for team in teams]


@router.get(
    "/teams",
    description="Get a list of Team objects with optional filters.",
    response_description="A list of Team objects. See /team/{team} for more information.",
)
@async_fail_gracefully_plural
async def read_teams(
    response: Response,
    country: Optional[str] = None,
    district: Optional[str] = None,
    state: Optional[str] = None,
    active: Optional[bool] = None,
    offseason: Optional[bool] = False,
    metric: str = "team",
    ascending: bool = True,
    limit: int = 100,
    offset: int = 0,
) -> List[Dict[str, Any]]:
    teams: List[Team] = await get_teams_cached(
        country=country,
        district=district,
        state=state,
        active=active,
        offseason=offseason,
        metric=metric,
        ascending=ascending,
        limit=limit,
        offset=offset,
    )
    return [get_v2_team(team) for team in teams]
