import statistics
from typing import List, Tuple, Callable, Optional

from src.types.enums import MatchStatus
from src.db.models import Alliance, Year


def process_year(year: Year, alliances: List[Alliance]) -> Year:
    week_one_alliances = [
        a for a in alliances if a.week == 1 and a.status == MatchStatus.COMPLETED
    ]

    def get_mean_sd(
        accessor: Callable[[Alliance], Optional[float]]
    ) -> Tuple[float, float]:
        arr: List[Optional[float]] = [accessor(x) for x in week_one_alliances]
        clean_arr: List[float] = [x for x in arr if x is not None]
        if len(clean_arr) == 0:
            raise ValueError("Empty array for mean/sd calculation")

        mean = statistics.mean(clean_arr)
        sd = statistics.pstdev(clean_arr)
        return round(mean, 2), round(sd, 2)

    N = len(week_one_alliances)
    if year.year == 2024 and N < 100:
        year.score_mean, year.score_sd = 30, 10
        year.no_foul_mean, year.no_foul_sd = 30, 10
        year.foul_mean, year.foul_sd = 0, 0
        year.auto_mean, year.auto_sd = 10, 10 / 3
        year.teleop_mean, year.teleop_sd = 10, 10 / 3
        year.endgame_mean, year.endgame_sd = 10, 10 / 3
        year.rp_1_mean, year.rp_1_sd = 0.5, 0.5 / 3
        year.rp_2_mean, year.rp_2_sd = 0.5, 0.5 / 3
        year.tiebreaker_mean, year.tiebreaker_sd = 0, 0
        year.comp_1_mean, year.comp_1_sd = 3, 1
        year.comp_2_mean, year.comp_2_sd = 3, 1
        year.comp_3_mean, year.comp_3_sd = 3, 1
        year.comp_4_mean, year.comp_4_sd = 3, 1
        year.comp_5_mean, year.comp_5_sd = 3, 1
        year.comp_6_mean, year.comp_6_sd = 3, 1
        year.comp_7_mean, year.comp_7_sd = 3, 1
        year.comp_8_mean, year.comp_8_sd = 3, 1
        year.comp_9_mean, year.comp_9_sd = 3, 1
        year.comp_10_mean, year.comp_10_sd = 3, 1
        year.comp_11_mean, year.comp_11_sd = 0, 0
        year.comp_12_mean, year.comp_12_sd = 0, 0
    elif year.year < 2016:
        year.score_mean, year.score_sd = get_mean_sd(lambda a: a.score)
    else:
        year.score_mean, year.score_sd = get_mean_sd(lambda a: a.score)
        year.no_foul_mean, year.no_foul_sd = get_mean_sd(lambda a: a.no_foul)
        year.foul_mean, year.foul_sd = get_mean_sd(lambda a: a.foul)
        year.auto_mean, year.auto_sd = get_mean_sd(lambda a: a.auto)
        year.teleop_mean, year.teleop_sd = get_mean_sd(lambda a: a.teleop)
        year.endgame_mean, year.endgame_sd = get_mean_sd(lambda a: a.endgame)
        year.rp_1_mean, year.rp_1_sd = get_mean_sd(lambda a: a.rp_1)
        year.rp_2_mean, year.rp_2_sd = get_mean_sd(lambda a: a.rp_2)
        year.tiebreaker_mean, year.tiebreaker_sd = get_mean_sd(lambda a: a.tiebreaker)
        year.comp_1_mean, year.comp_1_sd = get_mean_sd(lambda a: a.comp_1)
        year.comp_2_mean, year.comp_2_sd = get_mean_sd(lambda a: a.comp_2)
        year.comp_3_mean, year.comp_3_sd = get_mean_sd(lambda a: a.comp_3)
        year.comp_4_mean, year.comp_4_sd = get_mean_sd(lambda a: a.comp_4)
        year.comp_5_mean, year.comp_5_sd = get_mean_sd(lambda a: a.comp_5)
        year.comp_6_mean, year.comp_6_sd = get_mean_sd(lambda a: a.comp_6)
        year.comp_7_mean, year.comp_7_sd = get_mean_sd(lambda a: a.comp_7)
        year.comp_8_mean, year.comp_8_sd = get_mean_sd(lambda a: a.comp_8)
        year.comp_9_mean, year.comp_9_sd = get_mean_sd(lambda a: a.comp_9)
        year.comp_10_mean, year.comp_10_sd = get_mean_sd(lambda a: a.comp_10)
        year.comp_11_mean, year.comp_11_sd = get_mean_sd(lambda a: a.comp_11)
        year.comp_12_mean, year.comp_12_sd = get_mean_sd(lambda a: a.comp_12)

    return year
