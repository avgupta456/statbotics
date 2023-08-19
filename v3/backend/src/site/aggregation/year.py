from datetime import timedelta
from typing import Optional

from src.db.models import Year
from src.db.read import get_year as _get_year
from src.site.models import APIYear, PercentileStats
from src.utils.alru_cache import alru_cache


def unpack_year(year: Year) -> APIYear:
    total_stats = PercentileStats(
        p99=year.epa_1p or 0,
        p90=year.epa_10p or 0,
        p75=year.epa_25p or 0,
        p25=year.epa_75p or 0,
    )

    auto_stats = PercentileStats(
        p99=year.auto_epa_1p or 0,
        p90=year.auto_epa_10p or 0,
        p75=year.auto_epa_25p or 0,
        p25=year.auto_epa_75p or 0,
    )

    teleop_stats = PercentileStats(
        p99=year.teleop_epa_1p or 0,
        p90=year.teleop_epa_10p or 0,
        p75=year.teleop_epa_25p or 0,
        p25=year.teleop_epa_75p or 0,
    )

    endgame_stats = PercentileStats(
        p99=year.endgame_epa_1p or 0,
        p90=year.endgame_epa_10p or 0,
        p75=year.endgame_epa_25p or 0,
        p25=year.endgame_epa_75p or 0,
    )

    foul_rate = (year.fouls_mean or 0) / (year.no_fouls_mean or 1)

    return APIYear(
        year=year.year,
        score_mean=year.score_mean or 0,
        score_sd=year.score_sd or 0,
        total_stats=total_stats,
        auto_stats=auto_stats,
        teleop_stats=teleop_stats,
        endgame_stats=endgame_stats,
        foul_rate=foul_rate,
    )


@alru_cache(ttl=timedelta(minutes=1))
async def get_year(year: int, no_cache: bool = False) -> Optional[APIYear]:
    year_obj = _get_year(year=year)

    # If invalid, do not cache
    if year_obj is None:
        return (False, None)  # type: ignore

    # If valid, cache
    return (True, unpack_year(year_obj))  # type: ignore
