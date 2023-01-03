from typing import Any, Dict, Optional

from fastapi import APIRouter, Response

from src.api.aggregation.year import get_year
from src.api.db.event import get_event
from src.api.db.match import get_match

# from src.api.db.team_match import get_team_matches
from src.db.models.match import Match
from src.utils.decorators import async_fail_gracefully
from src.utils.utils import get_match_name

router = APIRouter()


@router.get("/")
async def read_root():
    return {"name": "Match Router"}


@router.get("/match/{match_id}")
@async_fail_gracefully
async def read_match(response: Response, match_id: str) -> Dict[str, Any]:
    match: Optional[Match] = await get_match(match_id)

    if match is None:
        raise Exception("Match not found")

    team_matches = await get_team_matches(match=match_id)

    if team_matches is None:
        raise Exception("Team matches not found")

    team_matches_dict = {
        x.team: {
            "epa": x.epa,
            "auto_epa": x.auto_epa,
            "teleop_epa": x.teleop_epa,
            "endgame_epa": x.endgame_epa,
            "rp_1_epa": x.rp_1_epa,
            "rp_2_epa": x.rp_2_epa,
            "alliance": x.alliance,
        }
        for x in team_matches
    }

    event_obj = await get_event(match.event)
    if event_obj is None:
        raise Exception("Event not found")
    event_name = event_obj.name
    match_name = get_match_name(match.key)

    year_stats = await get_year_stats(match.year)

    out = {
        "match": match.to_dict(),
        "team_matches": team_matches_dict,
        "event_name": event_name,
        "match_name": match_name,
        "year_stats": year_stats,
    }

    return out
