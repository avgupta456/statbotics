import numpy as np
from scipy.stats import exponnorm  # type: ignore


def sigmoid(x: float) -> float:
    return 1 / (1 + np.exp(-4 * (x - 0.5)))


def inv_sigmoid(x: float) -> float:
    return 0.5 + np.log(x / (1 - x)) / 4


distrib = exponnorm(1.6, -0.3, 0.2)  # type: ignore


def ppf(x: float) -> float:
    return distrib.ppf(x)  # type: ignore
