from typing import Any, Dict, Optional

from fastapi import APIRouter, Response

from src.db.models.match import Match
from src.db.read.match import get_match
from src.utils.decorators import async_fail_gracefully

router = APIRouter()


@router.get("/")
async def read_root():
    return {"name": "Match Router"}


@router.get("/{match_id}")
@async_fail_gracefully
async def read_match(response: Response, match_id: str) -> Dict[str, Any]:
    match: Optional[Match] = get_match(match_id)

    if match is None:
        raise Exception("Match not found")

    return match.to_dict()
