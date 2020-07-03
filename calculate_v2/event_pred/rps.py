import numpy as np


def get_rps(event, quals, teams):
    out = {}
    for team in teams:
        out[team] = np.zeros(shape=(len(quals)+1, 1))
        out[team][0] = 0

    for i, m in enumerate(quals):
        red, blue = m.getTeams()
        red_rps, blue_rps = m.red_rp_1 + m.red_rp_2, m.blue_rp_1 + m.blue_rp_2
        if m.winner == "red": red_rps += 2  # noqa 702
        elif m.winner == "blue": blue_rps += 2  # noqa 702
        else: red_rps, blue_rps = red_rps + 1, blue_rps + 1  # noqa 702

        for t in teams:
            out[t][i+1] = out[t][i]
            if t in red: out[t][i+1][0] += red_rps  # noqa 702
            elif t in blue: out[t][i+1][0] += blue_rps  # noqa 702

    return out
