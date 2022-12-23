from typing import Any, Dict

from src.api.db.year import get_year


async def get_year_stats(year: int) -> Dict[str, Any]:
    year_obj = await get_year(year)
    if year_obj is None:
        raise Exception("Year not found")

    total_stats = {
        "p99": year_obj.epa_1p,
        "p95": year_obj.epa_5p,
        "p90": year_obj.epa_10p,
        "p75": year_obj.epa_25p,
        "p50": year_obj.epa_median,
        "p25": year_obj.epa_75p,
        "mean": year_obj.epa_mean,
        "sd": year_obj.epa_sd,
    }

    auto_stats = {
        "p99": year_obj.auto_epa_1p,
        "p95": year_obj.auto_epa_5p,
        "p90": year_obj.auto_epa_10p,
        "p75": year_obj.auto_epa_25p,
        "p50": year_obj.auto_epa_median,
        "p25": year_obj.auto_epa_75p,
        "mean": year_obj.auto_epa_mean,
        "sd": year_obj.auto_epa_sd,
    }

    teleop_stats = {
        "p99": year_obj.teleop_epa_1p,
        "p95": year_obj.teleop_epa_5p,
        "p90": year_obj.teleop_epa_10p,
        "p75": year_obj.teleop_epa_25p,
        "p50": year_obj.teleop_epa_median,
        "p25": year_obj.teleop_epa_75p,
        "mean": year_obj.teleop_epa_mean,
        "sd": year_obj.teleop_epa_sd,
    }

    endgame_stats = {
        "p99": year_obj.endgame_epa_1p,
        "p95": year_obj.endgame_epa_5p,
        "p90": year_obj.endgame_epa_10p,
        "p75": year_obj.endgame_epa_25p,
        "p50": year_obj.endgame_epa_median,
        "p25": year_obj.endgame_epa_75p,
        "mean": year_obj.endgame_epa_mean,
        "sd": year_obj.endgame_epa_sd,
    }

    rp_1_stats = {
        "p99": year_obj.rp_1_epa_1p,
        "p95": year_obj.rp_1_epa_5p,
        "p90": year_obj.rp_1_epa_10p,
        "p75": year_obj.rp_1_epa_25p,
        "p50": year_obj.rp_1_epa_median,
        "p25": year_obj.rp_1_epa_75p,
        "mean": year_obj.rp_1_epa_mean,
        "sd": year_obj.rp_1_epa_sd,
    }

    rp_2_stats = {
        "p99": year_obj.rp_2_epa_1p,
        "p95": year_obj.rp_2_epa_5p,
        "p90": year_obj.rp_2_epa_10p,
        "p75": year_obj.rp_2_epa_25p,
        "p50": year_obj.rp_2_epa_median,
        "p25": year_obj.rp_2_epa_75p,
        "mean": year_obj.rp_2_epa_mean,
        "sd": year_obj.rp_2_epa_sd,
    }

    foul_rate = (year_obj.fouls_mean or 0) / (year_obj.no_fouls_mean or 1)

    return {
        "total": total_stats,
        "auto": auto_stats,
        "teleop": teleop_stats,
        "endgame": endgame_stats,
        "rp_1": rp_1_stats,
        "rp_2": rp_2_stats,
        "foul_rate": foul_rate,
    }
