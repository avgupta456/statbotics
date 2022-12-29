from datetime import timedelta
from typing import List, Optional

from src.db.models.team_event import TeamEvent
from src.db.read.team_event import get_team_events as _get_team_events
from src.utils.alru_cache import alru_cache


@alru_cache(ttl=timedelta(minutes=5))
async def get_team_events(
    year: Optional[int] = None,
    event_id: Optional[int] = None,
    team: Optional[int] = None,
    no_cache: bool = False,
) -> List[TeamEvent]:
    return (True, _get_team_events(year, event_id, team))  # type: ignore
