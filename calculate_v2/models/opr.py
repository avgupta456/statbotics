import numpy as np


def score(match, alliance): return match.red_score if alliance == "red" else match.blue_score  # noqa 501
def event_score(event): return event.opr_start
def year_score(year): return year.score_mean

def auto(match, alliance): return match.red_auto if alliance == "red" else match.blue_auto  # noqa 501
def event_auto(event): return event.opr_auto
def year_auto(year): return year.auto_mean

def teleop(match, alliance): return match.red_teleop if alliance == "red" else match.blue_teleop  # noqa 501
def event_teleop(event): return event.opr_teleop
def year_teleop(year): return year.teleop_mean

def one(match, alliance): return match.red_1 if alliance == "red" else match.blue_1  # noqa 501
def event_one(event): return event.opr_1
def year_one(year): return year.one_mean

def two(match, alliance): return match.red_2 if alliance == "red" else match.blue_2  # noqa 501
def event_two(event): return event.opr_2
def year_two(year): return year.two_mean

def endgame(match, alliance): return match.red_endgame if alliance == "red" else match.blue_endgame  # noqa 501
def event_endgame(event): return event.opr_endgame
def year_endgame(year): return year.endgame_mean

def foul(match, alliance): return -match.blue_fouls if alliance == "red" else -match.red_fouls  # noqa 501
def event_foul(event): return event.opr_fouls
def year_foul(year): return year.foul_mean

def no_foul(match, alliance): return match.red_no_fouls if alliance == "red" else match.blue_no_fouls  # noqa 501
def event_no_foul(event): return event.opr_no_fouls
def year_no_foul(year): return year.no_foul_mean


def computeOPR(input, output, year, year_mean):
    MTM = np.matmul(input.T, input)
    MTs = np.matmul(input.T, output)

    try:
        out = np.matmul(np.linalg.inv(MTM), MTs)
    except np.linalg.LinAlgError:
        # if singular (not enough matches, etc)
        out = computeAverages(input, output, year)

    # if highly unstable, handles foul oprs
    if year_mean > 0 and np.min(out) < -year_mean/(2 if year <= 2004 else 3):
        out = computeAverages(input, output, year)
    elif year_mean < 0 and np.min(out) > -year_mean/(2 if year <= 2004 else 3):
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
        avg = sum(scores)/len(scores)/TM
        out[i][0] = round(float(avg), 2) if len(scores) > 0 else 0
    return out


def opr_base(event, event_func=event_score):
    team_events = {}
    for team_event in event.team_events:
        team_events[team_event.getTeam()] = team_event

    # case of only playoffs
    if len(event.getMatches(playoffs=False)) == 0:
        teams, out = set(), {}
        for m in event.matches:
            [teams.add(t) for t in m.getRed()]
            [teams.add(t) for t in m.getBlue()]
        teams = list(teams)
        for t in teams:
            out[t] = [round(event_func(team_events[t]), 2)]
        early_exit = True
        return out, early_exit, 0, 0, 0, 0, 0, 0, 0

    teams, out = set(), {}
    match_objs = sorted(event.getMatches(playoffs=False))
    for m in match_objs:
        [teams.add(t) for t in m.getRed()]
        [teams.add(t) for t in m.getBlue()]
    teams = list(teams)
    M, T = len(match_objs), len(teams)
    input = np.zeros(shape=(2*M, T), dtype="float")
    output = np.zeros(shape=(2*M, 1), dtype="float")
    early_exit = False
    return out, early_exit, team_events, teams, match_objs, M, T, input, output


def get_OPR(event, func=score, event_func=event_score, year_func=year_score):
    mean_score = year_func(event.year)
    out, early_exit, team_events, teams, match_objs, \
        M, T, input, output = opr_base(event, event_func)
    if early_exit:
        return out

    for i in range(T):
        out[teams[i]] = [0]
    for i in range(M):
        m = match_objs[i]
        for t in m.getRed():
            input[2*i][teams.index(t)] = 1
        output[2*i] = func(m, "red")
        for t in m.getBlue():
            input[2*i+1][teams.index(t)] = 1
        output[2*i+1] = func(m, "blue")
        oprs = computeOPR(input, output, event.getYear(), mean_score)
        for j in range(len(teams)):
            out[teams[j]].append(round(float(oprs[j][0]), 2))
    for team in out:
        print(team, out[team][::5])
    return out


def get_xOPR(event, func=score, event_func=event_score, year_func=year_score):
    mean_score = year_func(event.year)
    out, early_exit, team_events, teams, match_objs, \
        M, T, input, output = opr_base(event, event_func)
    if early_exit:
        return out

    for i in range(M):
        m = match_objs[i]
        for t in m.getRed():
            input[2*i][teams.index(t)] = 1
        output[2*i][0] = sum([event_func(team_events[t]) for t in m.getRed()])
        for t in m.getBlue():
            input[2*i+1][teams.index(t)] = 1
        output[2*i+1][0] = sum([event_func(team_events[t]) for t in m.getBlue()])  # noqa 502
    oprs = computeOPR(input, output, event.getYear(), mean_score)
    for i in range(T):
        out[teams[i]] = [round(float(oprs[i][0]), 2)]
    for i in range(M):
        m = match_objs[i]
        output[2*i][0] = func(m, "red")
        output[2*i+1][0] = func(m, "blue")
        oprs = computeOPR(input, output, event.getYear(), mean_score)
        for j in range(T):
            out[teams[j]].append(round(float(oprs[j][0]), 2))
    return out


def get_ixOPR(event, func=score, event_func=event_score, year_func=year_score):
    mean_score = year_func(event.year)
    out, early_exit, team_events, teams, match_objs, \
        M, T, input, output = opr_base(event, event_func)
    if early_exit:
        return out

    iterations = 2  # experimentally chosen
    for i in range(M):
        m = match_objs[i]
        for t in m.getRed():
            input[2*i][teams.index(t)] = 1
        output[2*i][0] = sum([event_func(team_events[t]) for t in m.getRed()])
        for t in m.getBlue():
            input[2*i+1][teams.index(t)] = 1
        output[2*i+1][0] = sum([event_func(team_events[t]) for t in m.getBlue()])  # noqa 502
    oprs = computeOPR(input, output, event.getYear(), mean_score)
    for i in range(T):
        out[teams[i]] = [round(float(oprs[i][0]), 2)]
    for i in range(M):
        m = match_objs[i]
        output[2*i][0] = func(m, "red")
        output[2*i+1][0] = func(m, "blue")
        oprs = computeOPR(input, output, event.getYear(), mean_score)
        for j in range(iterations - 1):
            temp = output.copy()
            for k in range(i, M):
                red, blue = match_objs[k].getRed(), match_objs[k].getBlue()
                temp[2*k][0] = sum([oprs[teams.index(t)] for t in red])
                temp[2*k+1][0] = sum([oprs[teams.index(t)] for t in blue])
            oprs = computeOPR(input, temp, event.getYear(), mean_score)
        for j in range(T):
            out[teams[j]].append(round(float(oprs[j][0]), 2))
    return out


def opr_auto(event):
    return get_ixOPR(event, auto, event_auto, year_auto)


def opr_teleop(event):
    return get_ixOPR(event, teleop, event_teleop, year_teleop)


def opr_one(event):
    return get_ixOPR(event, one, event_one, year_one)


def opr_two(event):
    return get_ixOPR(event, two, event_two, year_two)


def opr_endgame(event):
    return get_ixOPR(event, endgame, event_endgame, year_endgame)


def opr_foul(event):
    return get_ixOPR(event, foul, event_foul, year_foul)


def opr_no_foul(event):
    return get_ixOPR(event, no_foul, event_no_foul, year_no_foul)


def win_prob(red, blue, year, sd_score):
    return 1/(10**(5/8*(blue-red)/sd_score)+1)
