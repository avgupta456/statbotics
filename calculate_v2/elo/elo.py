from helper import constants


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


def update_rating(year, red, blue, red_score, blue_score, playoff):
    win_margin = (red_score - blue_score)/constants.sd[year]
    pred_win_margin = 4/1000*(sum(red)-sum(blue))
    k = 4 if playoff == 1 else 12

    for i in range(len(red)):
        red[i] = round(red[i] + k*(win_margin-pred_win_margin), 2)
    for i in range(len(blue)):
        blue[i] = round(blue[i] - k*(win_margin-pred_win_margin), 2)

    return red, blue


def win_probability(red, blue):
    return 1/(10**((sum(blue)-sum(red))/400)+1)
