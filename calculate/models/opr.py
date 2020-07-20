import numpy as np
import scipy.linalg
from helper.utils import logistic


def score(match, alliance):
    if alliance == "red":
        return [match.red_score]
    return [match.blue_score]


def event_score(event):
    return [event.opr_start]


def all(match, alliance):
    if alliance == "red":
        return [
            match.red_score,
            match.red_auto,
            match.red_teleop,
            match.red_1,
            match.red_2,
            match.red_endgame,
            match.blue_fouls,
            match.red_no_fouls,
        ]
    return [
        match.blue_score,
        match.blue_auto,
        match.blue_teleop,
        match.blue_1,
        match.blue_2,
        match.blue_endgame,
        match.red_fouls,
        match.blue_no_fouls,
    ]


def event_all(event):
    return [
        event.opr_start,
        event.opr_auto,
        event.opr_teleop,
        event.opr_1,
        event.opr_2,
        event.opr_endgame,
        event.opr_fouls,
        event.opr_no_fouls,
    ]


def computeOPR(input, output, year, mean_score):
    try:
        A = np.matmul(input.T, input)
        Y = np.matmul(input.T, output)
        out = scipy.linalg.lstsq(
            A,
            Y,
            overwrite_a=True,
            overwrite_b=True,
            check_finite=True,
            lapack_driver="gelsy",
        )[0]
    except scipy.linalg.LinAlgError or scipy.linalg.ValueError:
        # if singular (not enough matches, etc)
        out = computeAverages(input, output, year)
    # if highly unstable, handles foul oprs
    if np.min(out) < -mean_score / (2 if year <= 2004 else 3):
        out = computeAverages(input, output, year)
    return out


def computeAverages(input, output, year):
    T, Y = input.shape[1], output.shape[1]  # teams in event
    TM = 2 if year <= 2004 else 3  # teams per alliance
    out = np.zeros(shape=(T, Y))
    for i in range(T):
        locs = np.where(input[i][:] == 1)
        if len(locs[0]) == 0:
            out[i] = np.array([0 * Y])
        else:
            out[i] = np.mean(output[locs], axis=0) / TM
    return out


def get_base(event, quals, playoffs, func, event_func):
    mean_score, year = event.year.score_mean, event.year.id
    team_events = {}
    for team_event in event.team_events:
        team_events[team_event.team_id] = team_event

    # case of only playoffs
    if len(quals) == 0:
        teams, out = set(), {}
        for m in playoffs:
            [teams.add(t) for t in m.getRed()]
            [teams.add(t) for t in m.getBlue()]
        teams = list(teams)
        for t in teams:
            out[t] = [event_func(team_events[t])]
        return True, 0, 0, 0, 0, 0, out, 0, 0, 0, 0, 0

    teams, out = set(), {}
    for m in quals:
        [teams.add(t) for t in m.getRed()]
        [teams.add(t) for t in m.getBlue()]
    teams = list(teams)

    M, T, Y = len(quals), len(teams), len(event_func(team_events[teams[0]]))
    input = np.zeros(shape=(2 * M, T), dtype="float")
    output = np.zeros(shape=(2 * M, Y), dtype="float")
    match_objs = quals

    arr = []
    for i in range(M):
        red, blue = match_objs[i].getRed(), match_objs[i].getBlue()
        red = [teams.index(t) for t in red]
        blue = [teams.index(t) for t in blue]
        arr.append([red, blue])

    return (
        False,
        team_events,
        teams,
        arr,
        input,
        output,
        out,
        T,
        M,
        match_objs,
        year,
        mean_score,
    )


def get_OPR(event, quals, playoffs, func=all, event_func=event_all):
    (
        quick_stop,
        team_events,
        teams,
        arr,
        input,
        output,
        out,
        T,
        M,
        match_objs,
        year,
        mean_score,
    ) = get_base(event, quals, playoffs, func, event_func)
    if quick_stop:
        return out

    oprs = computeOPR(input, output, year, mean_score)
    for i in range(T):
        out[teams[i]] = [oprs[i]]

    for i in range(M):
        m = match_objs[i]
        for t in arr[i][0]:
            input[2 * i][t] = 1
        for t in arr[i][1]:
            input[2 * i + 1][t] = 1
        output[2 * i] = np.array(func(m, "red"))
        output[2 * i + 1] = np.array(func(m, "blue"))
        oprs = computeOPR(input, output, year, mean_score)
        [out[teams[j]].append(oprs[j]) for j in range(T)]
    return out


def get_xOPR(event, quals, playoffs, func=all, event_func=event_all):
    (
        quick_stop,
        team_events,
        teams,
        arr,
        input,
        output,
        out,
        T,
        M,
        match_objs,
        year,
        mean_score,
    ) = get_base(event, quals, playoffs, func, event_func)
    if quick_stop:
        return out

    for i in range(M):
        for t in arr[i][0]:
            input[2 * i][t] = 1
        for t in arr[i][1]:
            input[2 * i + 1][t] = 1
        red = [event_func(team_events[teams[t]]) for t in arr[i][0]]
        blue = [event_func(team_events[teams[t]]) for t in arr[i][1]]
        output[2 * i] = np.sum(red, axis=0)
        output[2 * i + 1] = np.sum(blue, axis=0)

    oprs = computeOPR(input, output, year, mean_score)
    for i in range(T):
        out[teams[i]] = [oprs[i]]

    for i in range(M):
        m = match_objs[i]
        output[2 * i] = np.array(func(m, "red"))
        output[2 * i + 1] = np.array(func(m, "blue"))
        oprs = computeOPR(input, output, year, mean_score)
        [out[teams[j]].append(oprs[j]) for j in range(T)]
    return out


def get_ixOPR(event, quals, playoffs, func=all, event_func=event_all):
    (
        quick_stop,
        team_events,
        teams,
        arr,
        input,
        output,
        out,
        T,
        M,
        match_objs,
        year,
        mean_score,
    ) = get_base(event, quals, playoffs, func, event_func)
    if quick_stop:
        return out

    for i in range(M):
        for t in arr[i][0]:
            input[2 * i][t] = 1
        for t in arr[i][1]:
            input[2 * i + 1][t] = 1
        red = [event_func(team_events[teams[t]]) for t in arr[i][0]]
        blue = [event_func(team_events[teams[t]]) for t in arr[i][1]]
        output[2 * i] = np.sum(red, axis=0)
        output[2 * i + 1] = np.sum(blue, axis=0)

    oprs = computeOPR(input, output, year, mean_score)

    for i in range(T):
        out[teams[i]] = [oprs[i]]

    iterations = 2  # experimentally chosen
    for i in range(M):
        m = match_objs[i]
        output[2 * i] = np.array(func(m, "red"))
        output[2 * i + 1] = np.array(func(m, "blue"))
        oprs = computeOPR(input, output, year, mean_score)
        for j in range(iterations - 1):
            temp = output.copy()
            for k in range(i, M):
                temp[2 * k] = np.sum([oprs[i] for i in arr[k][0]], axis=0)
                temp[2 * k + 1] = np.sum([oprs[i] for i in arr[k][1]], axis=0)
            oprs = computeOPR(input, temp, year, mean_score)
        for j in range(T):
            out[teams[j]].append(oprs[j])
    return out


def get_ILS(event, quals):
    min_ils = -1 / 3
    teams, out = [], {}
    for team_event in event.team_events:
        teams.append(team_event.team_id)
        out[teams[-1]] = np.zeros(shape=(len(quals) + 1, 2))
        curr = [team_event.ils_1_start, team_event.ils_2_start]
        out[teams[-1]][0] = np.array(curr)

    for i, m in enumerate(quals):
        red, blue = m.getTeams()
        adjust_red_1 = (m.red_rp_1 - logistic(sum([out[r][i][0] for r in red]))) / 10
        adjust_red_2 = (m.red_rp_2 - logistic(sum([out[r][i][1] for r in red]))) / 10
        adjust_blue_1 = (m.blue_rp_1 - logistic(sum([out[b][i][0] for b in blue]))) / 10
        adjust_blue_2 = (m.blue_rp_2 - logistic(sum([out[b][i][1] for b in blue]))) / 10

        for t in teams:
            out[t][i + 1] = out[t][i]
            if t in red:
                out[t][i + 1][0] = max(min_ils, out[t][i][0] + adjust_red_1)
                out[t][i + 1][1] = max(min_ils, out[t][i][1] + adjust_red_2)
            elif t in blue:
                out[t][i + 1][0] = max(min_ils, out[t][i][0] + adjust_blue_1)
                out[t][i + 1][1] = max(min_ils, out[t][i][1] + adjust_blue_2)

    return out


def opr_v1(event, quals, playoffs):
    return get_ixOPR(event, quals, playoffs, score, event_score)


def opr_v2(event, quals, playoffs):
    OPRs = get_ixOPR(event, quals, playoffs, all, event_all)
    ILS = get_ILS(event, quals)
    return OPRs, ILS


def opr_standalone(SQL_Read, event):
    quals = sorted(SQL_Read.getMatches(event=event.id, playoff=False))
    playoffs = sorted(SQL_Read.getMatches(event=event.id, playoff=True))
    OPRs = get_ixOPR(event, quals, playoffs, all, event_all)
    ILS = get_ILS(event, quals)
    return OPRs, ILS


def win_prob(red, blue, year, sd_score):
    if isinstance(red, list):
        red = sum(red)
    if isinstance(red, dict):
        red = sum(red.values())
    if isinstance(blue, list):
        blue = sum(blue)
    if isinstance(blue, dict):
        blue = sum(blue.values())
    return 1 / (10 ** (5 / 8 * (blue - red) / sd_score) + 1)


def rp_prob(teams):
    return logistic(sum(teams))
