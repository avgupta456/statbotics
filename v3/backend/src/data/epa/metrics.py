import math
from collections import defaultdict
from typing import Callable, Dict, List, Optional, Tuple

from src.data.utils import objs_type
from src.db.models import Match
from src.types.enums import MatchStatus, MatchWinner
from src.utils.utils import r
from src.constants import EPS


def calc_binary_metrics(
    matches: List[Match],
    get_pred: Callable[[Match], Optional[float]],
    get_actual: Callable[[Match], Optional[float]],
    filter: Callable[[Match], bool],
) -> Tuple[int, float, float, float]:
    matches = [m for m in matches if filter(m)]
    count, conf, acc, mse = 0, 0, 0, 0
    for match in matches:
        pred = get_pred(match)
        actual = get_actual(match)

        if actual is None or pred is None:
            continue

        pred = min(max(pred, EPS), 1 - EPS)

        count += 1
        conf += max(pred, 1 - pred)
        acc += (pred > 0.5) == (actual > 0.5)
        mse += (pred - actual) ** 2

    return count, conf, acc, mse


def calc_rp_metrics(
    matches: List[Match], rp: str, filter: Callable[[Match], bool]
) -> Tuple[int, float, float, float, float]:
    matches = [m for m in matches if filter(m)]
    count, error, acc, ll, tp, fp, fn = 0, 0, 0, 0, 0, 0, 0
    for match in matches:
        if match.elim:
            continue
        for alliance in ["red", "blue"]:
            pred = getattr(match, f"epa_{alliance}_{rp}_pred")
            actual = getattr(match, f"{alliance}_{rp}")

            if actual is None or pred is None:
                continue

            pred = min(max(pred, EPS), 1 - EPS)

            count += 1
            error += pred - actual
            acc += (pred > 0.5) == (actual > 0.5)
            ll += actual * math.log(pred) + (1 - actual) * math.log(1 - pred)

            tp += actual == 1 and pred >= 0.5
            fp += actual == 0 and pred >= 0.5
            fn += actual == 1 and pred < 0.5

    prec = tp / max(1, (tp + fp))
    rec = tp / max(1, (tp + fn))
    f1 = 2 * prec * rec / (prec + rec) if prec + rec > 0 else 0

    return count, error, acc, ll, f1


def process_year(objs: objs_type) -> objs_type:
    matches = list(objs[4].values())

    event_matches_dict: Dict[str, List[Match]] = defaultdict(list)
    for match in matches:
        event_matches_dict[match.event].append(match)

    # YEAR
    year = objs[0]

    def get_pred(match: Match) -> Optional[float]:
        return match.epa_win_prob

    def get_actual(match: Match) -> Optional[float]:
        return {
            MatchWinner.RED: 1,
            MatchWinner.BLUE: 0,
            MatchWinner.TIE: 0.5,
            None: None,
        }[match.get_winner()]

    def get_season(match: Match) -> bool:
        return not match.offseason and match.status == MatchStatus.COMPLETED

    count, conf, acc, mse = calc_binary_metrics(
        matches, get_pred, get_actual, get_season
    )
    rp_1_count, rp_1_error, rp_1_acc, rp_1_ll, rp_1_f1 = calc_rp_metrics(
        matches, "rp_1", get_season
    )
    rp_2_count, rp_2_error, rp_2_acc, rp_2_ll, rp_2_f1 = calc_rp_metrics(
        matches, "rp_2", get_season
    )

    year.count = count
    year.rp_count = rp_1_count
    if count > 0:
        year.epa_conf = r(conf / count, 4)
        year.epa_acc = r(acc / count, 4)
        year.epa_mse = r(mse / count, 4)

    if rp_1_count > 0:
        year.epa_rp_1_error = r(rp_1_error / rp_1_count, 4)
        year.epa_rp_1_acc = r(rp_1_acc / rp_1_count, 4)
        year.epa_rp_1_ll = r(rp_1_ll / rp_1_count, 4)
        year.epa_rp_1_f1 = r(rp_1_f1, 4)

        year.epa_rp_2_error = r(rp_2_error / rp_2_count, 4)
        year.epa_rp_2_acc = r(rp_2_acc / rp_2_count, 4)
        year.epa_rp_2_ll = r(rp_2_ll / rp_2_count, 4)
        year.epa_rp_2_f1 = r(rp_2_f1, 4)

    # EVENTS

    for event in objs[2].values():
        ms = event_matches_dict[event.key]
        count, conf, acc, mse = calc_binary_metrics(
            ms, get_pred, get_actual, get_season  # TODO: revisit 'get_season'
        )
        rp_1_count, rp_1_error, rp_1_acc, rp_1_ll, rp_1_f1 = calc_rp_metrics(
            ms, "rp_1", get_season
        )
        rp_2_count, rp_2_error, rp_2_acc, rp_2_ll, rp_2_f1 = calc_rp_metrics(
            ms, "rp_2", get_season
        )
        event.count = count
        event.rp_count = rp_1_count
        if count > 0:
            event.epa_conf = r(conf / count, 4)
            event.epa_acc = r(acc / count, 4)
            event.epa_mse = r(mse / count, 4)

        if rp_1_count > 0:
            event.epa_rp_1_error = r(rp_1_error / rp_1_count, 4)
            event.epa_rp_1_acc = r(rp_1_acc / rp_1_count, 4)
            event.epa_rp_1_ll = r(rp_1_ll / rp_1_count, 4)
            event.epa_rp_1_f1 = r(rp_1_f1, 4)

            event.epa_rp_2_error = r(rp_2_error / rp_2_count, 4)
            event.epa_rp_2_acc = r(rp_2_acc / rp_2_count, 4)
            event.epa_rp_2_ll = r(rp_2_ll / rp_2_count, 4)
            event.epa_rp_2_f1 = r(rp_2_f1, 4)

    return objs
