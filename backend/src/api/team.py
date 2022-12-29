from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Response

from src.api.db.team import get_teams, get_team
from src.db.models.team import Team
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
        "rookie_year": 2008,  # TODO: Add to, get from DB
    }
