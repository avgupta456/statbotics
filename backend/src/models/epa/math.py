import numpy as np

# 5 represent the asymptote of the sample size of the moving average
# 1 / (1 - p) where p = 0.8, the decay rate of the EWMA. By the Bayesian
# conjugate prior of the normal distribution, the posterior predictive of
# the mean is a t-distribution with equal degrees of freedom



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


# used for ranking point system
def unit_sigmoid(x: float) -> float:
    return 1 / (1 + np.exp(-4 * (x - 0.5)))


def inv_unit_sigmoid(x: float) -> float:
    return 0.5 + np.log(x / (1 - x)) / 4
