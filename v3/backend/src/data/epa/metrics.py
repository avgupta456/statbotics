from collections import defaultdict
from typing import Callable, List, Optional, Dict

from src.db.models import Match

from src.types.enums import MatchStatus, MatchWinner
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

    def get_qual(match: Match) -> bool:
        return get_season(match) and not match.elim

    def get_elim(match: Match) -> bool:
        return get_season(match) and match.elim

    def get_champs(match: Match) -> bool:
        return get_season(match) and match.week == 8

    def get_champs_qual(match: Match) -> bool:
        return get_champs(match) and not match.elim

    count, acc, mse = calc_binary_metrics(matches, get_pred, get_actual, get_season)
    year.count = count
    if count > 0:
        year.epa_acc = round(acc / count, 4)
        year.epa_mse = round(mse / count, 4)

    qual_count, qual_acc, qual_mse = calc_binary_metrics(
        matches, get_pred, get_actual, get_qual
    )
    year.qual_count = qual_count
    if qual_count > 0:
        year.epa_qual_acc = round(qual_acc / qual_count, 4)
        year.epa_qual_mse = round(qual_mse / qual_count, 4)

    elim_count, elim_acc, elim_mse = calc_binary_metrics(
        matches, get_pred, get_actual, get_elim
    )
    year.elim_count = elim_count
    if elim_count > 0:
        year.epa_elim_acc = round(elim_acc / elim_count, 4)
        year.epa_elim_mse = round(elim_mse / elim_count, 4)

    champs_count, champs_acc, champs_mse = calc_binary_metrics(
        matches, get_pred, get_actual, get_champs
    )
    year.champs_count = champs_count
    if champs_count > 0:
        year.epa_champs_acc = round(champs_acc / champs_count, 4)
        year.epa_champs_mse = round(champs_mse / champs_count, 4)

    red_rp_1_count, red_rp_1_acc, red_rp_1_mse = calc_binary_metrics(
        matches, lambda m: m.red_rp_1_pred, lambda m: m.red_rp_1, get_season
    )
    blue_rp_1_count, blue_rp_1_acc, blue_rp_1_mse = calc_binary_metrics(
        matches, lambda m: m.blue_rp_1_pred, lambda m: m.blue_rp_1, get_season
    )
    rp_1_count = red_rp_1_count + blue_rp_1_count
    rp_1_acc = red_rp_1_acc + blue_rp_1_acc
    rp_1_mse = red_rp_1_mse + blue_rp_1_mse
    year.rp_count = rp_1_count
    if rp_1_count > 0:
        year.rp_1_acc = round(rp_1_acc / rp_1_count, 4)
        year.rp_1_mse = round(rp_1_mse / rp_1_count, 4)

    red_rp_2_count, red_rp_2_acc, red_rp_2_mse = calc_binary_metrics(
        matches, lambda m: m.red_rp_2_pred, lambda m: m.red_rp_2, get_qual
    )
    blue_rp_2_count, blue_rp_2_acc, blue_rp_2_mse = calc_binary_metrics(
        matches, lambda m: m.blue_rp_2_pred, lambda m: m.blue_rp_2, get_qual
    )
    rp_2_count = red_rp_2_count + blue_rp_2_count
    rp_2_acc = red_rp_2_acc + blue_rp_2_acc
    rp_2_mse = red_rp_2_mse + blue_rp_2_mse
    if rp_2_count > 0:
        year.rp_2_acc = round(rp_2_acc / rp_2_count, 4)
        year.rp_2_mse = round(rp_2_mse / rp_2_count, 4)

    (
        champs_red_rp_1_count,
        champs_red_rp_1_acc,
        champs_red_rp_1_mse,
    ) = calc_binary_metrics(
        matches, lambda m: m.red_rp_1_pred, lambda m: m.red_rp_1, get_champs_qual
    )
    (
        champs_blue_rp_1_count,
        champs_blue_rp_1_acc,
        champs_blue_rp_1_mse,
    ) = calc_binary_metrics(
        matches, lambda m: m.blue_rp_1_pred, lambda m: m.blue_rp_1, get_champs_qual
    )
    champs_rp_1_count = champs_red_rp_1_count + champs_blue_rp_1_count
    champs_rp_1_acc = champs_red_rp_1_acc + champs_blue_rp_1_acc
    champs_rp_1_mse = champs_red_rp_1_mse + champs_blue_rp_1_mse
    year.rp_champs_count = champs_rp_1_count
    if champs_rp_1_count > 0:
        year.rp_1_champs_acc = round(champs_rp_1_acc / champs_rp_1_count, 4)
        year.rp_1_champs_mse = round(champs_rp_1_mse / champs_rp_1_count, 4)

    (
        champs_red_rp_2_count,
        champs_red_rp_2_acc,
        champs_red_rp_2_mse,
    ) = calc_binary_metrics(
        matches, lambda m: m.red_rp_2_pred, lambda m: m.red_rp_2, get_champs
    )
    (
        champs_blue_rp_2_count,
        champs_blue_rp_2_acc,
        champs_blue_rp_2_mse,
    ) = calc_binary_metrics(
        matches, lambda m: m.blue_rp_2_pred, lambda m: m.blue_rp_2, get_champs
    )
    champs_rp_2_count = champs_red_rp_2_count + champs_blue_rp_2_count
    champs_rp_2_acc = champs_red_rp_2_acc + champs_blue_rp_2_acc
    champs_rp_2_mse = champs_red_rp_2_mse + champs_blue_rp_2_mse
    if champs_rp_2_count > 0:
        year.rp_2_champs_acc = round(champs_rp_2_acc / champs_rp_2_count, 4)
        year.rp_2_champs_mse = round(champs_rp_2_mse / champs_rp_2_count, 4)

    # EVENTS

    for event in objs[2].values():
        ms = event_matches_dict[event.key]
        count, acc, mse = calc_binary_metrics(ms, get_pred, get_actual, get_season)
        if count > 0:
            event.epa_acc = round(acc / count, 4)
            event.epa_mse = round(mse / count, 4)

        red_rp_1_count, red_rp_1_acc, red_rp_1_mse = calc_binary_metrics(
            ms, lambda m: m.red_rp_1_pred, lambda m: m.red_rp_1, get_season
        )
        blue_rp_1_count, blue_rp_1_acc, blue_rp_1_mse = calc_binary_metrics(
            ms, lambda m: m.blue_rp_1_pred, lambda m: m.blue_rp_1, get_season
        )
        rp_1_count = red_rp_1_count + blue_rp_1_count
        rp_1_acc = red_rp_1_acc + blue_rp_1_acc
        rp_1_mse = red_rp_1_mse + blue_rp_1_mse
        if rp_1_count > 0:
            event.rp_1_acc = round(rp_1_acc / rp_1_count, 4)
            event.rp_1_mse = round(rp_1_mse / rp_1_count, 4)

        red_rp_2_count, red_rp_2_acc, red_rp_2_mse = calc_binary_metrics(
            ms, lambda m: m.red_rp_2_pred, lambda m: m.red_rp_2, get_qual
        )
        blue_rp_2_count, blue_rp_2_acc, blue_rp_2_mse = calc_binary_metrics(
            ms, lambda m: m.blue_rp_2_pred, lambda m: m.blue_rp_2, get_qual
        )
        rp_2_count = red_rp_2_count + blue_rp_2_count
        rp_2_acc = red_rp_2_acc + blue_rp_2_acc
        rp_2_mse = red_rp_2_mse + blue_rp_2_mse
        if rp_2_count > 0:
            event.rp_2_acc = round(rp_2_acc / rp_2_count, 4)
            event.rp_2_mse = round(rp_2_mse / rp_2_count, 4)

    return objs
