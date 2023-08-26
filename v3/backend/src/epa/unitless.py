from typing import Callable, List

from scipy.stats import expon, exponnorm  # type: ignore
from src.epa.constants import NORM_MEAN, NORM_SD


def epa_to_unitless_epa(epa: float, mean: float, sd: float) -> float:
    return NORM_MEAN + NORM_SD * (epa - mean / 3) / sd


# For converting EPA to Norm EPA
distrib = exponnorm(1.6, -0.3, 0.2)  # type: ignore


def get_epa_to_norm_epa_func(year_epas: List[float]) -> Callable[[float, int], float]:
    total_N, cutoff_N = len(year_epas), int(len(year_epas) / 10)
    exponnorm_disrib = None if total_N == 0 else exponnorm(*exponnorm.fit(year_epas))  # type: ignore
    expon_distrib = None if cutoff_N == 0 else expon(*expon.fit(year_epas[:cutoff_N]))  # type: ignore

    def get_norm_epa(epa: float, i: int) -> float:
        exponnorm_value: float = exponnorm_disrib.cdf(epa)  # type: ignore
        percentile = exponnorm_value  # type: ignore
        if i < cutoff_N:
            expon_value: float = expon_distrib.cdf(epa)  # type: ignore
            expon_value = 1 - cutoff_N / total_N * (1 - expon_value)  # type: ignore
            # Linearly interpolate between the two distributions from 10% to 5%
            expon_frac = min(1, 2 * (cutoff_N - i) / cutoff_N)
            percentile = expon_frac * expon_value + (1 - expon_frac) * exponnorm_value  # type: ignore
        out: float = distrib.ppf(percentile)  # type: ignore
        return NORM_MEAN + NORM_SD * out  # type: ignore

    return get_norm_epa
