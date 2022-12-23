from typing import Any, Dict, Optional

from fastapi import APIRouter, Response

from src.db.models.match import Match
from src.api.db.event import get_event
from src.api.db.match import get_match
from src.api.db.year import get_year
from src.api.db.team_match import get_team_matches
from src.utils.decorators import async_fail_gracefully
from src.utils.utils import get_match_name

router = APIRouter()


@router.get("/")
async def read_root():
    return {"name": "Match Router"}


@router.get("/{match_id}")
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
            "alliance": x.alliance,
        }
        for x in team_matches
    }

    event_obj = await get_event(match.event)
    if event_obj is None:
        raise Exception("Event not found")
    event_name = event_obj.name

    year_obj = await get_year(match.year)
    if year_obj is None:
        raise Exception("Year not found")
    auto_mean = year_obj.auto_mean
    teleop_mean = year_obj.teleop_mean
    endgame_mean = year_obj.endgame_mean
    total_mean = year_obj.score_mean

    match_name = get_match_name(match.key)

    out = {
        "match": match.to_dict(),
        "team_matches": team_matches_dict,
        "event_name": event_name,
        "match_name": match_name,
        "year_stats": {
            "auto_mean": auto_mean,
            "teleop_mean": teleop_mean,
            "endgame_mean": endgame_mean,
            "total_mean": total_mean,
        },
    }

    print(out)

    return out
