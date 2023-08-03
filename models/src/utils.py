from typing import Any, List
import os
import pickle

from rich.table import Table
from rich.console import Console

# CACHING


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


# TYPER

console = Console()


def print_table(headers: List[str], data: List[List[Any]]):
    table = Table(*headers)
    for row in data:
        table.add_row(*row)

    console.print(table)
