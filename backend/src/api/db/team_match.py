from datetime import timedelta
from typing import List, Optional

from src.db.models.team_match import TeamMatch
from src.db.read.team_match import get_team_matches as _get_team_matches
from src.utils.alru_cache import alru_cache


@alru_cache(ttl=timedelta(minutes=5))
async def get_team_matches(
    year: Optional[int] = None,
    event: Optional[str] = None,
    team: Optional[int] = None,
    match: Optional[str] = None,
    no_cache: bool = False,
) -> List[TeamMatch]:
    return (True, _get_team_matches(year, event, team, match))  # type: ignore
