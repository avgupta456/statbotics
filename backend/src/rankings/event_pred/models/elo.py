from typing import Any, Dict, List, Union
import numpy as np


def win_prob(red_sum: float, blue_sum: float) -> float:
    return 1 / (10 ** ((blue_sum - red_sum) / 400) + 1)


def win_margin(red_sum: float, blue_sum: float, sd_score: float) -> float:
    return (red_sum - blue_sum) * sd_score / 250


def get_elos(
    matches: List[Dict[str, Any]],
    teams: List[int],
    team_stats: Dict[int, Dict[str, Union[int, float]]],
    team_matches: Dict[str, Dict[int, float]],
) -> Dict[int, Any]:
    out: Dict[int, Any] = {}
    for team in teams:
        out[team] = np.zeros(shape=(len(matches) + 1, 1))  # type: ignore
        out[team][0] = team_stats[team]["elo_start"]

    for i, m in enumerate(matches):
        team_m = team_matches[m["key"]]
        for t in teams:
            out[t][i + 1] = out[t][i]
            if t in team_m:
                out[t][i + 1] = team_m[t]
    return out
