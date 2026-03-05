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

    if year.year == 2025:
        # have to manually set processor algae to 3 points instead of 6
        # this affects no_foul_mean, teleop_mean, comp_12 (processor_algae_points),
        # and comp 15 (total algae points)

        update = 3 * year.comp_11_mean  # from 6 to 3 points
        year.no_foul_mean -= update
        year.teleop_mean -= update
        year.comp_12_mean -= update
        year.comp_15_mean -= update

    if year.year == 2026:
        # Seeded from week 1 data (64 matches)
        # TODO: Remove once week 1 data is available
        year.score_mean = 108.34
        year.score_sd = 69.25
        year.no_foul_mean = 103.92
        year.foul_mean = 4.41
        year.auto_mean = 20.71
        year.teleop_mean = 59.89
        year.endgame_mean = 23.32
        year.rp_1_mean = 0.34
        year.rp_2_mean = 0.05
        year.rp_3_mean = 0.0
        year.tiebreaker_mean = 103.92  # no_foul_points
        year.comp_1_mean = 20.71  # auto_fuel
        year.comp_2_mean = 0.0  # auto_tower
        year.comp_3_mean = 3.77  # transition_fuel
        year.comp_4_mean = 30.98  # first_shift_fuel
        year.comp_5_mean = 25.14  # second_shift_fuel
        year.comp_6_mean = 59.89  # teleop_fuel
        year.comp_7_mean = 22.15  # endgame_fuel
        year.comp_8_mean = 1.17  # endgame_tower
        year.comp_9_mean = 102.75  # total_fuel
        year.comp_10_mean = 1.17  # total_tower

    return year
