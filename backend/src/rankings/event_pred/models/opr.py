from typing import Any, Callable, Dict, List, Union
import numpy as np
import scipy.linalg  # type: ignore


e = np.e


def logistic(n: float):
    return float(1 / (1 + e ** (-4 * (n - 0.5))))


def score(match: Dict[str, Any], alliance: str) -> float:
    if alliance == "red":
        return [match["red_score"]]  # type: ignore
    return [match["blue_score"]]  # type: ignore


def event_score(event: Dict[str, Any]) -> float:
    return [event["opr_start"]]  # type: ignore


def all(match: Dict[str, Any], alliance: str) -> List[float]:
    if alliance == "red":
        return [
            match["red_score"],
            match["red_auto"],
            match["red_teleop"],
            match["red_1"],
            match["red_2"],
            match["red_endgame"],
            match["blue_fouls"],
            match["red_no_fouls"],
        ]
    return [
        match["blue_score"],
        match["blue_auto"],
        match["blue_teleop"],
        match["blue_1"],
        match["blue_2"],
        match["blue_endgame"],
        match["red_fouls"],
        match["blue_no_fouls"],
    ]


def event_all(event: Dict[str, Any]) -> List[float]:
    return [
        event["opr_start"],
        event["opr_auto"],
        event["opr_teleop"],
        event["opr_1"],
        event["opr_2"],
        event["opr_endgame"],
        event["opr_fouls"],
        event["opr_no_fouls"],
    ]


def compute_OPR(input: Any, output: Any, year: int, mean_score: float) -> Any:
    try:
        A = np.matmul(input.T, input)
        Y = np.matmul(input.T, output)
        out = scipy.linalg.lstsq(  # type: ignore
            A,
            Y,
            overwrite_a=True,
            overwrite_b=True,
            check_finite=True,
            lapack_driver="gelsy",
        )[0]
    except scipy.linalg.LinAlgError or scipy.linalg.ValueError:
        # if singular (not enough matches, etc)
        out = compute_averages(input, output, year)
    # if highly unstable, handles foul oprs
    if np.min(out) < -mean_score / (2 if year <= 2004 else 3):  # type: ignore
        out = compute_averages(input, output, year)
    return out  # type: ignore


# returns 2d np array
def compute_averages(input: Any, output: Any, year: int) -> Any:
    T, Y = input.shape[1], output.shape[1]  # teams in event
    TM = 2 if year <= 2004 else 3  # teams per alliance
    out = np.zeros(shape=(T, Y))  # type: ignore
    for i in range(T):
        locs = np.where(input[i][:] == 1)  # type: ignore
        if len(locs[0]) == 0:  # type: ignore
            out[i] = np.array([0 * Y])  # type: ignore
        else:
            out[i] = np.mean(output[locs], axis=0) / TM  # type: ignore
    return out  # type: ignore


def get_ixOPR(
    year: int,
    quals: List[Dict[str, Any]],
    playoffs: List[Dict[str, Any]],
    teams: List[int],
    team_stats: Dict[int, Dict[str, Union[int, float]]],
    team_matches: Dict[str, Dict[int, Any]],
    mean_score: float,
    func: Callable[..., Any] = all,
    event_func: Callable[..., Any] = event_all,
) -> Any:

    # case of only playoffs
    if len(quals) == 0:
        out: Dict[int, List[Any]] = {}
        for t in teams:
            out[t] = [event_func(team_stats[t])]
        return out

    out = {}
    M, T, Y = len(quals), len(teams), len(event_func(team_stats[teams[0]]))
    input = np.zeros(shape=(2 * M, T), dtype="float")  # type: ignore
    output = np.zeros(shape=(2 * M, Y), dtype="float")  # type: ignore

    arr: List[List[List[int]]] = []
    for i in range(M):
        red, blue = quals[i]["red"], quals[i]["blue"]
        red = [teams.index(t) for t in red]
        blue = [teams.index(t) for t in blue]
        arr.append([red, blue])

    for i in range(M):
        for t in arr[i][0]:
            input[2 * i][t] = 1
        for t in arr[i][1]:
            input[2 * i + 1][t] = 1

        red = [event_func(team_stats[teams[t]]) for t in arr[i][0]]
        blue = [event_func(team_stats[teams[t]]) for t in arr[i][1]]
        output[2 * i] = np.sum(red, axis=0)  # type: ignore
        output[2 * i + 1] = np.sum(blue, axis=0)  # type: ignore

    oprs = compute_OPR(input, output, year, mean_score)

    for i in range(T):
        out[teams[i]] = [oprs[i]]

    iterations = 2  # experimentally chosen
    for i in range(M):
        m = quals[i]
        output[2 * i] = np.array(func(m, "red"))  # type: ignore
        output[2 * i + 1] = np.array(func(m, "blue"))  # type: ignore
        oprs = compute_OPR(input, output, year, mean_score)
        for j in range(iterations - 1):
            temp: Any = output.copy()
            for k in range(i, M):
                temp[2 * k] = np.sum([oprs[i] for i in arr[k][0]], axis=0)  # type: ignore
                temp[2 * k + 1] = np.sum([oprs[i] for i in arr[k][1]], axis=0)  # type: ignore
            oprs = compute_OPR(input, temp, year, mean_score)
        for j in range(T):
            out[teams[j]].append(oprs[j])
    return out


def get_ILS(
    quals: List[Dict[str, Any]],
    teams: List[int],
    team_stats: Dict[int, Dict[str, Union[int, float]]],
    team_matches: Dict[str, Dict[int, Any]],
):
    min_ils = -1 / 3

    out: Dict[int, Any] = {}
    for team in teams:
        out[team] = np.zeros(shape=(len(quals) + 1, 2))  # type: ignore
        out[team][0] = [
            team_stats[team]["ils_1_start"],
            team_stats[team]["ils_2_start"],
        ]

    for i, m in enumerate(quals):
        red, blue = m["red"], m["blue"]
        adjust_red_1 = (m["red_rp_1"] - logistic(sum([out[r][i][0] for r in red]))) / 10
        adjust_red_2 = (m["red_rp_2"] - logistic(sum([out[r][i][1] for r in red]))) / 10
        adjust_blue_1 = (
            m["blue_rp_1"] - logistic(sum([out[b][i][0] for b in blue]))
        ) / 10
        adjust_blue_2 = (
            m["blue_rp_2"] - logistic(sum([out[b][i][1] for b in blue]))
        ) / 10

        for t in teams:
            out[t][i + 1] = out[t][i]
            if t in red:
                out[t][i + 1][0] = max(min_ils, out[t][i][0] + adjust_red_1)
                out[t][i + 1][1] = max(min_ils, out[t][i][1] + adjust_red_2)
            elif t in blue:
                out[t][i + 1][0] = max(min_ils, out[t][i][0] + adjust_blue_1)
                out[t][i + 1][1] = max(min_ils, out[t][i][1] + adjust_blue_2)

    return out


def get_oprs(
    year: int,
    quals: List[Dict[str, Any]],
    playoffs: List[Dict[str, Any]],
    teams: List[int],
    team_stats: Dict[int, Dict[str, Union[int, float]]],
    team_matches: Dict[str, Dict[int, Any]],
    mean_score: float,
):
    OPRs = get_ixOPR(
        year,
        quals,
        playoffs,
        teams,
        team_stats,
        team_matches,
        mean_score,
        all,
        event_all,
    )
    ILS = get_ILS(quals, teams, team_stats, team_matches)
    return OPRs, ILS


def win_prob(red_sum: float, blue_sum: float, year: int, sd_score: float):
    return 1 / (10 ** (5 / 8 * (blue_sum - red_sum) / sd_score) + 1)


def rp_prob(teams: List[float]) -> float:
    return logistic(sum(teams))
