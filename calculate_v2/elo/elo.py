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
    return rating


def update_rating(year, teams, match):
    r, b = [], []
    for i in range(len(match.red)):
        r.append(teams[match.red[i]].rating)
    for i in range(len(match.blue)):
        b.append(teams[match.blue[i]].rating)

    match.set_ratings(r.copy(), b.copy())

    win_margin = (match.red_score - match.blue_score)/sd[year]
    pred_win_margin = 4/1000*(sum(r)-sum(b))

    k = 4 if match.playoff else 12
    for i in range(len(r)):
        r[i] = r[i] + k*(win_margin-pred_win_margin)
    for i in range(len(b)):
        b[i] = b[i] - k*(win_margin-pred_win_margin)

    match.set_ratings_end(r.copy(), b.copy())

    for i in range(len(r)):
        teams[match.red[i]].set_rating(r[i])
    for i in range(len(b)):
        teams[match.blue[i]].set_rating(b[i])


def win_probability(red, blue):
    return 1/(10**((sum(blue)-sum(red))/400)+1)
