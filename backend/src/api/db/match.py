from datetime import timedelta
from typing import Optional

from src.db.models.match import Match
from src.db.read.match import get_match as _get_match
from src.utils.alru_cache import alru_cache


@alru_cache(ttl=timedelta(minutes=5))
async def get_match(match_id: str, no_cache: bool = False) -> Optional[Match]:
    match = _get_match(match_id)

    # If invalid, do not cache
    if match is None:
        return (False, None)  # type: ignore

    # If valid, cache
    return (True, match)  # type: ignore
