from datetime import timedelta
from typing import Optional, Tuple

from src.db.models import Year
from src.db.read import get_year as _get_year
from src.site.v2.models import APIYear, PercentileStats
from src.utils.alru_cache import alru_cache


def unpack_year(year: Year) -> APIYear:
    total_stats = PercentileStats(
        p99=year.epa_99p or 0,
        p95=0,
        p90=year.epa_90p or 0,
        p75=year.epa_75p or 0,
        p50=0,
        p25=year.epa_25p or 0,
        mean=0,
        sd=0,
    )

    auto_stats = PercentileStats(
        p99=year.auto_epa_99p or 0,
        p95=0,
        p90=year.auto_epa_90p or 0,
        p75=year.auto_epa_75p or 0,
        p50=0,
        p25=year.auto_epa_25p or 0,
        mean=0,
        sd=0,
    )

    teleop_stats = PercentileStats(
        p99=year.teleop_epa_99p or 0,
        p95=0,
        p90=year.teleop_epa_90p or 0,
        p75=year.teleop_epa_75p or 0,
        p50=0,
        p25=year.teleop_epa_25p or 0,
        mean=0,
        sd=0,
    )

    endgame_stats = PercentileStats(
        p99=year.endgame_epa_99p or 0,
        p95=0,
        p90=year.endgame_epa_90p or 0,
        p75=year.endgame_epa_75p or 0,
        p50=0,
        p25=year.endgame_epa_25p or 0,
        mean=0,
        sd=0,
    )

    rp_1_stats = PercentileStats(
        p99=year.rp_1_epa_99p or 0,
        p95=0,
        p90=year.rp_1_epa_90p or 0,
        p75=year.rp_1_epa_75p or 0,
        p50=0,
        p25=year.rp_1_epa_25p or 0,
        mean=0,
        sd=0,
    )

    rp_2_stats = PercentileStats(
        p99=year.rp_2_epa_99p or 0,
        p95=0,
        p90=year.rp_2_epa_90p or 0,
        p75=year.rp_2_epa_75p or 0,
        p50=0,
        p25=year.rp_2_epa_25p or 0,
        mean=0,
        sd=0,
    )

    return APIYear(
        year=year.year,
        score_mean=year.score_mean or 0,
        score_sd=year.score_sd or 0,
        total_stats=total_stats,
        auto_stats=auto_stats,
        teleop_stats=teleop_stats,
        endgame_stats=endgame_stats,
        rp_1_stats=rp_1_stats,
        rp_2_stats=rp_2_stats,
    )


@alru_cache(ttl=timedelta(minutes=1))
async def get_year(year: int, no_cache: bool = False) -> Tuple[bool, Optional[APIYear]]:
    year_obj = _get_year(year=year)

    # If invalid, do not cache
    if year_obj is None:
        return (False, None)

    # If valid, cache
    return (True, unpack_year(year_obj))
