from functools import lru_cache
from typing import Optional, Tuple

from src.constants import EPS
from src.db.models import TeamYear, Year
from src.models.epa.constants import (
    INIT_PENALTY,
    MEAN_REVERSION,
    NORM_MEAN,
    NORM_SD,
    YEAR_ONE_WEIGHT,
)
from src.models.epa.math import SkewNormal, inv_unit_sigmoid


@lru_cache(maxsize=None)
def get_constants(year: Year) -> Tuple[int, float, float]:
    num_teams = 2 if year.year <= 2004 else 3
    curr_mean = year.no_foul_mean or year.score_mean or 0
    curr_sd = year.score_sd or 0

    return num_teams, curr_mean, curr_sd


def norm_epa_to_next_season_epa(
    norm_epa: float, curr_mean: float, curr_sd: float, curr_num_teams: int
) -> float:
    return max(
        curr_mean / curr_num_teams + curr_sd * (norm_epa - NORM_MEAN) / NORM_SD, 0
    )


def get_init_epa(
    year: Year, team_year_1: Optional[TeamYear], team_year_2: Optional[TeamYear]
) -> SkewNormal:
    num_teams, year_mean, year_sd = get_constants(year)

    INIT_EPA = NORM_MEAN - INIT_PENALTY * NORM_SD
    norm_epa_1 = norm_epa_2 = INIT_EPA
    if team_year_1 is not None and team_year_1.norm_epa is not None:
        norm_epa_1 = team_year_1.norm_epa
    if team_year_2 is not None and team_year_2.norm_epa is not None:
        norm_epa_2 = team_year_2.norm_epa

    prev_norm_epa = YEAR_ONE_WEIGHT * norm_epa_1 + (1 - YEAR_ONE_WEIGHT) * norm_epa_2
    curr_norm_epa = (1 - MEAN_REVERSION) * prev_norm_epa + MEAN_REVERSION * INIT_EPA

    curr_epa_z_score = (curr_norm_epa - NORM_MEAN) / NORM_SD

    # enforces starting EPA >= 0
    curr_epa_z_score = max(-year_mean / num_teams / year_sd, curr_epa_z_score)

    mean = year.get_mean_components()
    sd_frac = (year_sd or 0) / (year_mean or 1)
    sd = mean * sd_frac

    if year.year >= 2016:
        # For ranking points, take inv sigmoid since later we will apply sigmoid
        mean[4] = max(-1, inv_unit_sigmoid(max(EPS, min(1 - EPS, mean[4]))))
        mean[5] = max(-1, inv_unit_sigmoid(max(EPS, min(1 - EPS, mean[5]))))
        mean[6] = max(-1, inv_unit_sigmoid(max(EPS, min(1 - EPS, mean[6]))))

    curr_epa_mean = mean / num_teams + sd * curr_epa_z_score
    curr_epa_sd = sd / num_teams

    return SkewNormal(curr_epa_mean, curr_epa_sd, 0)
