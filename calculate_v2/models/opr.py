import numpy as np
import scipy.linalg


def score(match, alliance):
    if alliance == "red":
        return match.red_score
    return match.blue_score


def event_score(event):
    return event.opr_start


def get_stats(match, alliance):
    if alliance == "red":
        return [match.red_score, match.red_auto, match.red_teleop,
                match.red_1, match.red_2, match.red_endgame, match.blue_fouls,
                match.red_no_fouls]
    return [match.blue_score, match.blue_auto, match.blue_teleop, match.blue_1,
            match.blue_2, match.blue_endgame, match.red_fouls,
            match.blue_no_fouls]


def get_event_stats(event):
    return [event.opr_start, event.opr_auto, event.opr_teleop, event.opr_1,
            event.opr_2, event.opr_endgame, event.opr_fouls,
            event.opr_no_fouls]


def computeOPR(input, output, year, mean_score):
    try:
        A = np.matmul(input.T, input)
        Y = np.matmul(input.T, output)
        out = scipy.linalg.lstsq(A, Y, overwrite_a=True, overwrite_b=True,
                                 check_finite=True, lapack_driver='gelsy')[0]
    except scipy.linalg.LinAlgError or scipy.linalg.ValueError:
        # if singular (not enough matches, etc)
        out = computeAverages(input, output, year)
    # if highly unstable, handles foul oprs
    if np.min(out) < -mean_score/(2 if year <= 2004 else 3):
        out = computeAverages(input, output, year)
    return out


def computeAverages(input, output, year):
    T = input.shape[1]  # teams in event
    TM = (2 if year <= 2004 else 3)  # teams per alliance
    out = np.zeros(shape=(T, 1))
    for i in range(T):
        locs = np.where(input[i][:] == 1)
        avg = 0 if len(locs[0]) == 0 else np.mean(output[locs])/TM
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


def get_OPR_end(event, quals, playoffs, func=score, event_func=event_score):
    mean_score, year = event.year.score_mean, event.year.id
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

    oprs = computeOPR(input, output, year, mean_score)
    for i in range(len(teams)):
        out[teams[i]].append(oprs[i])
    return out


def get_OPR(event, quals, playoffs, func=score, event_func=event_score):
    mean_score, year = event.year.score_mean, event.year.id
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
        oprs = computeOPR(input, output, year, mean_score)
        for j in range(len(teams)):
            out[teams[j]].append(oprs[j])
    return out


def get_xOPR(event, quals, playoffs, func=score, event_func=event_score):
    mean_score, year = event.year.score_mean, event.year.id
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
    oprs = computeOPR(input, output, year, mean_score)
    for i in range(T):
        out[teams[i]] = [round(float(oprs[i][0]), 2)]
    for i in range(M):
        m = match_objs[i]
        output[2*i][0] = func(m, "red")
        output[2*i+1][0] = func(m, "blue")
        oprs = computeOPR(input, output, year, mean_score)
        for j in range(T):
            out[teams[j]].append(oprs[j])
    return out


def get_ixOPR(event, quals, playoffs, func=score, event_func=event_score):
    mean_score, year = event.year.score_mean, event.year.id
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
        out[teams[i]] = [oprs[i]]

    for i in range(M):
        m = match_objs[i]
        output[2*i][0] = func(m, "red")
        output[2*i+1][0] = func(m, "blue")
        oprs = computeOPR(input, output, year, mean_score)
        for j in range(iterations - 1):
            temp = output.copy()
            for k in range(i, M):
                temp[2*k][0] = sum([oprs[i] for i in arr[k][0]])
                temp[2*k+1][0] = sum([oprs[i] for i in arr[k][1]])
            oprs = computeOPR(input, temp, year, mean_score)
        for j in range(T):
            out[teams[j]].append(oprs[j])
    return out


def get_ixOPR_all(event, quals, playoffs):
    mean_score, year = event.year.score_mean, event.year.id
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
            out[t] = get_event_stats(team_events[t])
        return out

    teams, out = set(), {}
    for m in quals:
        [teams.add(t) for t in m.getRed()]
        [teams.add(t) for t in m.getBlue()]
    teams = list(teams)

    M, T = len(quals), len(teams)
    input = np.zeros(shape=(2*M, T), dtype="float")
    output = np.zeros(shape=(2*M, 8), dtype="float")
    match_objs = quals

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
        red = [get_event_stats(team_events[teams[t]]) for t in arr[i][0]]
        blue = [get_event_stats(team_events[teams[t]]) for t in arr[i][1]]
        output[2*i] = np.sum(red, axis=0)
        output[2*i+1] = np.sum(blue, axis=0)

    oprs = computeOPR(input, output, year, mean_score)

    for i in range(T):
        out[teams[i]] = [oprs[i]]

    for i in range(M):
        m = match_objs[i]
        output[2*i] = np.array(get_stats(m, "red"))
        output[2*i+1] = np.array(get_stats(m, "blue"))
        oprs = computeOPR(input, output, year, mean_score)
        for j in range(iterations - 1):
            temp = output.copy()
            for k in range(i, M):
                temp[2*k] = np.sum([oprs[i] for i in arr[k][0]], axis=0)
                temp[2*k+1] = np.sum([oprs[i] for i in arr[k][1]], axis=0)
            oprs = computeOPR(input, temp, year, mean_score)
        for j in range(T):
            out[teams[j]].append(oprs[j])
    return out


def opr_v1(event, quals, playoffs):
    return get_ixOPR(event, quals, playoffs)


def opr_v2(event, quals, playoffs):
    if event.year_id < 2016:
        return get_ixOPR(event, quals, playoffs)
    return get_ixOPR_all(event, quals, playoffs)


def win_prob(red, blue, year, sd_score):
    return 1/(10**(5/8*(blue-red)/sd_score)+1)
