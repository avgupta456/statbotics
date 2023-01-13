from datetime import timedelta
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Response

from src.db.models import Team
from src.db.read import get_team, get_teams
from src.utils.alru_cache import alru_cache
from src.utils.decorators import (
    async_fail_gracefully_api_singular,
    async_fail_gracefully_api_plural,
)

router = APIRouter()


@router.get("/")
async def read_root():
    return {"name": "Team Router"}


@alru_cache(ttl=timedelta(hours=1))
async def get_team_cached(team: str) -> Optional[Team]:
    return (True, get_team(team=team))  # type: ignore


@alru_cache(ttl=timedelta(hours=1))
async def get_teams_cached(
    district: Optional[str] = None, state: Optional[str] = None
) -> List[Team]:
    return (True, get_teams(district=district, state=state))  # type: ignore


@router.get(
    "/team/{team}",
    description="Get a single Team object containing team name, location, normalized EPA statistics, and winrate.",
    response_description="A Team object.",
)
@async_fail_gracefully_api_singular
async def read_team(
    response: Response,
    team: str,
) -> Dict[str, Any]:
    team_obj: Optional[Team] = await get_team_cached(team=team)
    if team_obj is None:
        raise Exception("Team not found")

    return team_obj.as_dict()


@router.get(
    "/teams/district/{district}",
    description="Get a list of Team objects from a single district. Specify lowercase district abbreviation, ex: fnc, fim",
    response_description="A list of Team objects. See /team/{team} for more information.",
)
@async_fail_gracefully_api_plural
async def read_teams_district(
    response: Response,
    district: str,
) -> List[Dict[str, Any]]:
    teams: List[Team] = await get_teams_cached(district=district)
    return [team.as_dict() for team in teams]


@router.get(
    "/teams/state/{state}",
    description="Get a list of Team objects from a single state. Specify uppercase state abbreviation, ex: NC, CA",
    response_description="A list of Team objects. See /team/{team} for more information.",
)
@async_fail_gracefully_api_plural
async def read_teams_state(
    response: Response,
    state: str,
) -> List[Dict[str, Any]]:
    teams: List[Team] = await get_teams_cached(state=state)
    return [team.as_dict() for team in teams]
