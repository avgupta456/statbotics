import statistics
from typing import Callable, List, Optional, Tuple

from src.db.models import Match, Year
from src.types.enums import MatchStatus
from src.utils.utils import r


def process_year(year: Year, matches: List[Match]) -> Year:
    week_one_matches = [
        m for m in matches if m.week == 1 and m.status == MatchStatus.COMPLETED
    ]

    def get_mean(
        red_accessor: Callable[[Match], Optional[float]],
        blue_accessor: Callable[[Match], Optional[float]],
    ) -> float:
        arr: List[Optional[float]] = [red_accessor(x) for x in week_one_matches] + [
            blue_accessor(x) for x in week_one_matches
        ]
        clean_arr: List[float] = [x for x in arr if x is not None]
        if len(clean_arr) < 1:
            return 0
        return r(statistics.mean(clean_arr), 2)

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

    year.score_mean, year.score_sd = get_mean_sd(
        lambda m: m.red_score, lambda m: m.blue_score
    )
    if year.year >= 2016:
        year.no_foul_mean, _ = get_mean_sd(
            lambda m: m.red_no_foul, lambda m: m.blue_no_foul
        )
        year.foul_mean = get_mean(lambda m: m.red_foul, lambda m: m.blue_foul)
        year.auto_mean = get_mean(lambda m: m.red_auto, lambda m: m.blue_auto)
        year.teleop_mean = get_mean(lambda m: m.red_teleop, lambda m: m.blue_teleop)
        year.endgame_mean = get_mean(lambda m: m.red_endgame, lambda m: m.blue_endgame)
        year.rp_1_mean = get_mean(lambda m: m.red_rp_1, lambda m: m.blue_rp_1)
        year.rp_2_mean = get_mean(lambda m: m.red_rp_2, lambda m: m.blue_rp_2)
        year.rp_3_mean = get_mean(lambda m: m.red_rp_3, lambda m: m.blue_rp_3)
        year.tiebreaker_mean = get_mean(
            lambda m: m.red_tiebreaker, lambda m: m.blue_tiebreaker
        )

        for i in range(1, 19):
            mean = get_mean(
                lambda m: getattr(m, f"red_comp_{i}"),
                lambda m: getattr(m, f"blue_comp_{i}"),
            )
            setattr(year, f"comp_{i}_mean", mean)

    if len(week_one_matches) < 100 and year.year == 2025:
        year.score_mean = 120
        year.score_sd = 50
        year.no_foul_mean = 120
        year.foul_mean = 0
        year.auto_mean = 26
        year.teleop_mean = 84
        year.endgame_mean = 10
        year.rp_1_mean = 0.5
        year.rp_2_mean = 0.5
        year.rp_3_mean = 0.5
        year.tiebreaker_mean = 0
        year.comp_1_mean = 6
        year.comp_2_mean = 4
        year.comp_3_mean = 20
        year.comp_4_mean = 20
        year.comp_5_mean = 70
        year.comp_6_mean = 6
        year.comp_7_mean = 6
        year.comp_8_mean = 6
        year.comp_9_mean = 6
        year.comp_10_mean = 90
        year.comp_11_mean = 2
        year.comp_12_mean = 6
        year.comp_13_mean = 2
        year.comp_14_mean = 8
        year.comp_15_mean = 14
        year.comp_16_mean = 28
        year.comp_17_mean = 10

    return year
