import numpy as np


def getMatchTiebreakers(m, year):
    if year == 2016:
        return [m["red_1"], m["blue_1"]]
    elif year == 2017:
        return [m["red_auto"], m["blue_auto"]]
    elif year == 2018:
        return [m["red_endgame"], m["blue_endgame"]]
    elif year == 2019:
        return [m["red_2"], m["blue_2"]]
    elif year == 2020:
        return [m["red_auto"], m["blue_auto"]]


# oprs - score, auto, teleop, 1, 2, endgame, fouls, no_fouls
def getOPRTiebreakers(oprs, red, blue, year):
    red_oprs = np.sum([oprs[t] for t in red], axis=0)
    blue_oprs = np.sum([oprs[t] for t in blue], axis=0)
    if year == 2016:
        return [red_oprs[3], blue_oprs[3]]
    if year == 2017:
        return [red_oprs[1], blue_oprs[1]]
    if year == 2018:
        return [red_oprs[5], blue_oprs[5]]
    if year == 2019:
        return [red_oprs[4], blue_oprs[4]]
    if year == 2020:
        return [red_oprs[1], blue_oprs[1]]


def get_tiebreakers(year, matches, teams):
    out = {}
    for team in teams:
        out[team] = np.zeros(shape=(len(matches) + 1, 1))
        out[team][0] = 0

    for i, m in enumerate(matches):
        red, blue = m["red"], m["blue"]
        red_tie, blue_tie = getMatchTiebreakers(m, year)

        for t in teams:
            out[t][i + 1] = out[t][i]
            if t in red:
                out[t][i + 1][0] += red_tie  # noqa 702
            elif t in blue:
                out[t][i + 1][0] += blue_tie  # noqa 702

    return out
