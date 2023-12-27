from collections import defaultdict
from typing import Callable, List, Optional, Dict

from src.db.models import Match

from src.types.enums import MatchStatus, MatchWinner
from src.data.utils import objs_type
from src.utils.utils import r


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
    # TODO: Refactor, add precision, recall, f1-score, ll?
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

    count, acc, mse = calc_binary_metrics(matches, get_pred, get_actual, get_season)
    year.count = count
    if count > 0:
        year.epa_acc = r(acc / count, 4)
        year.epa_mse = r(mse / count, 4)

    # EVENTS

    for event in objs[2].values():
        ms = event_matches_dict[event.key]
        count, acc, mse = calc_binary_metrics(ms, get_pred, get_actual, get_season)
        if count > 0:
            event.epa_acc = r(acc / count, 4)
            event.epa_mse = r(mse / count, 4)

    return objs
