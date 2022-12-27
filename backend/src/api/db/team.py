from datetime import timedelta
from typing import List

from src.db.models.team import Team
from src.db.read.team import get_teams as _get_teams
from src.utils.alru_cache import alru_cache


@alru_cache(ttl=timedelta(minutes=5))
async def get_teams(no_cache: bool = False) -> List[Team]:
    return (True, _get_teams())  # type: ignore
