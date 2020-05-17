import trueskill
import itertools
import math

mu_env = 1500
sigma_env = 250

env = trueskill.TrueSkill(mu=mu_env, sigma=sigma_env, beta=sigma_env/2, tau=sigma_env/100,
    draw_probability=0, backend=None) #ignores draws temporarily

def new_rating():
    return env.create_rating()

def existing_rating(team):
    mu, sigma, alpha = team.get_rating_max_ts(), team.rating_ts.sigma, 0.25
    mu, sigma = (1-alpha) * mu + alpha * (mu_env-100), (1-alpha) * sigma + alpha * sigma_env
    return env.create_rating(mu=mu, sigma=sigma)

def update_rating(year, teams, match):
    r = (teams[match.red[0]].rating_ts, teams[match.red[1]].rating_ts, teams[match.red[2]].rating_ts)
    b = (teams[match.blue[0]].rating_ts, teams[match.blue[1]].rating_ts, teams[match.blue[2]].rating_ts)
    match.set_ratings_ts(r, b)

    if match.winner=="red": nr, nb = env.rate([r, b])
    elif match.winner=="blue": nb, nr = env.rate([b, r])
    else: nr, nb = env.rate([r, b], ranks=[0, 0])

    for i in range(3): teams[match.red[i]].set_rating_ts(nr[i])
    for i in range(3): teams[match.blue[i]].set_rating_ts(nb[i])

def win_probability(team1, team2):
    delta_mu = sum(r.mu for r in team1) - sum(r.mu for r in team2)
    sum_sigma = sum(r.sigma ** 2 for r in itertools.chain(team1, team2))
    denom = math.sqrt(6 * ((sigma_env/2) ** 2) + sum_sigma) #beta=250
    return trueskill.global_env().cdf(delta_mu/denom)
