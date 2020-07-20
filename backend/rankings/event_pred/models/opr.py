import numpy as np
import scipy.linalg


def logistic(n):
    return float(1/(1+np.e**(-4*(n-0.5))))


def score(match, alliance):
    if alliance == "red":
        return [match["red_score"]]
    return [match["blue_score"]]


def event_score(event):
    return [event["opr_start"]]


def all(match, alliance):
    if alliance == "red":
        return [match["red_score"], match["red_auto"], match["red_teleop"],
                match["red_1"], match["red_2"], match["red_endgame"],
                match["blue_fouls"], match["red_no_fouls"]]
    return [match["blue_score"], match["blue_auto"], match["blue_teleop"],
            match["blue_1"], match["blue_2"], match["blue_endgame"],
            match["red_fouls"], match["blue_no_fouls"]]


def event_all(event):
    return [event["opr_start"], event["opr_auto"], event["opr_teleop"],
            event["opr_1"], event["opr_2"], event["opr_endgame"],
            event["opr_fouls"], event["opr_no_fouls"]]


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
    T, Y = input.shape[1], output.shape[1]  # teams in event
    TM = (2 if year <= 2004 else 3)  # teams per alliance
    out = np.zeros(shape=(T, Y))
    for i in range(T):
        locs = np.where(input[i][:] == 1)
        if len(locs[0]) == 0:
            out[i] = np.array([0 * Y])
        else:
            out[i] = np.mean(output[locs], axis=0)/TM
    return out


def get_ixOPR(year, quals, playoffs, teams, team_stats, team_matches,
              mean_score, func=all, event_func=event_all):

    # case of only playoffs
    if len(quals) == 0:
        out = {}
        for t in teams:
            out[t] = [event_func(team_stats[t])]
        return out

    out = {}
    M, T, Y = len(quals), len(teams), len(event_func(team_stats[teams[0]]))
    input = np.zeros(shape=(2*M, T), dtype="float")
    output = np.zeros(shape=(2*M, Y), dtype="float")

    arr = []
    for i in range(M):
        red, blue = quals[i]["red"], quals[i]["blue"]
        red = [teams.index(t) for t in red]
        blue = [teams.index(t) for t in blue]
        arr.append([red, blue])

    for i in range(M):
        for t in arr[i][0]: input[2*i][t] = 1  # noqa 701
        for t in arr[i][1]: input[2*i+1][t] = 1  # noqa 701
        red = [event_func(team_stats[teams[t]]) for t in arr[i][0]]
        blue = [event_func(team_stats[teams[t]]) for t in arr[i][1]]
        output[2*i] = np.sum(red, axis=0)
        output[2*i+1] = np.sum(blue, axis=0)

    oprs = computeOPR(input, output, year, mean_score)

    for i in range(T):
        out[teams[i]] = [oprs[i]]

    iterations = 2  # experimentally chosen
    for i in range(M):
        m = quals[i]
        output[2*i] = np.array(func(m, "red"))
        output[2*i+1] = np.array(func(m, "blue"))
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


def get_ILS(quals, teams, team_stats, team_matches):
    min_ils = -1/3

    out = {}
    for team in teams:
        out[team] = np.zeros(shape=(len(quals)+1, 2))
        out[team][0] = [team_stats[team]["ils_1_start"], team_stats[team]["ils_2_start"]]  # noqa 502

    for i, m in enumerate(quals):
        red, blue = m["red"], m["blue"]
        adjust_red_1 = (m["red_rp_1"] - logistic(sum([out[r][i][0] for r in red]))) / 10  # noqa 502
        adjust_red_2 = (m["red_rp_2"] - logistic(sum([out[r][i][1] for r in red]))) / 10  # noqa 502
        adjust_blue_1 = (m["blue_rp_1"] - logistic(sum([out[b][i][0] for b in blue]))) / 10  # noqa 502
        adjust_blue_2 = (m["blue_rp_2"] - logistic(sum([out[b][i][1] for b in blue]))) / 10  # noqa 502

        for t in teams:
            out[t][i+1] = out[t][i]
            if t in red:
                out[t][i+1][0] = max(min_ils, out[t][i][0]+adjust_red_1)
                out[t][i+1][1] = max(min_ils, out[t][i][1]+adjust_red_2)
            elif t in blue:
                out[t][i+1][0] = max(min_ils, out[t][i][0]+adjust_blue_1)
                out[t][i+1][1] = max(min_ils, out[t][i][1]+adjust_blue_2)

    return out


def get_oprs(year, quals, playoffs, teams, team_stats, team_matches, mean_score):  # noqa 502
    OPRs = get_ixOPR(year, quals, playoffs, teams, team_stats,
                     team_matches, mean_score, all, event_all)
    ILS = get_ILS(quals, teams, team_stats, team_matches)
    return OPRs, ILS


def win_prob(red, blue, year, sd_score):
    if isinstance(red, list): red = sum(red)  # noqa 701
    if isinstance(red, dict): red = sum(red.values())  # noqa 701
    if isinstance(blue, list): blue = sum(blue)  # noqa 701
    if isinstance(blue, dict): blue = sum(blue.values())  # noqa 701
    return 1/(10**(5/8*(blue-red)/sd_score)+1)


def rp_prob(teams):
    return logistic(sum(teams))
