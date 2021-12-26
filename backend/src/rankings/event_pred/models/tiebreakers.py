from typing import Any, Dict, List, Tuple
import numpy as np


def get_match_tiebreakers(m: Dict[str, Any], year: int) -> Tuple[float, float]:
    if year == 2016:
        return (m["red_1"], m["blue_1"])
    elif year == 2017:
        return (m["red_auto"], m["blue_auto"])
    elif year == 2018:
        return (m["red_endgame"], m["blue_endgame"])
    elif year == 2019:
        return (m["red_2"], m["blue_2"])
    elif year == 2020:
        return (m["red_auto"], m["blue_auto"])
    return (m["red_score"], m["blue_score"])


# oprs - score, auto, teleop, 1, 2, endgame, fouls, no_fouls
def get_opr_tiebreakers(
    oprs: Dict[int, List[float]], red: List[int], blue: List[int], year: int
) -> Tuple[float, float]:
    red_oprs = np.sum([oprs[t] for t in red], axis=0)  # type: ignore
    blue_oprs = np.sum([oprs[t] for t in blue], axis=0)  # type: ignore
    if year == 2016:
        return (red_oprs[3], blue_oprs[3])
    if year == 2017:
        return (red_oprs[1], blue_oprs[1])
    if year == 2018:
        return (red_oprs[5], blue_oprs[5])
    if year == 2019:
        return (red_oprs[4], blue_oprs[4])
    if year == 2020:
        return (red_oprs[1], blue_oprs[1])
    return (red_oprs[0], blue_oprs[0])


def get_tiebreakers(
    year: int, matches: List[Dict[str, Any]], teams: List[int]
) -> Dict[int, List[float]]:
    out: Dict[int, Any] = {}
    for team in teams:
        out[team] = np.zeros(shape=(len(matches) + 1, 1))  # type: ignore
        out[team][0] = 0

    for i, m in enumerate(matches):
        red, blue = m["red"], m["blue"]
        red_tie, blue_tie = get_match_tiebreakers(m, year)

        for t in teams:
            out[t][i + 1] = out[t][i]
            if t in red:
                out[t][i + 1][0] += red_tie
            elif t in blue:
                out[t][i + 1][0] += blue_tie

    return out
