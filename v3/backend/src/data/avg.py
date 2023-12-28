import statistics
from typing import Callable, List, Optional, Tuple

from src.db.models import Alliance, Year
from src.types.enums import MatchStatus
from src.utils.utils import r


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
            return 0, 0

        mean = statistics.mean(clean_arr)
        sd = statistics.pstdev(clean_arr)
        return r(mean, 2), r(sd, 2)

    N = len(week_one_alliances)
    if year.year == 2024 and N < 100:
        year.score_mean, year.score_sd = 30, 10
        year.no_foul_mean = 30
        year.foul_mean = 0
        year.auto_mean = 10
        year.teleop_mean = 10
        year.endgame_mean = 10
        year.rp_1_mean = 0.5
        year.rp_2_mean = 0.5
        year.tiebreaker_mean = 0
        year.comp_1_mean = 3
        year.comp_2_mean = 3
        year.comp_3_mean = 3
        year.comp_4_mean = 3
        year.comp_5_mean = 3
        year.comp_6_mean = 3
        year.comp_7_mean = 3
        year.comp_8_mean = 3
        year.comp_9_mean = 3
        year.comp_10_mean = 3
        return year

    year.score_mean, year.score_sd = get_mean_sd(lambda a: a.score)
    if year.year >= 2016:
        year.no_foul_mean, _ = get_mean_sd(lambda a: a.no_foul)
        year.foul_mean, _ = get_mean_sd(lambda a: a.foul)
        year.auto_mean, _ = get_mean_sd(lambda a: a.auto)
        year.teleop_mean, _ = get_mean_sd(lambda a: a.teleop)
        year.endgame_mean, _ = get_mean_sd(lambda a: a.endgame)
        year.rp_1_mean, _ = get_mean_sd(lambda a: a.rp_1)
        year.rp_2_mean, _ = get_mean_sd(lambda a: a.rp_2)
        year.tiebreaker_mean, _ = get_mean_sd(lambda a: a.tiebreaker)
        for i in range(1, 19):
            mean, _ = get_mean_sd(lambda a: getattr(a, f"comp_{i}"))
            setattr(year, f"comp_{i}_mean", mean)

    return year
