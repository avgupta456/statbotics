import datetime
import os
import pickle
import time
from typing import Any

import numpy as np

e = np.e


def dump(path: str, data: Any):
    os.makedirs(path)
    with open(path, "wb") as f:
        pickle.dump(data, f)


def load(file: str):
    with open(file, "rb") as f:
        return pickle.load(f)


def dump_cache(path: str, data: Any):
    os.makedirs(path)
    with open(path + "/data.p", "wb") as f:
        pickle.dump(data, f)


def load_cache(file: str):
    with open(file + "/data.p", "rb") as f:
        return pickle.load(f)


def get_timestamp_from_str(date: str):
    timestamp = int(
        time.mktime(datetime.datetime.strptime(date, "%Y-%m-%d").timetuple())
    )
    return timestamp


def round_float(num: float, places: int = 2):
    return round(float(num), places)


# for ils
def logistic(n: float):
    return float(1 / (1 + e ** (-4 * (n - 0.5))))


def logistic_inv(n: float):
    if n <= 0:
        return -1 / 3
    return max(-1 / 3, float(-np.log((1 - n) / e ** 2 / n) / 4))
