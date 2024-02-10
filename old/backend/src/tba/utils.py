import os
import pickle
from typing import Any


def dump(path: str, data: Any):
    try:
        if not os.path.exists(path):
            os.makedirs(path)
        with open(path, "wb") as f:
            pickle.dump(data, f)
    except OSError:
        pass


def load(file: str):
    with open(file, "rb") as f:
        return pickle.load(f)


def dump_cache(path: str, data: Any):
    try:
        if not os.path.exists(path):
            os.makedirs(path)
        with open(path + "/data.p", "wb") as f:
            pickle.dump(data, f)
    except OSError:
        pass


def load_cache(file: str):
    with open(file + "/data.p", "rb") as f:
        return pickle.load(f)
