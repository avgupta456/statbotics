import numpy as np
from helper import constants


def computeOPR(input, output, year):
    MTM = np.matmul(input.T, input)
    MTs = np.matmul(input.T, output)
    try:
        out = np.matmul(np.linalg.inv(MTM), MTs)
    except np.linalg.LinAlgError:
        out = computeAverages(input, output, year)
    neg_cutoff = -constants.mean[year]/(2 if year <= 2004 else 3)
    if np.min(out) < neg_cutoff:
        out = computeAverages(input, output, year)
    return out


def computeAverages(input, output, year):
    # matches (red, blue), teams
    M, T = input.shape[0], input.shape[1]
    TM = (2 if year <= 2004 else 3)  # teams per alliance
    out = np.zeros(shape=(T, 1))
    for i in range(T):
        scores = []
        for j in range(M):
            if input[j][i] == 1:
                scores.append(output[j])
        if len(scores) > 0:
            out[i] = sum(scores)/len(scores)/TM
        else:
            out[i] = 0
    return out


def get_OPR(event):
    teams, out = set(), {}
    match_objs = sorted(event.getMatches(playoffs=False))
    for m in match_objs:
        [teams.add(t) for t in m.getRed()]
        [teams.add(t) for t in m.getBlue()]
    teams = list(teams)
    for t in teams:
        out[t] = []
    M, T = len(match_objs), len(teams)
    input = np.zeros(shape=(2*M, T), dtype="float")
    output = np.zeros(shape=(2*M, 1), dtype="float")
    for i in range(M):
        m = match_objs[i]
        for t in m.getRed():
            input[2*i][teams.index(t)] = 1
        output[2*i] = m.red_score
        for t in m.getBlue():
            input[2*i+1][teams.index(t)] = 1
        output[2*i+1] = m.blue_score
        oprs = computeOPR(input, output, event.getYear())
        for j in range(len(teams)):
            out[teams[j]].append(round(float(oprs[j][0]), 2))
    for team in out:
        print(team, out[team][::5])
    return out


def get_xOPR(event):
    team_events, out = {}, []
    for team_event in event.team_events:
        team_events[team_event.getTeam()] = team_event
    teams, out = set(), {}
    match_objs = sorted(event.getMatches(playoffs=False))
    for m in match_objs:
        [teams.add(t) for t in m.getRed()]
        [teams.add(t) for t in m.getBlue()]
    teams = list(teams)
    for t in teams:
        out[t] = []
    M, T = len(match_objs), len(teams)
    input = np.zeros(shape=(2*M, T), dtype="float")
    output = np.zeros(shape=(2*M, 1), dtype="float")
    for i in range(M):
        m = match_objs[i]
        for t in m.getRed():
            input[2*i][teams.index(t)] = 1
        output[2*i][0] = sum([team_events[t].opr_start for t in m.getRed()])
        for t in m.getBlue():
            input[2*i+1][teams.index(t)] = 1
        output[2*i+1][0] = sum([team_events[t].opr_start for t in m.getBlue()])
    oprs = computeOPR(input, output, event.getYear())
    for i in range(M):
        m = match_objs[i]
        output[2*i][0] = m.red_score
        output[2*i+1][0] = m.blue_score
        oprs = computeOPR(input, output, event.getYear())
        for j in range(T):
            out[teams[j]].append(round(float(oprs[j][0]), 2))
    return out


def get_ixOPR(event):
    iterations = 2
    team_events, out = {}, []
    for team_event in event.team_events:
        team_events[team_event.getTeam()] = team_event
    teams, out = set(), {}
    match_objs = sorted(event.getMatches(playoffs=False))
    for m in match_objs:
        [teams.add(t) for t in m.getRed()]
        [teams.add(t) for t in m.getBlue()]
    teams = list(teams)
    for t in teams:
        out[t] = []
    M, T = len(match_objs), len(teams)
    input = np.zeros(shape=(2*M, T), dtype="float")
    output = np.zeros(shape=(2*M, 1), dtype="float")
    for i in range(M):
        m = match_objs[i]
        for t in m.getRed():
            input[2*i][teams.index(t)] = 1
        output[2*i][0] = sum([team_events[t].opr_start for t in m.getRed()])
        for t in m.getBlue():
            input[2*i+1][teams.index(t)] = 1
        output[2*i+1][0] = sum([team_events[t].opr_start for t in m.getBlue()])
    oprs = computeOPR(input, output, event.getYear())
    for i in range(M):
        m = match_objs[i]
        output[2*i][0] = m.red_score
        output[2*i+1][0] = m.blue_score
        oprs = computeOPR(input, output, event.getYear())
        for j in range(iterations - 1):
            temp = output.copy()
            for k in range(i, M):
                red, blue = match_objs[k].getRed(), match_objs[k].getBlue()
                temp[2*k][0] = sum([oprs[teams.index(t)] for t in red])
                temp[2*k+1][0] = sum([oprs[teams.index(t)] for t in blue])
            oprs = computeOPR(input, temp, event.getYear())
        for j in range(T):
            out[teams[j]].append(round(float(oprs[j][0]), 2))
    return out


def win_prob(red, blue, year):
    return 1/(10**(5/8*(blue-red)/constants.sd[year])+1)
