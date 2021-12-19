import numpy as np


def get_rps(event, matches, teams):
    out = {}
    for team in teams:
        out[team] = np.zeros(shape=(len(matches) + 1, 1))
        out[team][0] = 0

    for i, m in enumerate(matches):
        red, blue = m["red"], m["blue"]
        red_rps = m["red_rp_1"] + m["red_rp_2"]
        blue_rps = m["blue_rp_1"] + m["blue_rp_2"]
        if m["winner"] == "red":
            red_rps += 2
        elif m["winner"] == "blue":
            blue_rps += 2
        else:
            red_rps, blue_rps = red_rps + 1, blue_rps + 1

        for t in teams:
            out[t][i + 1] = out[t][i]
            if t in red:
                out[t][i + 1][0] += red_rps
            elif t in blue:
                out[t][i + 1][0] += blue_rps

    return out
