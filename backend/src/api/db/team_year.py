from datetime import timedelta
from typing import List, Optional

from src.db.models.team_year import TeamYear
from src.db.read.team_year import get_team_years as _get_team_years
from src.utils.alru_cache import alru_cache


@alru_cache(ttl=timedelta(minutes=5))
async def get_team_years(
    year: Optional[int] = None, no_cache: bool = False
) -> List[TeamYear]:
    return (True, _get_team_years(year))  # type: ignore
