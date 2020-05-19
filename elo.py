import trueskill
import itertools
import math

sd = {2005: 15.5, 2006: 20.5, 2007: 32.9, 2008: 24.4, 2009: 21.0,
    2010: 2.7, 2011: 28.4, 2012: 15.5, 2013: 31.1, 2014: 49.3, 2015: 33.2,
    2016: 27.5, 2017: 70.6, 2018: 106.9, 2019: 17.1, 2020: 44}

start_elo = 1500

def weightElo(r, b, year):
    w = [1, 1, 1] #weights[year]
    r.sort(), b.sort()
    red_w = 3*(w[0]*r[0]+w[1]*r[1]+w[2]*r[2])/sum(w)
    blue_w = 3*(w[0]*b[0]+w[1]*b[1]+w[2]*b[2])/sum(w)
    return 4/1000*(red_w-blue_w)

def new_rating():
    return start_elo

def existing_rating(team):
    rating, alpha = team.get_rating_max_elo(), 0.25
    rating = (1-alpha) * rating + alpha * (start_elo-100) #to avoid drift
    return rating

def update_rating(year, teams, match):
    r = (teams[match.red[0]].rating_elo, teams[match.red[1]].rating_elo, teams[match.red[2]].rating_elo)
    b = (teams[match.blue[0]].rating_elo, teams[match.blue[1]].rating_elo, teams[match.blue[2]].rating_elo)
    match.set_ratings_elo(r, b)

    win_margin = (match.red_score - match.blue_score)/sd[year]
    pred_win_margin = weightElo([r[0],r[1],r[2]], [b[0],b[1],b[2]], year)

    if(match.playoff): k = 4
    else: k = 16

    for i in range(3): teams[match.red[i]].set_rating_elo(r[i]+k*(win_margin-pred_win_margin))
    for i in range(3): teams[match.blue[i]].set_rating_elo(b[i]-k*(win_margin-pred_win_margin))

def win_probability(red, blue):
    return 1/(10**((sum(blue)-sum(red))/400)+1)
