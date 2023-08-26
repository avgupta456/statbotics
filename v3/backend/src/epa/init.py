from functools import lru_cache
from typing import Optional, Tuple

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
def get_constants(year: Year) -> Tuple[int, float, float, float, float, float]:
    num_teams = 2 if year.year <= 2004 else 3
    curr_mean = year.no_foul_mean or year.score_mean or 0
    curr_sd = year.score_sd or 0
    init_epa = curr_mean / num_teams - INIT_PENALTY * curr_sd

    rp_1_mean = year.rp_1_mean or sigmoid(MIN_RP_EPA * num_teams)
    rp_2_mean = year.rp_2_mean or sigmoid(MIN_RP_EPA * num_teams)

    rp_1_seed = inv_sigmoid(rp_1_mean) / num_teams
    rp_2_seed = inv_sigmoid(rp_2_mean) / num_teams

    return num_teams, curr_mean, curr_sd, init_epa, rp_1_seed, rp_2_seed


def norm_epa_to_next_season_epa(
    norm_epa: float, curr_mean: float, curr_sd: float, curr_num_teams: int
) -> float:
    return curr_mean / curr_num_teams + curr_sd * (norm_epa - NORM_MEAN) / NORM_SD


def get_init_epa(
    year: Year, team_year_1: Optional[TeamYear], team_year_2: Optional[TeamYear]
) -> Rating:
    num_teams, curr_mean, curr_sd, init_epa, rp_1_seed, rp_2_seed = get_constants(year)

    norm_epa_1 = norm_epa_2 = NORM_MEAN + -INIT_PENALTY * NORM_SD
    if team_year_1 is not None and team_year_1.norm_epa_end is not None:
        norm_epa_1 = team_year_1.norm_epa_end
    if team_year_2 is not None and team_year_2.norm_epa_end is not None:
        norm_epa_2 = team_year_2.norm_epa_end

    epa_1 = norm_epa_to_next_season_epa(norm_epa_1, curr_mean, curr_sd, num_teams)
    epa_2 = norm_epa_to_next_season_epa(norm_epa_2, curr_mean, curr_sd, num_teams)
    prev_epa = YEAR_ONE_WEIGHT * epa_1 + (1 - YEAR_ONE_WEIGHT) * epa_2
    curr_epa = (1 - MEAN_REVERSION) * prev_epa + MEAN_REVERSION * init_epa

    rp_factor = (prev_epa - curr_mean / num_teams) / (curr_sd)
    rp_1 = max(MIN_RP_EPA, rp_1_seed + 0.25 * rp_factor)
    rp_2 = max(MIN_RP_EPA, rp_2_seed + 0.25 * rp_factor)

    return Rating(curr_epa, rp_1, rp_2)
