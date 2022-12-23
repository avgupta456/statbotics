from typing import Dict

from src.api.db.year import get_year


async def get_year_stats(year: int) -> Dict[str, float]:
    year_obj = await get_year(year)
    if year_obj is None:
        raise Exception("Year not found")

    auto_mean = year_obj.auto_mean
    teleop_mean = year_obj.teleop_mean
    endgame_mean = year_obj.endgame_mean
    total_mean = year_obj.score_mean
    foul_rate = (year_obj.fouls_mean or 0) / (year_obj.no_fouls_mean or 1)
    rp_1_mean = (year_obj.rp_1_mean or 0) + 1
    rp_2_mean = (year_obj.rp_2_mean or 0) + 1

    return {
        "auto_mean": auto_mean,
        "teleop_mean": teleop_mean,
        "endgame_mean": endgame_mean,
        "total_mean": total_mean,
        "foul_rate": foul_rate,
        "rp_1_mean": rp_1_mean,
        "rp_2_mean": rp_2_mean,
    }
