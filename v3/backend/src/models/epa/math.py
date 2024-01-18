# import math
from functools import lru_cache
from typing import Any, Optional, Tuple

import numpy as np
import scipy.stats  # type: ignore

"""
# NOTE: Unused in favor of t_prob_gt_0()
def normal_prob_gt_0(mean: float, sd: float) -> float:
    return 0.5 * (1 + math.erf(mean / (sd * np.sqrt(2))))
"""

# 5 represent the asymptote of the sample size of the moving average
# 1 / (1 - p) where p = 0.8, the decay rate of the EWMA. By the Bayesian
# conjugate prior of the normal distribution, the posterior predictive of
# the mean is a t-distribution with equal degrees of freedom


@lru_cache(maxsize=None)
def get_t_distrib(int_n: int = 5000) -> Any:
    n = int_n / 1000
    return scipy.stats.t(n)


def t_prob_gt_0(mean: float, sd: float, n: Any = 5) -> float:
    t_distrib = get_t_distrib(int(n * 1000))
    return t_distrib.cdf(mean / sd)  # type: ignore


MAX_SKEW = 0.95


@lru_cache(maxsize=None)
def _get_skew_normal_95_conf_interval(skew_int: int) -> Tuple[Any, Any]:
    skew = skew_int / 1e3  # for better caching

    # https://en.wikipedia.org/wiki/Skew_normal_distribution
    abs_skew = abs(skew)
    sign_skew = 1 if skew >= 0 else -1

    c = np.pi / 2
    numerator = abs_skew ** (2 / 3)
    denominator = numerator + ((4 - np.pi) / 2) ** (2 / 3)
    delta = sign_skew * np.sqrt(c * numerator / denominator)
    a = delta / np.sqrt(1 - delta**2)

    # assumes mean 0, var 1 (rescale after)
    omega = 1 / np.sqrt(1 - 2 * delta**2 / np.pi)
    xi = -omega * delta * np.sqrt(2 / np.pi)

    skewnorm_distrib = scipy.stats.skewnorm(a, loc=xi, scale=omega)
    return skewnorm_distrib.interval(0.95)  # type: ignore


def get_skew_normal_95_conf_interval(
    mean: float, sd: float, skew: float, n: float = 1, n_digits: Optional[int] = None
) -> Tuple[Any, Any]:
    lower, upper = _get_skew_normal_95_conf_interval(int(skew * 1e3))
    lower = mean + lower * sd / np.sqrt(n)
    upper = mean + upper * sd / np.sqrt(n)
    if n_digits is not None:
        lower = np.round(lower, n_digits)  # type: ignore
        upper = np.round(upper, n_digits)  # type: ignore
    return lower, upper  # type: ignore


class SkewNormal:
    # all inputs are 1d np arrays, does not handle covariance between variables
    # skew is only computed on total, and assumed equal for all variables
    def __init__(self, mean: Any, var: Any, skew_index: int):
        self.mean = mean
        self.var = var
        self.skew = 0
        self.n = 1

        self.skew_i = skew_index

    @staticmethod
    def update_mean(mean: Any, x: Any, alpha: float) -> Any:
        new_mean = x
        return (1 - alpha) * mean + alpha * new_mean

    @staticmethod
    def update_var(var: Any, mean: Any, new_mean: Any, x: Any, alpha: float) -> Any:
        # https://stats.stackexchange.com/questions/111851/standard-deviation-of-an-exponentially-weighted-mean
        new_var = (x - mean) * (x - new_mean)
        return (1 - alpha) * var + alpha * new_var

    @staticmethod
    def update_skew(
        skew: float,
        new_var: float,
        mean: float,
        new_mean: float,
        x: float,
        alpha: float,
    ) -> Any:
        # Note: unsure of exact derivation of this formula
        # https://stats.stackexchange.com/questions/6874/exponential-weighted-moving-skewness-kurtosis
        new_skew = (x - mean) * (x - new_mean) * (x - new_mean) / (new_var ** (3 / 2))
        new_skew = (1 - alpha) * skew + alpha * new_skew
        return min(max(new_skew, -MAX_SKEW), MAX_SKEW)

    def add_obs(self, x: Any, percent: float, weight: float) -> None:
        mean, var, skew, n = self.mean, self.var, self.skew, self.n
        skew_i = self.skew_i

        new_mean = self.update_mean(mean, x, percent)
        new_var = self.update_var(var, mean, new_mean, x, percent)
        new_skew = self.update_skew(
            skew, new_var[skew_i], mean[skew_i], new_mean[skew_i], x[skew_i], percent
        )
        new_n = n * (1 - percent) + 1

        self.mean = weight * new_mean + (1 - weight) * mean
        self.var = new_var * weight + (1 - weight) * var
        self.skew = new_skew * weight + (1 - weight) * skew
        self.n = new_n * weight + (1 - weight) * n

    def get_distrib(self) -> Any:
        # https://en.wikipedia.org/wiki/Skew_normal_distribution
        skew = self.skew
        abs_skew = abs(skew)
        sign_skew = 1 if skew >= 0 else -1

        c = np.pi / 2
        numerator = abs_skew ** (2 / 3)
        denominator = numerator + ((4 - np.pi) / 2) ** (2 / 3)
        delta = sign_skew * np.sqrt(c * numerator / denominator)
        a = delta / np.sqrt(1 - delta**2)

        # assumes mean 0, var 1 (rescale after)
        omega = 1 / np.sqrt(1 - 2 * delta**2 / np.pi)
        xi = -omega * delta * np.sqrt(2 / np.pi)

        distrib = scipy.stats.skewnorm(a, loc=xi, scale=omega)

        return distrib

    def conf_interval(self) -> Tuple[Any, Any]:
        return get_skew_normal_95_conf_interval(self.mean, np.sqrt(self.var), self.skew)

    def mean_conf_interval(self) -> Any:
        return get_skew_normal_95_conf_interval(
            self.mean, np.sqrt(self.var), self.skew, self.n
        )

    def __repr__(self) -> str:
        return f"SkewNormal(mean={self.mean}, var={self.var}, skew={self.skew})"


# used for 2018 switch/scale power
# -2 instead of -4 since both alliances contribute
def zero_sigmoid(x: float) -> float:
    return 1 / (1 + np.exp(-2 * x))


def inv_zero_sigmoid(x: float) -> float:
    return np.log(x / (1 - x)) / 2


# used for ranking point system
def unit_sigmoid(x: float) -> float:
    return 1 / (1 + np.exp(-4 * (x - 0.5)))


def inv_unit_sigmoid(x: float) -> float:
    return 0.5 + np.log(x / (1 - x)) / 4
