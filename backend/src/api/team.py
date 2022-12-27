from typing import Any, Dict, List

from fastapi import APIRouter, Response

from src.api.db.team import get_teams
from src.utils.decorators import async_fail_gracefully

router = APIRouter()


@router.get("/")
async def read_root():
    return {"name": "Team Router"}


@router.get("/all")
@async_fail_gracefully
async def read_all_teams(response: Response) -> List[Dict[str, Any]]:
    return [{"num": x.team, "team": x.name} for x in await get_teams()]
