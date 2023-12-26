from typing import Any, Tuple

import scipy.stats  # type: ignore

import numpy as np


class Logistic:
    def __init__(self, mean: float) -> None:
        self.mean = mean

    @staticmethod
    def update_mean(mean: float, x: float, alpha: float) -> float:
        new_mean = x
        return (1 - alpha) * mean + alpha * new_mean

    def add_obs(self, x: float, alpha: float) -> None:
        self.mean = self.update_mean(self.mean, x, alpha)


class SkewNormal:
    # all inputs are 1d np arrays, does not handle covariance between variables
    # skew is only computed on total, and assumed equal for all variables
    def __init__(self, mean: Any, var: Any, skew_index: int) -> None:
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

    def add_obs(self, x: Any, alpha: float) -> None:
        mean, var, skew, n = self.mean, self.var, self.skew, self.n
        skew_i = self.skew_i  # takes one measurement of skew for all variables

        new_mean = self.update_mean(mean, x, alpha)
        new_var = self.update_var(var, mean, new_mean, x, alpha)
        new_skew = self.update_skew(
            skew, new_var[skew_i], mean[skew_i], new_mean[skew_i], x[skew_i], alpha
        )
        new_n = n * (1 - alpha) + 1

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
    return 1 / (1 + np.exp(-4 * (x - 0.5)))


def inv_sigmoid(x: float) -> float:
    return 0.5 + np.log(x / (1 - x)) / 4
