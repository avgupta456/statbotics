import math

from typing import Any, List, Tuple

import numpy as np

import scipy.stats  # type: ignore


def normal_prob_gt_0(mean: float, sd: float) -> float:
    # NOTE: Unused in favor of t_prob_gt_0()
    return 0.5 * (1 + math.erf(mean / (sd * np.sqrt(2))))


# 10 / 3 represent the asymptote of the sample size of the moving average
# 1 / (1 - p) where p = 0.7, the decay rate of the EWMA. By the Bayesian
# conjugate prior of the normal distribution, the posterior predictive of
# the mean is a t-distribution with equal degrees of freedom
distrib = scipy.stats.t(10 / 3)


def t_prob_gt_0(mean: float, sd: float) -> float:
    # TODO: precompute 1000 values of this function to speed up
    return distrib.cdf(mean / sd)  # type: ignore


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
        return (1 - alpha) * skew + alpha * new_skew

    def add_obs(self, x: Any, alpha: float, only_pos: bool = False) -> None:

        mean, var, skew, n = self.mean, self.var, self.skew, self.n
        skew_i = self.skew_i

        new_mean = self.update_mean(mean, x, alpha)
        new_var = self.update_var(var, mean, new_mean, x, alpha)
        new_skew = self.update_skew(
            skew, new_var[skew_i], mean[skew_i], new_mean[skew_i], x[skew_i], alpha
        )
        new_n = n * (1 - alpha) + 1

        if only_pos:
            new_mean = np.maximum(new_mean, 0)

        self.mean = new_mean
        self.var = new_var
        self.skew = new_skew
        self.n = new_n

    def get_distrib(self) -> Any:
        # https://en.wikipedia.org/wiki/Skew_normal_distribution
        skew = min(max(self.skew, -0.9), 0.9)
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

    def conf_interval(self, alpha: float = 0.95) -> Tuple[Any, Any]:
        distrib = self.get_distrib()
        lower, upper = distrib.interval(alpha)  # type: ignore
        lower = self.mean + lower * np.sqrt(self.var)
        upper = self.mean + upper * np.sqrt(self.var)
        return lower, upper

    def mean_conf_interval(self, alpha: float = 0.95) -> Any:
        distrib = self.get_distrib()
        lower, upper = distrib.interval(alpha)  # type: ignore
        lower = self.mean + lower * np.sqrt(self.var / self.n)
        upper = self.mean + upper * np.sqrt(self.var / self.n)
        return lower, upper

    def __repr__(self) -> str:
        return f"SkewNormal(mean={self.mean}, var={self.var}, skew={self.skew})"


def sigmoid(x: float) -> float:
    return 1 / (1 + np.exp(-2 * x))


def softmax(arr: List[float]) -> List[float]:
    exp_arr = [np.exp(x) for x in arr]
    sum_exp_arr = sum(exp_arr)
    return [x / sum_exp_arr for x in exp_arr]
