from datetime import timedelta
from typing import Dict, Optional

from src.db.models import Year
from src.db.read import get_year as _get_year
from src.site.models import APIYear, PercentileStats
from src.site.static import get_epa_breakdown_percentiles
from src.utils.alru_cache import alru_cache


def unpack_year(
    year: Year, epa_breakdown_percentiles: Dict[str, Dict[str, float]]
) -> APIYear:
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

    epa_breakdown_stats = {
        k: PercentileStats(
            p99=v.get("p99", 0),
            p95=v.get("p95", 0),
            p90=v.get("p90", 0),
            p75=v.get("p75", 0),
            p50=v.get("p50", 0),
            p25=v.get("p25", 0),
            mean=v.get("mean", 0),
            sd=v.get("sd", 0),
        ).to_dict()  # to_dict() doesn't fully handle nesting
        for k, v in epa_breakdown_percentiles.items()
    }

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
        foul_rate=foul_rate,
        epa_breakdown_stats=epa_breakdown_stats,
    )


@alru_cache(ttl=timedelta(minutes=1))
async def get_year(year: int, no_cache: bool = False) -> Optional[APIYear]:
    year_obj = _get_year(year=year)

    # If invalid, do not cache
    if year_obj is None:
        return (False, None)  # type: ignore

    epa_breakdown_percentiles = {}
    if year == 2023:
        epa_breakdown_percentiles = get_epa_breakdown_percentiles()

    # If valid, cache
    return (True, unpack_year(year_obj, epa_breakdown_percentiles))  # type: ignore
