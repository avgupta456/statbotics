import numpy as np


def sigmoid(x: float) -> float:
    return 1 / (1 + np.exp(-4 * (x - 0.5)))


def inv_sigmoid(x: float) -> float:
    return 0.5 + np.log(x / (1 - x)) / 4
