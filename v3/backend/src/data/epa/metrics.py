from typing import Callable, List, Optional

from src.db.models import Match

from src.data.utils import objs_type


def calc_binary_metrics(
    matches: List[Match],
    get_pred: Callable[[Match], Optional[float]],
    get_actual: Callable[[Match], Optional[float]],
    filter: Callable[[Match], bool],
):
    matches = [m for m in matches if filter(m)]
    count, acc, mse = 0, 0, 0
    for match in matches:
        pred = get_pred(match)
        actual = get_actual(match)

        if actual is None or pred is None:
            continue

        count += 1
        acc += (pred > 0.5) == (actual > 0.5)
        mse += (pred - actual) ** 2

    return count, acc, mse


def process_year(objs: objs_type) -> objs_type:
    matches = list(objs[4].values())

    # YEAR
    year = objs[0]

    count, acc, mse = calc_binary_metrics(
        matches,
        lambda m: m.epa_win_prob,
        lambda m: {"red": 1, "blue": 0, "tie": 0.5, None: None}[m.get_winner()],
        lambda m: m.status == "Completed",
    )

    year.count = count
    year.epa_acc = round(acc / count, 4)
    year.epa_mse = round(mse / count, 4)

    # EVENTS

    return objs
