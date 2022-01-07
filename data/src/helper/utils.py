import os
import pickle
from typing import Any

import numpy as np


def dump(path: str, data: Any):
    if not os.path.exists(path):
        os.makedirs(path)
    with open(path, "wb") as f:
        pickle.dump(data, f)


def load(file: str):
    with open(file, "rb") as f:
        return pickle.load(f)


def dump_cache(path: str, data: Any):
    if not os.path.exists(path):
        os.makedirs(path)
    with open(path + "/data.p", "wb") as f:
        pickle.dump(data, f)


def load_cache(file: str):
    with open(file + "/data.p", "rb") as f:
        return pickle.load(f)


def get_team_year_id(team: int, year: int):
    return int(str(year) + str(team))


def get_team_event_id(team: int, event: int):
    return int("1" + str(event).zfill(4) + str(team))


def get_team_match_id(team: int, match: int):
    return int("1" + str(match).zfill(6) + str(team))


# for ils

e = np.e


def logistic(n: float):
    return float(1 / (1 + e ** (-4 * (n - 0.5))))


def logistic_inv(n: float):
    if n <= 0:
        return -1 / 3
    return max(-1 / 3, float(-np.log((1 - n) / e ** 2 / n) / 4))
