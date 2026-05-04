# import math
from functools import lru_cache
from typing import Any, Tuple

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


class EPARating:
    # all inputs are 1d np arrays, does not handle covariance between variables
    def __init__(self, mean: Any):
        self.mean = mean

    @staticmethod
    def update_mean(mean: Any, x: Any, alpha: float) -> Any:
        new_mean = x
        return (1 - alpha) * mean + alpha * new_mean

    def add_obs(self, x: Any, percent: float, weight: float) -> None:
        mean = self.mean
        new_mean = self.update_mean(mean, x, percent)
        self.mean = weight * new_mean + (1 - weight) * mean

    def __repr__(self) -> str:
        return f"EPARating(mean={self.mean})"


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
