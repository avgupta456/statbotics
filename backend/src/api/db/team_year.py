from datetime import timedelta
from typing import List, Optional

from src.db.models.team_year import TeamYear
from src.db.read.team_year import (
    get_team_year as _get_team_year,
    get_team_years as _get_team_years,
)
from src.utils.alru_cache import alru_cache


@alru_cache(ttl=timedelta(minutes=5))
async def get_team_year(
    team_num: Optional[int] = None, year: Optional[int] = None, no_cache: bool = False
) -> Optional[TeamYear]:
    team_year = _get_team_year(team_num, year)  # type: ignore

    # If invalid, do not cache
    if team_year is None:
        return (False, None)  # type: ignore

    # If valid, cache
    return (True, team_year)  # type: ignore


@alru_cache(ttl=timedelta(minutes=5))
async def get_team_years(
    year: Optional[int] = None, no_cache: bool = False
) -> List[TeamYear]:
    return (True, _get_team_years(year))  # type: ignore
