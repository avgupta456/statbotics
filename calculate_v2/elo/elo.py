'''Standard Deviation of Individual Alliance Score, Week 1 of Given Year'''
sd = {2002: 11.3, 2003: 31.4, 2004: 33.7, 2005: 15.5, 2006: 20.5, 2007: 32.9,
      2008: 24.4, 2009: 21.0, 2010: 2.7, 2011: 28.4, 2012: 15.5, 2013: 31.1,
      2014: 49.3, 2015: 33.2, 2016: 27.5, 2017: 70.6, 2018: 106.9, 2019: 17.1,
      2020: 58.3}


# rating for 2002
def start_rating():
    return 1500


# standard mean reversion rating
def mean_reversion():
    return 1450


def existing_rating(team_1yr, team_2yr):
    rating = 0.70 * team_1yr + 0.30 * team_2yr  # previous seasons elo
    rating = 0.80 * rating + 0.20 * mean_reversion()  # to avoid drift
    return round(rating, 3)


def update_rating(year, red, blue, red_score, blue_score, playoff):
    win_margin = (red_score - blue_score)/sd[year]
    pred_win_margin = 4/1000*(sum(red)-sum(blue))
    k = 4 if playoff == 1 else 12

    for i in range(len(red)):
        red[i] = round(red[i] + k*(win_margin-pred_win_margin), 3)
    for i in range(len(blue)):
        blue[i] = round(blue[i] - k*(win_margin-pred_win_margin), 3)

    return red, blue


def win_probability(red, blue):
    return 1/(10**((sum(blue)-sum(red))/400)+1)
