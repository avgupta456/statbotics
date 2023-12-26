from functools import lru_cache
from typing import Optional, Tuple

from src.epa.math import SkewNormal
from src.db.models import TeamYear, Year
from src.epa.constants import (
    INIT_PENALTY,
    MEAN_REVERSION,
    MIN_RP_EPA,
    YEAR_ONE_WEIGHT,
    NORM_MEAN,
    NORM_SD,
)
from src.epa.math import inv_sigmoid, sigmoid
from src.epa.types import Rating


@lru_cache(maxsize=None)
def get_constants(year: Year) -> Tuple[int, float, float, float, float]:
    num_teams = 2 if year.year <= 2004 else 3
    curr_mean = year.no_foul_mean or year.score_mean or 0
    curr_sd = year.score_sd or 0

    rp_1_mean = year.rp_1_mean or sigmoid(MIN_RP_EPA * num_teams)
    rp_2_mean = year.rp_2_mean or sigmoid(MIN_RP_EPA * num_teams)

    rp_1_seed = inv_sigmoid(rp_1_mean) / num_teams
    rp_2_seed = inv_sigmoid(rp_2_mean) / num_teams

    return num_teams, curr_mean, curr_sd, rp_1_seed, rp_2_seed


def norm_epa_to_next_season_epa(
    norm_epa: float, curr_mean: float, curr_sd: float, curr_num_teams: int
) -> float:
    return max(
        curr_mean / curr_num_teams + curr_sd * (norm_epa - NORM_MEAN) / NORM_SD, 0
    )


def get_init_epa(
    year: Year, team_year_1: Optional[TeamYear], team_year_2: Optional[TeamYear]
) -> Rating:
    num_teams, curr_mean, curr_sd, _rp_1_seed, _rp_2_seed = get_constants(year)

    norm_epa_1 = norm_epa_2 = NORM_MEAN - INIT_PENALTY * NORM_SD
    if team_year_1 is not None and team_year_1.norm_epa is not None:
        norm_epa_1 = team_year_1.norm_epa
    if team_year_2 is not None and team_year_2.norm_epa is not None:
        norm_epa_2 = team_year_2.norm_epa

    prev_norm_epa = YEAR_ONE_WEIGHT * norm_epa_1 + (1 - YEAR_ONE_WEIGHT) * norm_epa_2
    curr_norm_epa = (1 - MEAN_REVERSION) * prev_norm_epa + MEAN_REVERSION * NORM_MEAN

    curr_epa_z_score = (curr_norm_epa - NORM_MEAN) / NORM_SD

    # enforces starting EPA >= 0
    curr_epa_z_score = max(-curr_mean / num_teams / curr_sd, curr_epa_z_score)

    mean = year.get_mean_components()
    sd = year.get_sd_components()

    curr_epa_mean = mean / num_teams + curr_sd * curr_epa_z_score
    curr_epa_sd = sd / num_teams

    return Rating(SkewNormal(curr_epa_mean, curr_epa_sd, 0), 0, 0)
