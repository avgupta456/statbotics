from datetime import timedelta
from typing import Optional

from src.db.models import Year
from src.db.read import get_year as _get_year
from src.utils.alru_cache import alru_cache
from src.api.models import APIYear, PercentileStats


def unpack_year(year: Year) -> APIYear:
    total_stats = PercentileStats(
        p99=year.epa_1p or 0,
        p95=year.epa_5p or 0,
        p90=year.epa_10p or 0,
        p75=year.epa_25p or 0,
        p50=year.epa_median or 0,
        p25=year.epa_75p or 0,
        mean=year.epa_mean or 0,
        sd=year.epa_sd or 0,
    )

    auto_stats = PercentileStats(
        p99=year.auto_epa_1p or 0,
        p95=year.auto_epa_5p or 0,
        p90=year.auto_epa_10p or 0,
        p75=year.auto_epa_25p or 0,
        p50=year.auto_epa_median or 0,
        p25=year.auto_epa_75p or 0,
        mean=year.auto_epa_mean or 0,
        sd=year.auto_epa_sd or 0,
    )

    teleop_stats = PercentileStats(
        p99=year.teleop_epa_1p or 0,
        p95=year.teleop_epa_5p or 0,
        p90=year.teleop_epa_10p or 0,
        p75=year.teleop_epa_25p or 0,
        p50=year.teleop_epa_median or 0,
        p25=year.teleop_epa_75p or 0,
        mean=year.teleop_epa_mean or 0,
        sd=year.teleop_epa_sd or 0,
    )

    endgame_stats = PercentileStats(
        p99=year.endgame_epa_1p or 0,
        p95=year.endgame_epa_5p or 0,
        p90=year.endgame_epa_10p or 0,
        p75=year.endgame_epa_25p or 0,
        p50=year.endgame_epa_median or 0,
        p25=year.endgame_epa_75p or 0,
        mean=year.endgame_epa_mean or 0,
        sd=year.endgame_epa_sd or 0,
    )

    rp_1_stats = PercentileStats(
        p99=year.rp_1_epa_1p or 0,
        p95=year.rp_1_epa_5p or 0,
        p90=year.rp_1_epa_10p or 0,
        p75=year.rp_1_epa_25p or 0,
        p50=year.rp_1_epa_median or 0,
        p25=year.rp_1_epa_75p or 0,
        mean=year.rp_1_epa_mean or 0,
        sd=year.rp_1_epa_sd or 0,
    )

    rp_2_stats = PercentileStats(
        p99=year.rp_2_epa_1p or 0,
        p95=year.rp_2_epa_5p or 0,
        p90=year.rp_2_epa_10p or 0,
        p75=year.rp_2_epa_25p or 0,
        p50=year.rp_2_epa_median or 0,
        p25=year.rp_2_epa_75p or 0,
        mean=year.rp_2_epa_mean or 0,
        sd=year.rp_2_epa_sd or 0,
    )

    foul_rate = (year.fouls_mean or 0) / (year.no_fouls_mean or 1)

    return APIYear(
        year=year.year,
        total_stats=total_stats,
        auto_stats=auto_stats,
        teleop_stats=teleop_stats,
        endgame_stats=endgame_stats,
        rp_1_stats=rp_1_stats,
        rp_2_stats=rp_2_stats,
        foul_rate=foul_rate,
    )


@alru_cache(ttl=timedelta(minutes=5))
async def get_year(year: int, no_cache: bool = False) -> Optional[APIYear]:
    year_obj = _get_year(year=year)

    # If invalid, do not cache
    if year_obj is None:
        return (False, None)  # type: ignore

    # If valid, cache
    return (True, unpack_year(year_obj))  # type: ignore
