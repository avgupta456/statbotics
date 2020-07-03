import datetime
import random

from helper import setup, utils
from models import opr as opr_model
from models import elo as elo_model
from event_pred import rps as rps_model
from event_pred import tiebreakers

TBA, SQL, SQL_Read, SQL_Write = setup.setup(False)
print("Finished Setup")


def getObjects(event_key, year):
    event = SQL_Read.getEvent_byKey(str(year)+event_key)
    quals = sorted(SQL_Read.getMatches(event=event.id, playoff=False))
    playoffs = sorted(SQL_Read.getMatches(event=event.id, playoff=True))
    sd_score = event.year.score_sd
    return event, quals, playoffs, sd_score


def getDicts(event, quals, playoffs):
    oprs, ils = opr_model.opr_v2(event, quals, playoffs)
    elos = elo_model.get_elos(event, quals)
    teams = oprs.keys()

    rps = rps_model.get_rps(event, quals, teams)
    ties = tiebreakers.get_tiebreakers(event, quals, teams)

    return oprs, ils, elos, rps, ties, teams


def getCurrStats(index, teams, oprs, ils, elos):
    oprs_curr, ils_curr, elos_curr = {}, {}, {}
    for team in teams:
        oprs_curr[team] = oprs[team][index]
        ils_curr[team] = ils[team][index]
        elos_curr[team] = elos[team][index]
    return oprs_curr, ils_curr, elos_curr


def getPreds(index, quals, oprs_curr, elos_curr, ils_curr, year, sd_score):
    team_matches = {}  # for each match i after index, red and blue teams
    preds = {}  # for each match i after index , win_prob, red rps, blue rps
    for i in range(index, len(quals)):
        m = quals[i]
        red, blue = m.getTeams()
        red_score = sum([utils.clean(oprs_curr[t][0]) for t in red])
        blue_score = sum([utils.clean(oprs_curr[t][0]) for t in blue])
        red_elo = sum([utils.clean(elos_curr[t]) for t in red])
        blue_elo = sum([utils.clean(elos_curr[t]) for t in blue])

        elo_prob = elo_model.win_prob(red_elo, blue_elo)
        elo_margin = elo_model.win_margin(red_elo, blue_elo, sd_score)
        opr_prob = opr_model.win_prob(red_score, blue_score, year, sd_score)
        win_prob = (elo_prob + opr_prob)/2
        win_margin = (elo_margin + (red_score - blue_score))/2
        red_score = (red_score + blue_score)/2 + win_margin/2
        blue_score = (red_score + blue_score)/2 - win_margin/2

        red_rp_1 = opr_model.rp_prob([ils_curr[t][0] for t in red])
        red_rp_2 = opr_model.rp_prob([ils_curr[t][1] for t in red])
        blue_rp_1 = opr_model.rp_prob([ils_curr[t][0] for t in blue])
        blue_rp_2 = opr_model.rp_prob([ils_curr[t][1] for t in blue])

        ties_pred = tiebreakers.getOPRTiebreakers(oprs_curr, red, blue, year)
        red_tie, blue_tie = ties_pred

        team_matches[i] = [red, blue]
        preds[i] = [round(red_score), round(blue_score), round(win_prob, 2),
                    round(red_rp_1, 2), round(red_rp_2, 2),
                    round(blue_rp_1, 2), round(blue_rp_2, 2),
                    round(red_tie, 2), round(blue_tie, 2)]

    return team_matches, preds


def meanSim(index, quals, teams, team_matches, preds, rps, ties):
    rps_out, ties_out = {}, {}
    for team in teams:
        rps_out[team] = rps[team][index][0]
        ties_out[team] = ties[team][index][0]
    for i in range(index, len(quals)):
        red, blue = team_matches[i]
        red_rps = preds[i][2] * 2 + preds[i][3] + preds[i][4]
        blue_rps = (1-preds[i][2]) * 2 + preds[i][5] + preds[i][6]
        for team in teams:
            if team in red:
                rps_out[team] += red_rps
                ties_out[team] += preds[i][7]
            if team in blue:
                rps_out[team] += blue_rps
                ties_out[team] += preds[i][8]
    return rps_out, ties_out


def singleSim(index, quals, teams, team_matches, preds, rps, mean_ties):
    rps_out, ranks_out = {}, {}
    for team in teams:
        rps_out[team] = rps[team][index][0]

    for i in range(index, len(quals)):
        red, blue = team_matches[i]
        red_rps, blue_rps = 0, 0
        if preds[i][2] > random.uniform(0, 1): red_rps += 2  # noqa 702
        else: blue_rps += 2  # noqa 702
        if preds[i][3] > random.uniform(0, 1): red_rps += 1  # noqa 702
        if preds[i][4] > random.uniform(0, 1): red_rps += 1  # noqa 702
        if preds[i][5] > random.uniform(0, 1): blue_rps += 1  # noqa 702
        if preds[i][6] > random.uniform(0, 1): blue_rps += 1  # noqa 702
        for team in red: rps_out[team] += red_rps  # noqa 702
        for team in blue: rps_out[team] += blue_rps  # noqa 702

    for team in teams: ranks_out[team] = [rps_out[team], mean_ties[team]]  # noqa 702
    ranks_out = sorted(ranks_out, key=lambda k: (ranks_out[k][0], ranks_out[k][1]))[::-1]  # noqa 502
    ranks_out = {ranks_out[i]: i+1 for i in range(len(ranks_out))}
    return rps_out, ranks_out


def indexSim(index, iterations, teams, quals, team_matches, preds, rps, ties):
    mean_rps, mean_ties = meanSim(index, quals, teams, team_matches, preds, rps, ties)  # noqa 502

    T = len(teams)
    avg_rps, ranks = {}, {}
    for team in teams:
        avg_rps[team] = 0
        ranks[team] = [0 for i in range(T)]

    for i in range(iterations):
        rps_ind, ranks_ind = singleSim(index, quals, teams, team_matches,
                                       preds, rps, mean_ties)
        for team in teams:
            avg_rps[team] += rps_ind[team]
            ranks[team][ranks_ind[team]-1] += 1

    avg_ranks = {}
    for team in teams:
        avg_rps[team] /= iterations
        ranks[team] = [freq/iterations for freq in ranks[team]]
        avg_ranks[team] = 1 + sum([i * ranks[team][i] for i in range(T)])
    return mean_rps, mean_ties, avg_rps, avg_ranks, ranks


def quickSim(year, event_key):
    event, quals, playoffs, sd_score = getObjects(event_key, year)
    oprs, ils, elos, rps, ties, teams = getDicts(event, quals, playoffs)
    out = {t: [] for t in teams}
    for i in range(len(quals)+1):
        oprs_c, ils_c, elos_c = getCurrStats(i, teams, oprs, ils, elos)
        team_matches, preds = getPreds(i, quals, oprs_c, elos_c, ils_c, year, sd_score)  # noqa 502
        mean_rps, mean_ties = meanSim(i, quals, teams, team_matches, preds, rps, ties)  # noqa 502
        for team in teams:
            out[team].append([mean_rps[team], mean_ties[team]])
    return out


def sim(year, event_key, iterations=100):
    event, quals, playoffs, sd_score = getObjects(event_key, year)
    oprs, ils, elos, rps, ties, teams = getDicts(event, quals, playoffs)
    out = {t: [] for t in teams}
    for i in range(len(quals)+1):
        oprs_c, ils_c, elos_c = getCurrStats(i, teams, oprs, ils, elos)
        team_matches, preds = getPreds(i, quals, oprs_c, elos_c, ils_c, year, sd_score)  # noqa 502
        mean_rps, mean_ties, avg_rps, avg_ranks, ranks = indexSim(
            i, iterations, teams, quals, team_matches, preds, rps, ties)
        for team in teams:
            out[team].append([mean_rps[team], mean_ties[team], avg_rps[team],
                              avg_ranks[team], ranks[team]])
    return out


year, event_key = 2020, 'ncwak'
index = 0  # after match 0 aka start of event

start = datetime.datetime.now()
out = sim(year, event_key)
for team in out.keys():
    print(team, round(out[team][index][0], 2), round(out[team][index][1], 2))
print()

end = datetime.datetime.now()
print(end-start)
