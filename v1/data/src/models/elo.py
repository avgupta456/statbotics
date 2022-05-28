from typing import Dict, Optional, Tuple

START_RATING = 1450
MEAN_REVERSION = 1450


def existing_rating(team_1yr: Optional[float], team_2yr: Optional[float]) -> float:
    team_1yr = team_1yr or MEAN_REVERSION
    team_2yr = team_2yr or MEAN_REVERSION
    rating = 0.70 * team_1yr + 0.30 * team_2yr  # previous seasons elo
    rating = 0.80 * rating + 0.20 * MEAN_REVERSION  # to avoid drift
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
    k = 3 if playoff else 12

    # prevents modification to inputs red and blue
    new_red: Dict[int, float] = {}
    new_blue: Dict[int, float] = {}
    for t in red:
        new_red[t] = round(red[t] + k * (win_margin - pred_win_margin), 2)
    for t in blue:
        new_blue[t] = round(blue[t] - k * (win_margin - pred_win_margin), 2)

    return new_red, new_blue


def win_prob(red_sum: float, blue_sum: float) -> float:
    return 1 / (10 ** ((blue_sum - red_sum) / 400) + 1)


def win_margin(red_sum: float, blue_sum: float, sd_score: float) -> float:
    return (red_sum - blue_sum) * sd_score / 250
