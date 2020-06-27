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


def update_rating(year, sd_score, red, blue, red_score, blue_score, playoff):
    win_margin = (red_score - blue_score)/sd_score
    pred_win_margin = 4/1000*(sum(red.values())-sum(blue.values()))
    k = 4 if playoff == 1 else 12

    for t in red:
        red[t] = round(red[t] + k*(win_margin-pred_win_margin), 2)
    for t in blue:
        blue[t] = round(blue[t] - k*(win_margin-pred_win_margin), 2)

    return red, blue


def win_prob(red, blue):
    return 1/(10**((sum(blue.values())-sum(red.values()))/400)+1)
