from datetime import timedelta
from typing import Optional

from src.db.models.year import Year
from src.db.read.year import get_year as _get_year
from src.utils.alru_cache import alru_cache


@alru_cache(ttl=timedelta(minutes=5))
async def get_year(year: int, no_cache: bool = False) -> Optional[Year]:
    year_obj = _get_year(year)

    # If invalid, do not cache
    if year_obj is None:
        return (False, None)  # type: ignore

    # If valid, cache
    return (True, year_obj)  # type: ignore
