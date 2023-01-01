from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Response

from src.api.aggregation.year import get_year_stats
from src.api.db.match import get_matches
from src.api.db.event import get_event
from src.api.db.team_event import get_team_events
from src.api.db.team_match import get_team_matches
from src.api.utils import unpack_match
from src.data.nepa import get_epa_to_norm_epa_func
from src.db.models.event import Event
from src.db.models.team_event import TeamEvent
from src.db.models.team_match import TeamMatch
from src.db.models.match import Match
from src.utils.decorators import async_fail_gracefully
from src.utils.utils import get_match_number

router = APIRouter()


@router.get("/")
async def read_root():
    return {"name": "Event Router"}


@router.get("/event/{event_id}")
@async_fail_gracefully
async def read_event(response: Response, event_id: str) -> Dict[str, Any]:
    event: Optional[Event] = await get_event(event_id)

    if event is None:
        raise Exception("Event not found")

    epa_to_norm_epa = get_epa_to_norm_epa_func(event.year)

    team_event_objs: List[TeamEvent] = await get_team_events(event_id=event_id)

    team_events = [
        {
            "num": x.team,
            "team": x.team_name,
            "total_epa": x.epa_end,
            "norm_epa": epa_to_norm_epa(x.epa_end or 0),
            "auto_epa": x.auto_epa_end,
            "teleop_epa": x.teleop_epa_end,
            "endgame_epa": x.endgame_epa_end,
            "rp_1_epa": x.rp_1_epa_end,
            "rp_2_epa": x.rp_2_epa_end,
            "wins": x.wins,
            "losses": x.losses,
            "ties": x.ties,
            "count": x.count,
            "rank": x.rank,
        }
        for x in team_event_objs
    ]

    match_objs: List[Match] = await get_matches(event_id=event_id)
    matches = [unpack_match(m) for m in match_objs]
    matches.sort(key=lambda x: x["time"] or 0)

    year_stats = await get_year_stats(event.year)

    out = {
        "event_name": event.name,
        "year": event.year,
        "team_events": team_events,
        "matches": matches,
        "year_stats": year_stats,
    }

    return out


@router.get("/event/{event_id}/team_matches/{team}")
@async_fail_gracefully
async def read_team_matches(
    response: Response, event_id: str, team: int
) -> List[Dict[str, Any]]:
    team_match_objs: List[TeamMatch] = await get_team_matches(event=event_id, team=team)

    team_matches = [
        {
            "match": get_match_number(x.match),
            "playoff": x.playoff,
            "total_epa": x.epa,
            "auto_epa": x.auto_epa,
            "teleop_epa": x.teleop_epa,
            "endgame_epa": x.endgame_epa,
            "rp_1_epa": x.rp_1_epa,
            "rp_2_epa": x.rp_2_epa,
        }
        for x in team_match_objs
    ]

    return team_matches
