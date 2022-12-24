from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Response

from src.api.aggregation.year import get_year_stats
from src.api.db.event import get_event
from src.api.db.team_event import get_team_events
from src.db.models.event import Event
from src.db.models.team_event import TeamEvent
from src.utils.decorators import async_fail_gracefully

router = APIRouter()


@router.get("/")
async def read_root():
    return {"name": "Event Router"}


@router.get("/{event_id}")
@async_fail_gracefully
async def read_event(response: Response, event_id: str) -> Dict[str, Any]:
    event: Optional[Event] = await get_event(event_id)

    if event is None:
        raise Exception("Event not found")

    event_name = event.name

    team_event_objs: List[TeamEvent] = await get_team_events(event_id=event_id)

    team_events = [
        {
            "num": x.team,
            "team": x.team_name,
            "epa_start": x.epa_start,
            "epa": x.epa_end,
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

    year_stats = await get_year_stats(event.year)

    out = {
        "event_name": event_name,
        "team_events": team_events,
        "year_stats": year_stats,
    }

    return out
