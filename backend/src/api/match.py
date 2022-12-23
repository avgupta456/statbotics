from datetime import timedelta
from typing import Any, Dict, Optional

from fastapi import APIRouter, Response

from src.db.models.match import Match
from src.db.read.event import get_event
from src.db.read.match import get_match
from src.db.read.year import get_year
from src.db.read.team_match import get_team_matches
from src.utils.alru_cache import alru_cache
from src.utils.decorators import async_fail_gracefully
from src.utils.utils import get_match_name

router = APIRouter()


@router.get("/")
async def read_root():
    return {"name": "Match Router"}


@alru_cache(ttl=timedelta(minutes=5))
async def _read_match(match_id: str, no_cache: bool = False) -> Dict[str, Any]:
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
            "rp_1_epa": x.rp_1_epa,
            "rp_2_epa": x.rp_2_epa,
            "alliance": x.alliance,
        }
        for x in team_matches
    }

    event_obj = get_event(match.event)
    if event_obj is None:
        raise Exception("Event not found")
    event_name = event_obj.name

    year_obj = get_year(match.year)
    if year_obj is None:
        raise Exception("Year not found")
    auto_mean = year_obj.auto_mean
    teleop_mean = year_obj.teleop_mean
    endgame_mean = year_obj.endgame_mean
    total_mean = year_obj.score_mean
    foul_rate = (year_obj.fouls_mean or 0) / (year_obj.no_fouls_mean or 1)
    rp_1_mean = (year_obj.rp_1_mean or 0) + 1 / 3
    rp_2_mean = (year_obj.rp_2_mean or 0) + 1 / 3

    match_name = get_match_name(match.key)

    return (
        True,
        {
            "match": match.to_dict(),
            "team_matches": team_matches_dict,
            "event_name": event_name,
            "match_name": match_name,
            "year_stats": {
                "auto_mean": auto_mean,
                "teleop_mean": teleop_mean,
                "endgame_mean": endgame_mean,
                "total_mean": total_mean,
                "foul_rate": foul_rate,
                "rp_1_mean": rp_1_mean,
                "rp_2_mean": rp_2_mean,
            },
        },
    )  # type: ignore


@router.get("/{match_id}")
@async_fail_gracefully
async def read_match(response: Response, match_id: str) -> Dict[str, Any]:
    return await _read_match(match_id)
