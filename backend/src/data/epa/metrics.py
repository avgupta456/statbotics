import math
from collections import defaultdict
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

from src.constants import EPS
from src.data.utils import objs_type
from src.db.models import Match
from src.types.enums import MatchStatus, MatchWinner
from src.utils.utils import r


def get_conf(pred: Any) -> float:
    return np.maximum(pred, 1 - pred).mean()  # type: ignore


def get_acc(pred: Any, actual: Any) -> float:
    return np.mean((pred > 0.5) == (actual > 0.5))  # type: ignore


def get_mse(pred: Any, actual: Any) -> float:
    return np.mean((pred - actual) ** 2)  # type: ignore


def get_error(pred: Any, actual: Any) -> float:
    return np.mean(pred - actual)  # type: ignore


def get_rmse(pred: Any, actual: Any) -> float:
    return math.sqrt(get_mse(pred, actual))


def get_ll(pred: Any, actual: Any) -> float:
    return -np.mean(actual * np.log(pred) + (1 - actual) * np.log(1 - pred))  # type: ignore


def get_f1(pred: Any, actual: Any) -> float:
    tp = np.sum(np.logical_and(pred >= 0.5, actual == 1))
    fp = np.sum(np.logical_and(pred >= 0.5, actual == 0))
    fn = np.sum(np.logical_and(pred < 0.5, actual == 1))

    prec = tp / max(1, (tp + fp))
    rec = tp / max(1, (tp + fn))
    return 2 * prec * rec / (prec + rec) if prec + rec > 0 else 0


outcome_dict = {
    MatchWinner.RED: 1,
    MatchWinner.BLUE: 0,
    MatchWinner.TIE: 0.5,
    None: None,
}


def win_prob_metrics(
    matches: List[Match],
) -> Tuple[int, Optional[float], Optional[float], Optional[float]]:
    preds: List[Any] = []
    actuals: List[Any] = []
    for match in matches:
        pred = match.epa_win_prob
        actual = outcome_dict[match.get_winner()]
        if actual is None or pred is None:
            continue

        pred = min(max(pred, EPS), 1 - EPS)
        preds.append(pred)
        actuals.append(actual)

    if len(preds) == 0:
        return 0, None, None, None

    preds = np.array(preds)  # type: ignore
    actuals = np.array(actuals)  # type: ignore

    conf = get_conf(preds)
    acc = get_acc(preds, actuals)
    mse = get_mse(preds, actuals)
    return len(preds), r(conf, 4), r(acc, 4), r(mse, 4)


def score_metrics(
    matches: List[Match],
) -> Tuple[int, Optional[float], Optional[float]]:
    preds: List[Any] = []
    actuals: List[Any] = []
    for match in matches:
        for pred, actual in [
            (match.epa_red_score_pred, match.red_score),
            (match.epa_blue_score_pred, match.blue_score),
        ]:
            if actual is None or pred is None:
                continue

            preds.append(pred)
            actuals.append(actual)

    if len(preds) == 0:
        return 0, None, None

    preds = np.array(preds)  # type: ignore
    actuals = np.array(actuals)  # type: ignore

    error = get_error(preds, actuals)
    rmse = get_rmse(preds, actuals)
    return len(preds), r(error, 4), r(rmse, 4)


def rp_metrics(
    matches: List[Match], rp: str
) -> Tuple[int, Optional[float], Optional[float]]:
    preds: List[Any] = []
    actuals: List[Any] = []
    for match in matches:
        if match.elim:
            continue
        for alliance in ["red", "blue"]:
            pred = getattr(match, f"epa_{alliance}_{rp}_pred")
            actual = getattr(match, f"{alliance}_{rp}")

            if actual is None or pred is None:
                continue

            pred = min(max(pred, EPS), 1 - EPS)
            preds.append(pred)
            actuals.append(actual)

    if len(preds) == 0:
        return 0, None, None

    preds = np.array(preds)  # type: ignore
    actuals = np.array(actuals)  # type: ignore

    error = get_error(preds, actuals)
    acc = get_acc(preds, actuals)
    return len(preds), r(error, 4), r(acc, 4)


def process_year(objs: objs_type) -> objs_type:
    matches = list(objs[4].values())

    event_matches_dict: Dict[str, List[Match]] = defaultdict(list)
    for match in matches:
        event_matches_dict[match.event].append(match)

    # YEAR
    year = objs[0]

    season_matches = [m for m in matches if m.status == MatchStatus.COMPLETED]
    champs_matches = [m for m in season_matches if m.week == 8]
    season_qual_matches = [m for m in season_matches if not m.elim]
    champs_qual_matches = [m for m in champs_matches if not m.elim]

    # win prob
    year.count, year.epa_conf, year.epa_acc, year.epa_mse = win_prob_metrics(
        season_matches
    )
    (
        year.champs_count,
        year.epa_champs_conf,
        year.epa_champs_acc,
        year.epa_champs_mse,
    ) = win_prob_metrics(champs_matches)

    # score
    _, year.epa_score_error, year.epa_score_rmse = score_metrics(season_matches)
    (
        _,
        year.epa_champs_score_error,
        year.epa_champs_score_rmse,
    ) = score_metrics(champs_matches)

    # rp
    (
        year.rp_count,
        year.epa_rp_1_error,
        year.epa_rp_1_acc,
    ) = rp_metrics(season_qual_matches, "rp_1")
    (
        _,
        year.epa_rp_2_error,
        year.epa_rp_2_acc,
    ) = rp_metrics(season_qual_matches, "rp_2")
    (
        _,
        year.epa_rp_3_error,
        year.epa_rp_3_acc,
    ) = rp_metrics(season_qual_matches, "rp_3")

    (
        year.champs_rp_count,
        year.epa_champs_rp_1_error,
        year.epa_champs_rp_1_acc,
    ) = rp_metrics(champs_qual_matches, "rp_1")
    (
        _,
        year.epa_champs_rp_2_error,
        year.epa_champs_rp_2_acc,
    ) = rp_metrics(champs_qual_matches, "rp_2")
    (
        _,
        year.epa_champs_rp_3_error,
        year.epa_champs_rp_3_acc,
    ) = rp_metrics(champs_qual_matches, "rp_3")

    # EVENTS

    for event in objs[2].values():
        ms = event_matches_dict[event.key]
        qual_ms = [m for m in ms if not m.elim]
        event.count, event.epa_conf, event.epa_acc, event.epa_mse = win_prob_metrics(ms)
        (
            _,
            event.epa_score_error,
            event.epa_score_rmse,
        ) = score_metrics(ms)
        (
            event.rp_count,
            event.epa_rp_1_error,
            event.epa_rp_1_acc,
        ) = rp_metrics(qual_ms, "rp_1")
        (
            _,
            event.epa_rp_2_error,
            event.epa_rp_2_acc,
        ) = rp_metrics(qual_ms, "rp_2")
        (
            _,
            event.epa_rp_3_error,
            event.epa_rp_3_acc,
        ) = rp_metrics(qual_ms, "rp_3")

    return objs
