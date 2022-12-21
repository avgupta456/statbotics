from typing import Any, Dict, Optional

from fastapi import APIRouter, Response

from src.db.models.match import Match
from src.db.read.match import get_match
from src.db.read.team_match import get_team_matches
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

    team_matches = get_team_matches(match=match_id)

    if team_matches is None:
        raise Exception("Team matches not found")

    team_matches_dict = {
        x.team: {
            "epa": x.epa,
            "auto_epa": x.auto_epa,
            "teleop_epa": x.teleop_epa,
            "endgame_epa": x.endgame_epa,
            "alliance": x.alliance,
        }
        for x in team_matches
    }

    return {
        "match": match.to_dict(),
        "team_matches": team_matches_dict,
    }
