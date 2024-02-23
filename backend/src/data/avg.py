import statistics
from typing import Callable, List, Optional, Tuple

from src.constants import CURR_YEAR
from src.db.models import Match, Year
from src.types.enums import MatchStatus
from src.utils.utils import r


def process_year(year: Year, matches: List[Match]) -> Year:
    week_one_matches = [
        m for m in matches if m.week == 1 and m.status == MatchStatus.COMPLETED
    ]

    def get_mean_sd(
        red_accessor: Callable[[Match], Optional[float]],
        blue_accessor: Callable[[Match], Optional[float]],
    ) -> Tuple[float, float]:
        arr: List[Optional[float]] = [red_accessor(x) for x in week_one_matches] + [
            blue_accessor(x) for x in week_one_matches
        ]
        clean_arr: List[float] = [x for x in arr if x is not None]
        if len(clean_arr) < 2:
            return 0, 0

        mean = statistics.mean(clean_arr)
        sd = statistics.stdev(clean_arr)
        return r(mean, 2), r(sd, 2)

    N = 2 * len(week_one_matches)
    if year.year == CURR_YEAR and N < 100:
        year.score_mean, year.score_sd = 39.74, 24.11
        year.no_foul_mean = 37.6
        year.foul_mean = 2.15
        year.auto_mean = 16.05
        year.teleop_mean = 18.77
        year.endgame_mean = 2.77
        year.rp_1_mean = 0.06
        year.rp_2_mean = 0.01
        year.tiebreaker_mean = 0.1
        year.comp_1_mean = 2.65
        year.comp_2_mean = 2.76
        year.comp_3_mean = 13.4
        year.comp_4_mean = 9.19
        year.comp_5_mean = 18.77
        year.comp_6_mean = 2.6
        year.comp_7_mean = 2.73
        year.comp_8_mean = 9.35
        year.comp_9_mean = 29.45
        year.comp_10_mean = 0.95
        year.comp_11_mean = 11.95
        year.comp_12_mean = 32.18
        year.comp_13_mean = 1.4
        year.comp_14_mean = 1.35
        year.comp_15_mean = 0.01
        year.comp_16_mean = 0.01
        year.comp_17_mean = 0.02
        return year

    year.score_mean, year.score_sd = get_mean_sd(
        lambda m: m.red_score, lambda m: m.blue_score
    )
    if year.year >= 2016:
        year.no_foul_mean, _ = get_mean_sd(lambda m: m.red_no_foul, lambda m: m.blue_no_foul)  # type: ignore
        year.foul_mean, _ = get_mean_sd(lambda m: m.red_foul, lambda m: m.blue_foul)
        year.auto_mean, _ = get_mean_sd(lambda m: m.red_auto, lambda m: m.blue_auto)
        year.teleop_mean, _ = get_mean_sd(lambda m: m.red_teleop, lambda m: m.blue_teleop)  # type: ignore
        year.endgame_mean, _ = get_mean_sd(lambda m: m.red_endgame, lambda m: m.blue_endgame)  # type: ignore
        year.rp_1_mean, _ = get_mean_sd(lambda m: m.red_rp_1, lambda m: m.blue_rp_1)
        year.rp_2_mean, _ = get_mean_sd(lambda m: m.red_rp_2, lambda m: m.blue_rp_2)
        year.tiebreaker_mean, _ = get_mean_sd(lambda m: m.red_tiebreaker, lambda m: m.blue_tiebreaker)  # type: ignore
        for i in range(1, 19):
            mean, _ = get_mean_sd(
                lambda m: getattr(m, f"red_comp_{i}"),
                lambda m: getattr(m, f"blue_comp_{i}"),
            )
            setattr(year, f"comp_{i}_mean", mean)

    return year
