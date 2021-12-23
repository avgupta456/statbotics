from typing import Dict, List, Tuple, Union

import numpy as np


# rating for 2002
def start_rating() -> int:
    return 1500


# standard mean reversion rating
def mean_reversion() -> int:
    return 1450


def existing_rating(team_1yr: float, team_2yr: float) -> float:
    rating = 0.70 * team_1yr + 0.30 * team_2yr  # previous seasons elo
    rating = 0.80 * rating + 0.20 * mean_reversion()  # to avoid drift
    return round(rating, 2)


def update_rating(
    sd_score: float,
    red: Dict[int, float],
    blue: Dict[int, float],
    red_score: int,
    blue_score: int,
    playoff: bool,
) -> Tuple[Dict[int, float], Dict[int, float]]:
    win_margin = (red_score - blue_score) / sd_score
    pred_win_margin = 4 / 1000 * (sum(red.values()) - sum(blue.values()))
    k = 4 if playoff == 1 else 12

    # prevents modification to inputs red and blue
    new_red: Dict[int, float] = {}
    new_blue: Dict[int, float] = {}
    for t in red:
        new_red[t] = round(red[t] + k * (win_margin - pred_win_margin), 2)
    for t in blue:
        new_blue[t] = round(blue[t] - k * (win_margin - pred_win_margin), 2)

    return new_red, new_blue


def win_prob(
    red: Union[List[float], Dict[int, float]],
    blue: Union[List[float], Dict[int, float]],
) -> float:
    red_sum, blue_sum = 0, 0
    if isinstance(red, list):
        red_sum = sum(red)
    if isinstance(red, dict):
        red_sum = sum(red.values())
    if isinstance(blue, list):
        blue_sum = sum(blue)
    if isinstance(blue, dict):
        blue_sum = sum(blue.values())
    return 1 / (10 ** ((blue_sum - red_sum) / 400) + 1)


def win_margin(
    red: Union[List[float], Dict[int, float]],
    blue: Union[List[float], Dict[int, float]],
    sd_score: float,
) -> float:
    red_sum, blue_sum = 0, 0
    if isinstance(red, list):
        red_sum = sum(red)
    if isinstance(red, dict):
        red_sum = sum(red.values())
    if isinstance(blue, list):
        blue_sum = sum(blue)
    if isinstance(blue, dict):
        blue_sum = sum(blue.values())
    return (red_sum - blue_sum) * sd_score / 250


def get_elos(event, quals):
    teams, out = [], {}
    for team_event in event.team_events:
        teams.append(team_event.team_id)
        out[teams[-1]] = np.zeros(shape=(len(quals) + 1, 1))
        curr = [team_event.elo_start]
        out[teams[-1]][0] = np.array(curr)

    for i, m in enumerate(quals):
        red, blue = m.getTeams()
        for t in teams:
            out[t][i + 1] = out[t][i]
        for team_match in m.team_matches:
            out[team_match.team_id][i + 1] = team_match.elo
    return out
