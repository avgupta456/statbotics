import numpy as np


# rating for 2002
def start_rating():
    return 1500


# standard mean reversion rating
def mean_reversion():
    return 1450


def existing_rating(team_1yr, team_2yr):
    rating = 0.70 * team_1yr + 0.30 * team_2yr  # previous seasons elo
    rating = 0.80 * rating + 0.20 * mean_reversion()  # to avoid drift
    return round(rating, 2)


def update_rating(sd_score, red, blue, red_score, blue_score, playoff):
    win_margin = (red_score - blue_score) / sd_score
    pred_win_margin = 4 / 1000 * (sum(red.values()) - sum(blue.values()))
    k = 4 if playoff == 1 else 12

    for t in red:
        red[t] = round(red[t] + k * (win_margin - pred_win_margin), 2)
    for t in blue:
        blue[t] = round(blue[t] - k * (win_margin - pred_win_margin), 2)

    return red, blue


def win_prob(red, blue):
    if isinstance(red, list):
        red = sum(red)
    if isinstance(red, dict):
        red = sum(red.values())
    if isinstance(blue, list):
        blue = sum(blue)
    if isinstance(blue, dict):
        blue = sum(blue.values())
    return 1 / (10 ** ((blue - red) / 400) + 1)


def win_margin(red, blue, sd_score):
    if isinstance(red, list):
        red = sum(red)
    if isinstance(red, dict):
        red = sum(red.values())
    if isinstance(blue, list):
        blue = sum(blue)
    if isinstance(blue, dict):
        blue = sum(blue.values())
    return (red - blue) * sd_score / 250


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
