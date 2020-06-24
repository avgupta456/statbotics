import numpy as np
import scipy.linalg


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

def foul(match, alliance): return match.blue_fouls if alliance == "red" else match.red_fouls  # noqa 501
def event_foul(event): return event.opr_fouls
def year_foul(year): return year.foul_mean

def no_foul(match, alliance): return match.red_no_fouls if alliance == "red" else match.blue_no_fouls  # noqa 501
def event_no_foul(event): return event.opr_no_fouls
def year_no_foul(year): return year.no_foul_mean


def computeOPR(input, output, year, year_mean):
    try:
        A = np.matmul(input.T, input)
        Y = np.matmul(input.T, output)
        out = scipy.linalg.lstsq(A, Y, overwrite_a=True, overwrite_b=True,
                                 check_finite=True, lapack_driver='gelsy')[0]
        # inv = np.linalg.inv(np.matmul(input.T, input))
        # out = np.matmul(inv, np.matmul(input.T, output))
    except scipy.linalg.LinAlgError or scipy.linalg.ValueError:
        # if singular (not enough matches, etc)
        out = computeAverages(input, output, year)
    # if highly unstable, handles foul oprs
    if np.min(out) < -year_mean/(2 if year <= 2004 else 3):
        out = computeAverages(input, output, year)
    return out


def computeAverages(input, output, year):
    T = input.shape[1]  # teams in event
    TM = (2 if year <= 2004 else 3)  # teams per alliance
    out = np.zeros(shape=(T, 1))
    for i in range(T):
        avg = np.mean(output[np.where(input[i][:] == 1)])/TM
        out[i][0] = round(float(avg), 2)
    return out


def opr_base(event, quals, playoffs, event_func=event_score):
    team_events = {}
    for team_event in event.team_events:
        team_events[team_event.getTeam()] = team_event

    # case of only playoffs
    if len(quals) == 0:
        teams, out = set(), {}
        for m in playoffs:
            [teams.add(t) for t in m.getRed()]
            [teams.add(t) for t in m.getBlue()]
        teams = list(teams)
        for t in teams:
            out[t] = [round(event_func(team_events[t]), 2)]
        early_exit = True
        return out, early_exit, 0, 0, 0, 0, 0, 0, 0

    teams, out = set(), {}
    for m in quals:
        [teams.add(t) for t in m.getRed()]
        [teams.add(t) for t in m.getBlue()]
    teams = list(teams)

    M, T = len(quals), len(teams)
    input = np.zeros(shape=(2*M, T), dtype="float")
    output = np.zeros(shape=(2*M, 1), dtype="float")
    early_exit = False
    return out, early_exit, team_events, teams, quals, M, T, input, output


def get_OPR_end(event, quals, playoffs, func=score,
                event_func=event_score, year_func=year_score):
    mean_score = year_func(event.year)
    out, early_exit, team_events, teams, match_objs, \
        M, T, input, output = opr_base(event, quals, playoffs, event_func)
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
    for i in range(len(teams)):
        out[teams[i]].append(round(float(oprs[i][0]), 2))
    return out


def get_OPR(event, quals, playoffs,
            func=score, event_func=event_score, year_func=year_score):
    mean_score = year_func(event.year)
    out, early_exit, team_events, teams, match_objs, \
        M, T, input, output = opr_base(event, quals, playoffs, event_func)
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
    return out


def get_xOPR(event, quals, playoffs,
             func=score, event_func=event_score, year_func=year_score):
    mean_score = year_func(event.year)
    out, early_exit, team_events, teams, match_objs, \
        M, T, input, output = opr_base(event, quals, playoffs, event_func)
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


def get_ixOPR(event, quals, playoffs,
              func=score, event_func=event_score, year_func=year_score):
    mean_score = year_func(event.year)
    out, early_exit, team_events, teams, match_objs, \
        M, T, input, output = opr_base(event, quals, playoffs, event_func)
    if early_exit:
        return out

    arr = []
    for i in range(M):
        red, blue = match_objs[i].getRed(), match_objs[i].getBlue()
        red = [teams.index(t) for t in red]
        blue = [teams.index(t) for t in blue]
        arr.append([red, blue])

    iterations = 2  # experimentally chosen
    for i in range(M):
        for t in arr[i][0]: input[2*i][t] = 1  # noqa 701
        for t in arr[i][1]: input[2*i+1][t] = 1  # noqa 701
        output[2*i][0] = sum([event_func(team_events[teams[t]]) for t in arr[i][0]])  # noqa 502
        output[2*i+1][0] = sum([event_func(team_events[teams[t]]) for t in arr[i][1]])  # noqa 502
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
                temp[2*k][0] = sum([oprs[i] for i in arr[k][0]])
                temp[2*k+1][0] = sum([oprs[i] for i in arr[k][1]])
            oprs = computeOPR(input, temp, event.getYear(), mean_score)
        for j in range(T):
            out[teams[j]].append(round(float(oprs[j][0]), 2))
    return out


def opr_auto(event, quals, playoffs):
    return get_OPR_end(event, quals, playoffs, auto, event_auto, year_auto)


def opr_teleop(event, quals, playoffs):
    return get_OPR_end(event, quals, playoffs, teleop, event_teleop, year_teleop)  # noqa 502


def opr_one(event, quals, playoffs):
    return get_OPR_end(event, quals, playoffs, one, event_one, year_one)


def opr_two(event, quals, playoffs):
    return get_OPR_end(event, quals, playoffs, two, event_two, year_two)


def opr_endgame(event, quals, playoffs):
    return get_OPR_end(event, quals, playoffs, endgame, event_endgame, year_endgame)  # noqa 502


def opr_foul(event, quals, playoffs):
    return get_OPR_end(event, quals, playoffs, foul, event_foul, year_foul)


def opr_no_foul(event, quals, playoffs):
    return get_OPR_end(event, quals, playoffs, no_foul, event_no_foul, year_no_foul)  # noqa 502


def opr_v1(event, quals, playoffs):
    return get_ixOPR(event, quals, playoffs, score, event_score, year_score)


def opr_v2(event, quals, playoffs):
    if event.year_id < 2016:
        return opr_v1(event)
    return get_ixOPR(event, quals, playoffs, no_foul, event_no_foul, year_no_foul)  # noqa 502


def win_prob(red, blue, year, sd_score):
    return 1/(10**(5/8*(blue-red)/sd_score)+1)
