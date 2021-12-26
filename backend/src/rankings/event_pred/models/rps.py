from typing import Any, Dict, List
import numpy as np


def get_rps(matches: List[Dict[str, Any]], teams: List[int]) -> Dict[int, Any]:
    out: Dict[int, Any] = {}
    for team in teams:
        out[team] = np.zeros(shape=(len(matches) + 1, 1))  # type: ignore
        out[team][0] = 0

    for i, m in enumerate(matches):
        red, blue = m["red"], m["blue"]
        red_rps = max(0, m["red_rp_1"] + m["red_rp_2"])  # handles pre 2016
        blue_rps = max(0, m["blue_rp_1"] + m["blue_rp_2"])  # handles pre 2016
        if m["winner"] == "red":
            red_rps += 2
        elif m["winner"] == "blue":
            blue_rps += 2
        else:
            red_rps += 1
            blue_rps += 1

        for t in teams:
            out[t][i + 1] = out[t][i]
            if t in red:
                out[t][i + 1][0] += red_rps
            elif t in blue:
                out[t][i + 1][0] += blue_rps

    return out
