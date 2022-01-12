from typing import Any, Callable, Dict, List, Set, Tuple

import numpy as np
import scipy.linalg  # type: ignore

from src.db.models.event import Event
from src.db.models.match import Match
from src.db.models.team_event import TeamEvent
from src.helper.utils import logistic


def score(match: Match, alliance: str) -> List[int]:
    if alliance == "red":
        return [match.red_score or 0]
    return [match.blue_score or 0]


def event_score(event: TeamEvent) -> List[float]:
    return [event.opr_start or 0]


def all(match: Match, alliance: str) -> List[float]:
    if alliance == "red":
        return [
            match.red_score or 0,
            match.red_auto or 0,
            match.red_teleop or 0,
            match.red_1 or 0,
            match.red_2 or 0,
            match.red_endgame or 0,
            match.blue_fouls or 0,
            match.red_no_fouls or 0,
        ]
    return [
        match.blue_score or 0,
        match.blue_auto or 0,
        match.blue_teleop or 0,
        match.blue_1 or 0,
        match.blue_2 or 0,
        match.blue_endgame or 0,
        match.red_fouls or 0,
        match.blue_no_fouls or 0,
    ]


def event_all(event: TeamEvent) -> List[float]:
    return [
        event.opr_start or 0,
        event.opr_auto or 0,
        event.opr_teleop or 0,
        event.opr_1 or 0,
        event.opr_2 or 0,
        event.opr_endgame or 0,
        event.opr_fouls or 0,
        event.opr_no_fouls or 0,
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


def get_base(
    event: Event,
    team_events: List[TeamEvent],
    quals: List[Match],
    playoffs: List[Match],
    event_func: Callable[..., Any],
) -> Tuple[
    Any,
    Dict[int, TeamEvent],
    List[int],
    List[List[List[int]]],
    Any,
    Any,
    int,
    int,
    List[Match],
    int,
]:
    year = event.year
    team_events_dict: Dict[int, TeamEvent] = {}
    for team_event in team_events:
        team_events_dict[team_event.team] = team_event

    # case of only playoffs
    if len(quals) == 0:
        teams_set: Set[int] = set()
        out: Any = {}
        for m in playoffs:
            [teams_set.add(t) for t in m.get_red()]
            [teams_set.add(t) for t in m.get_blue()]
        teams = list(teams_set)
        for t in teams:
            out[t] = [event_func(team_events_dict[t])]
        return out, team_events_dict, [], [], None, None, 0, 0, [], 0

    teams_set: Set[int] = set()
    out: Any = {}
    for m in quals:
        [teams_set.add(t) for t in m.get_red()]
        [teams_set.add(t) for t in m.get_blue()]
    teams = list(teams_set)

    M, T, Y = len(quals), len(teams), len(event_func(team_events_dict[teams[0]]))
    input: Any = np.zeros(shape=(2 * M, T), dtype="float")  # type: ignore
    output: Any = np.zeros(shape=(2 * M, Y), dtype="float")  # type: ignore
    match_objs = quals

    arr: List[List[List[int]]] = []
    for i in range(M):
        red, blue = match_objs[i].get_red(), match_objs[i].get_blue()
        red = [teams.index(t) for t in red]
        blue = [teams.index(t) for t in blue]
        arr.append([red, blue])

    return (
        out,
        team_events_dict,
        teams,
        arr,
        input,
        output,
        T,
        M,
        match_objs,
        year,
    )


def get_OPR(
    event: Event,
    team_events: List[TeamEvent],
    quals: List[Match],
    playoffs: List[Match],
    score_mean: float,
    func: Callable[..., Any] = all,
    event_func: Callable[..., Any] = event_all,
) -> Any:
    base = get_base(event, team_events, quals, playoffs, event_func)
    (
        out,
        _team_events_dict,
        teams,
        arr,
        input,
        output,
        T,
        M,
        m_objs,
        year,
    ) = base

    if out != {}:
        return out

    oprs = compute_OPR(input, output, year, score_mean)
    for i in range(T):
        out[teams[i]] = [oprs[i]]

    for i in range(M):
        m = m_objs[i]
        for t in arr[i][0]:
            input[2 * i][t] = 1
        for t in arr[i][1]:
            input[2 * i + 1][t] = 1
        output[2 * i] = np.array(func(m, "red"))  # type: ignore
        output[2 * i + 1] = np.array(func(m, "blue"))  # type: ignore
        oprs = compute_OPR(input, output, year, score_mean)
        [out[teams[j]].append(oprs[j]) for j in range(T)]
    return out


def get_xOPR(
    event: Event,
    team_events: List[TeamEvent],
    quals: List[Match],
    playoffs: List[Match],
    score_mean: float,
    func: Callable[..., Any] = all,
    event_func: Callable[..., Any] = event_all,
):
    base = get_base(event, team_events, quals, playoffs, event_func)
    (
        out,
        team_events_dict,
        teams,
        arr,
        input,
        output,
        T,
        M,
        m_objs,
        year,
    ) = base

    if out != {}:
        return out

    for i in range(M):
        for t in arr[i][0]:
            input[2 * i][t] = 1
        for t in arr[i][1]:
            input[2 * i + 1][t] = 1
        red = [event_func(team_events_dict[teams[t]]) for t in arr[i][0]]
        blue = [event_func(team_events_dict[teams[t]]) for t in arr[i][1]]
        output[2 * i] = np.sum(red, axis=0)  # type: ignore
        output[2 * i + 1] = np.sum(blue, axis=0)  # type: ignore

    oprs = compute_OPR(input, output, year, score_mean)
    for i in range(T):
        out[teams[i]] = [oprs[i]]

    for i in range(M):
        m = m_objs[i]
        output[2 * i] = np.array(func(m, "red"))  # type: ignore
        output[2 * i + 1] = np.array(func(m, "blue"))  # type: ignore
        oprs = compute_OPR(input, output, year, score_mean)
        [out[teams[j]].append(oprs[j]) for j in range(T)]
    return out


def get_ixOPR(
    event: Event,
    team_events: List[TeamEvent],
    quals: List[Match],
    playoffs: List[Match],
    score_mean: float,
    func: Callable[..., Any] = all,
    event_func: Callable[..., Any] = event_all,
):
    base = get_base(event, team_events, quals, playoffs, event_func)
    (
        out,
        team_events_dict,
        teams,
        arr,
        input,
        output,
        T,
        M,
        m_objs,
        year,
    ) = base

    if out != {}:
        return out

    for i in range(M):
        for t in arr[i][0]:
            input[2 * i][t] = 1
        for t in arr[i][1]:
            input[2 * i + 1][t] = 1
        red = [event_func(team_events_dict[teams[t]]) for t in arr[i][0]]
        blue = [event_func(team_events_dict[teams[t]]) for t in arr[i][1]]
        output[2 * i] = np.sum(red, axis=0)  # type: ignore
        output[2 * i + 1] = np.sum(blue, axis=0)  # type: ignore

    oprs = compute_OPR(input, output, year, score_mean)

    for i in range(T):
        out[teams[i]] = [oprs[i]]

    M_completed = len([m for m in quals if m.status == "Completed"])
    iterations = 2  # experimentally chosen
    for i in range(M_completed):
        m = m_objs[i]
        output[2 * i] = np.array(func(m, "red"))  # type: ignore
        output[2 * i + 1] = np.array(func(m, "blue"))  # type: ignore
        oprs = compute_OPR(input, output, year, score_mean)
        for j in range(iterations - 1):
            temp = output.copy()
            for k in range(i, M):
                temp[2 * k] = np.sum([oprs[i] for i in arr[k][0]], axis=0)  # type: ignore
                temp[2 * k + 1] = np.sum([oprs[i] for i in arr[k][1]], axis=0)  # type: ignore
            oprs = compute_OPR(input, temp, year, score_mean)
        for j in range(T):
            out[teams[j]].append(oprs[j])
    return out


def get_ILS(team_events: List[TeamEvent], quals: List[Match]):
    completed_quals = [m for m in quals if m.status == "Completed"]

    min_ils = -1 / 3
    teams: List[int] = []
    out: Any = {}

    for team_event in team_events:
        teams.append(team_event.team)
        out[teams[-1]] = np.zeros(shape=(len(completed_quals) + 1, 2))  # type: ignore
        curr = [team_event.ils_1_start, team_event.ils_2_start]
        out[teams[-1]][0] = np.array(curr)  # type: ignore

    for i, m in enumerate(completed_quals):
        red, blue = m.get_teams()
        adjust_red_1 = (
            (m.red_rp_1 or 0) - (logistic(sum([out[r][i][0] for r in red])) or 0)
        ) / 10
        adjust_red_2 = (
            (m.red_rp_2 or 0) - (logistic(sum([out[r][i][1] for r in red])) or 0)
        ) / 10
        adjust_blue_1 = (
            (m.blue_rp_1 or 0) - (logistic(sum([out[b][i][0] for b in blue])) or 0)
        ) / 10
        adjust_blue_2 = (
            (m.blue_rp_2 or 0) - (logistic(sum([out[b][i][1] for b in blue])) or 0)
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


def opr_v1(
    event: Event, team_events: List[TeamEvent], matches: List[Match], score_mean: float
):
    quals = sorted([m for m in matches if not m.playoff], key=lambda m: m.sort())
    playoffs = sorted([m for m in matches if m.playoff], key=lambda m: m.sort())
    return get_ixOPR(
        event, team_events, quals, playoffs, score_mean, score, event_score
    )


def opr_v2(
    event: Event, team_events: List[TeamEvent], matches: List[Match], score_mean: float
):
    quals = sorted([m for m in matches if not m.playoff], key=lambda m: m.sort())
    playoffs = sorted([m for m in matches if m.playoff], key=lambda m: m.sort())
    OPRs = get_ixOPR(event, team_events, quals, playoffs, score_mean, all, event_all)
    ILS = get_ILS(team_events, quals)
    return OPRs, ILS


def win_prob(red_sum: float, blue_sum: float, sd_score: float) -> float:
    return 1 / (10 ** (5 / 8 * (blue_sum - red_sum) / sd_score) + 1)


def rp_prob(teams: List[float]) -> float:
    return logistic(sum(teams))
