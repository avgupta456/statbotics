# type: ignore

from bisect import bisect_left
from typing import Callable, List

from scipy.stats import expon, exponnorm
from src.epa.constants import NORM_MEAN, NORM_SD


def epa_to_unitless_epa(epa: float, mean: float, sd: float) -> float:
    return NORM_MEAN + NORM_SD * (epa - mean / 3) / sd


# For converting EPA to Norm EPA
distrib = exponnorm(1.6, -0.3, 0.2)


def get_epa_to_norm_epa_func(year_epas: List[float]) -> Callable[[float], float]:
    total_N, cutoff_N = len(year_epas), int(len(year_epas) / 10)
    exponnorm_disrib = None if total_N == 0 else exponnorm(*exponnorm.fit(year_epas))
    expon_distrib = None if cutoff_N == 0 else expon(*expon.fit(year_epas[:cutoff_N]))

    def get_norm_epa(epa: float) -> float:
        i = bisect_left(year_epas, epa)
        exponnorm_value: float = exponnorm_disrib.cdf(epa)
        percentile = exponnorm_value
        if i < cutoff_N:
            expon_value: float = expon_distrib.cdf(epa)
            expon_value = 1 - cutoff_N / total_N * (1 - expon_value)
            # Linearly interpolate between the two distributions from 10% to 5%
            expon_frac = min(1, 2 * (cutoff_N - i) / cutoff_N)
            percentile = expon_frac * expon_value + (1 - expon_frac) * exponnorm_value
        out: float = distrib.ppf(percentile)
        return NORM_MEAN + NORM_SD * out

    return get_norm_epa
