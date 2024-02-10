import bisect
from functools import lru_cache
from typing import Callable, List

from scipy.interpolate import interp1d  # type: ignore

from src.constants import CURR_YEAR
from src.db.read import get_team_years as get_team_years_db


def epa_to_unitless_epa(epa: float, mean: float, sd: float) -> float:
    return 1500 + 250 * (epa - mean / 3) / sd


@lru_cache()
def get_epa_to_norm_epa_func(year: int) -> Callable[[float], float]:
    if year >= CURR_YEAR:
        return lambda epa: epa

    team_years = get_team_years_db(year=year)
    if len(team_years) == 0:
        raise ValueError("No team years found for year " + str(year))

    epas: List[float] = sorted(
        [ty.epa_end for ty in team_years if ty.epa_end is not None]
    )
    norm_epas: List[float] = sorted(
        [ty.norm_epa_end for ty in team_years if ty.norm_epa_end is not None]
    )
    spline = interp1d(norm_epas, epas, kind="linear", fill_value="extrapolate")  # type: ignore

    keys: List[float] = []
    values: List[float] = []
    for norm_epa in range(1200, 2400):
        keys.append(max(0, spline(norm_epa)))  # type: ignore
        values.append(norm_epa)  # type: ignore

    def epa_to_norm_epa(epa: float) -> float:
        try:
            return values[bisect.bisect_left(keys, epa)]
        except IndexError:
            return 2400

    return epa_to_norm_epa
