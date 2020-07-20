import numpy as np


def win_prob(red, blue):
    if isinstance(red, list):
        red = sum(red)  # noqa 701
    if isinstance(red, dict):
        red = sum(red.values())  # noqa 701
    if isinstance(blue, list):
        blue = sum(blue)  # noqa 701
    if isinstance(blue, dict):
        blue = sum(blue.values())  # noqa 701
    return 1 / (10 ** ((blue - red) / 400) + 1)


def win_margin(red, blue, sd_score):
    if isinstance(red, list):
        red = sum(red)  # noqa 701
    if isinstance(red, dict):
        red = sum(red.values())  # noqa 701
    if isinstance(blue, list):
        blue = sum(blue)  # noqa 701
    if isinstance(blue, dict):
        blue = sum(blue.values())  # noqa 701
    return (red - blue) * sd_score / 250


def get_elos(matches, teams, team_stats, team_matches):
    out = {}
    for team in teams:
        out[team] = np.zeros(shape=(len(matches) + 1, 1))
        out[team][0] = team_stats[team]["elo_start"]

    for i, m in enumerate(matches):
        team_m = team_matches[m["key"]]
        for t in teams:
            out[t][i + 1] = out[t][i]
            if t in team_m:
                out[t][i + 1] = team_m[t]
    return out
