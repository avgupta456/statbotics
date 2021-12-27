import random
from typing import Any, Dict, List, Tuple

from rankings.event_pred import read
from rankings.event_pred.models import (
    elo as elo_model,
    opr as opr_model,
    rps as rps_model,
    tiebreakers,
)


def get_dicts(event_key: str, year: int):
    key = str(year) + event_key
    sd_score, mean_score = read.get_year_dict(year=year)
    teams, team_stats = read.get_teams_dict(key)
    matches = read.get_matches_dict(key)
    team_matches = read.get_team_matches_dict(key)

    # currently empty elims
    oprs, ils = opr_model.get_oprs(
        year, matches, [], teams, team_stats, team_matches, mean_score
    )
    elos = elo_model.get_elos(matches, teams, team_stats, team_matches)
    teams = oprs.keys()

    rps = rps_model.get_rps(matches, teams)
    ties = tiebreakers.get_tiebreakers(year, matches, teams)

    return teams, matches, sd_score, oprs, ils, elos, rps, ties


def get_curr_stats(
    index: int,
    teams: List[int],
    oprs: Dict[int, List[Any]],
    ils: Dict[int, List[Any]],
    elos: Dict[int, List[Any]],
) -> Tuple[Dict[int, Any], Dict[int, Any], Dict[int, Any]]:
    oprs_curr: Dict[int, Any] = {}
    ils_curr: Dict[int, Any] = {}
    elos_curr: Dict[int, Any] = {}
    for team in teams:
        oprs_curr[team] = oprs[team][index]
        ils_curr[team] = ils[team][index]
        elos_curr[team] = elos[team][index]
    return oprs_curr, ils_curr, elos_curr


def get_preds(
    index: int,
    quals: List[Dict[str, Any]],
    oprs_curr: Dict[int, Any],
    elos_curr: Dict[int, Any],
    ils_curr: Dict[int, Any],
    year: int,
    sd_score: float,
):
    team_matches: Dict[
        int, Any
    ] = {}  # for each match i after index, red and blue teams
    preds: Dict[
        int, List[float]
    ] = {}  # for each match i after index , win_prob, red rps, blue rps
    for i in range(index, len(quals)):
        m = quals[i]
        red, blue = m["red"], m["blue"]
        red_score = sum([oprs_curr[t][0] for t in red])
        blue_score = sum([oprs_curr[t][0] for t in blue])
        red_elo = sum([elos_curr[t] for t in red])
        blue_elo = sum([elos_curr[t] for t in blue])

        elo_prob = elo_model.win_prob(red_elo, blue_elo)
        elo_margin = elo_model.win_margin(red_elo, blue_elo, sd_score)
        opr_prob = opr_model.win_prob(red_score, blue_score, year, sd_score)
        win_prob = (elo_prob + opr_prob) / 2
        win_margin = (elo_margin + (red_score - blue_score)) / 2
        red_score = (red_score + blue_score) / 2 + win_margin / 2
        blue_score = (red_score + blue_score) / 2 - win_margin / 2

        red_rp_1 = opr_model.rp_prob([ils_curr[t][0] for t in red])
        red_rp_2 = opr_model.rp_prob([ils_curr[t][1] for t in red])
        blue_rp_1 = opr_model.rp_prob([ils_curr[t][0] for t in blue])
        blue_rp_2 = opr_model.rp_prob([ils_curr[t][1] for t in blue])

        ties_pred = tiebreakers.get_opr_tiebreakers(oprs_curr, red, blue, year)
        red_tie, blue_tie = ties_pred

        team_matches[i] = [red, blue]
        preds[i] = [
            round(float(red_score)),
            round(float(blue_score)),
            round(float(win_prob), 2),
            round(red_rp_1, 2),
            round(red_rp_2, 2),
            round(blue_rp_1, 2),
            round(blue_rp_2, 2),
            round(red_tie, 2),
            round(blue_tie, 2),
        ]

    return team_matches, preds


def _mean_sim(
    index: int,
    matches: List[Dict[str, Any]],
    teams: List[int],
    team_matches: Dict[int, Any],
    preds: Dict[int, List[float]],
    rps: Dict[int, Any],
    ties: Dict[int, Any],
):
    rps_out: Dict[int, float] = {}
    ties_out: Dict[int, float] = {}
    for team in teams:
        rps_out[team] = rps[team][index][0]
        ties_out[team] = ties[team][index][0]
    for i in range(index, len(matches)):
        red, blue = team_matches[i]
        red_rps = preds[i][2] * 2 + preds[i][3] + preds[i][4]
        blue_rps = (1 - preds[i][2]) * 2 + preds[i][5] + preds[i][6]
        for team in teams:
            if team in red:
                rps_out[team] += red_rps
                ties_out[team] += preds[i][7]
            if team in blue:
                rps_out[team] += blue_rps
                ties_out[team] += preds[i][8]
        for team in teams:
            rps_out[team] = round(rps_out[team], 2)
            ties_out[team] = round(ties_out[team], 2)
    return rps_out, ties_out


def mean_sim(year: int, event_key: str, i: int):
    teams, matches, sd_score, oprs, ils, elos, rps, ties = get_dicts(event_key, year)
    for t in teams:  # gets specific stats based on current index
        oprs[t], ils[t], elos[t] = oprs[t][i], ils[t][i], elos[t][i]
    team_matches, preds = get_preds(i, matches, oprs, elos, ils, year, sd_score)
    rps_out, ties_out = _mean_sim(i, matches, teams, team_matches, preds, rps, ties)

    return {"mean_rps": rps_out, "mean_tiebreakers": ties_out}


def single_sim(
    index: int,
    matches: List[Dict[str, Any]],
    teams: List[int],
    team_matches: Dict[int, Any],
    preds: Dict[int, List[float]],
    rps: Dict[int, Any],
    mean_ties: Dict[int, Any],
):
    rps_out: Dict[int, float] = {}
    for team in teams:
        rps_out[team] = rps[team][index][0]

    for i in range(index, len(matches)):
        red, blue = team_matches[i]
        red_rps, blue_rps = 0, 0
        if preds[i][2] > random.uniform(0, 1):
            red_rps += 2
        else:
            blue_rps += 2
        if preds[i][3] > random.uniform(0, 1):
            red_rps += 1
        if preds[i][4] > random.uniform(0, 1):
            red_rps += 1
        if preds[i][5] > random.uniform(0, 1):
            blue_rps += 1
        if preds[i][6] > random.uniform(0, 1):
            blue_rps += 1
        for team in red:
            rps_out[team] += red_rps
        for team in blue:
            rps_out[team] += blue_rps

    rps_dict: Dict[int, Tuple[float, float]] = {}
    for team in teams:
        rps_dict[team] = (rps_out[team], mean_ties[team])
    rps_list = sorted(rps_dict, key=lambda k: rps_dict[k], reverse=True)
    ranks_out = {rps_list[i]: i + 1 for i in range(len(rps_list))}
    return rps_out, ranks_out


def _index_sim(
    index: int,
    iterations: int,
    teams: List[int],
    matches: List[Dict[str, Any]],
    team_matches: Dict[int, Any],
    preds: Dict[int, List[float]],
    rps: Dict[int, Any],
    ties: Dict[int, Any],
):
    mean_rps, mean_ties = _mean_sim(
        index, matches, teams, team_matches, preds, rps, ties
    )

    T = len(teams)
    avg_rps: Dict[int, float] = {}
    ranks: Dict[int, List[float]] = {}
    for team in teams:
        avg_rps[team] = 0
        ranks[team] = [0 for _ in range(T)]

    for _ in range(iterations):
        rps_ind, ranks_ind = single_sim(
            index, matches, teams, team_matches, preds, rps, mean_ties
        )
        for team in teams:
            avg_rps[team] += rps_ind[team]
            ranks[team][ranks_ind[team] - 1] += 1

    avg_ranks: Dict[int, float] = {}
    for team in teams:
        avg_rps[team] /= iterations
        ranks[team] = [round(freq / iterations, 2) for freq in ranks[team]]
        avg_ranks[team] = round(1 + sum([i * ranks[team][i] for i in range(T)]), 2)
    return mean_rps, mean_ties, avg_rps, avg_ranks, ranks


def index_sim(year: int, event_key: str, i: int, iterations: int):
    teams, matches, sd_score, oprs, ils, elos, rps, ties = get_dicts(event_key, year)
    for t in teams:  # gets specific stats based on current index
        oprs[t], ils[t], elos[t] = oprs[t][i], ils[t][i], elos[t][i]
    team_matches, preds = get_preds(i, matches, oprs, elos, ils, year, sd_score)
    mean_rps, mean_ties, avg_rps, avg_ranks, ranks = _index_sim(
        i, iterations, teams, matches, team_matches, preds, rps, ties
    )

    dict_ranks = {}
    for team in ranks:
        dict_ranks[team] = {}
        for i in range(len(ranks[team])):
            dict_ranks[team][i + 1] = ranks[team][i]

    return {
        "mean_rps": mean_rps,
        "mean_tiebreaker": mean_ties,
        "sim_rps": avg_rps,
        "sim_ranks": avg_ranks,
        "sim_rank_probs": dict_ranks,
    }


def quick_sim(year: int, event_key: str):
    teams, matches, sd_score, oprs, ils, elos, rps, ties = get_dicts(event_key, year)

    out: Dict[int, Dict[str, Dict[int, Any]]] = {}
    for i in range(len(matches) + 1):
        oprs_c, ils_c, elos_c = get_curr_stats(i, teams, oprs, ils, elos)
        team_matches, preds = get_preds(
            i, matches, oprs_c, elos_c, ils_c, year, sd_score
        )
        mean_rps, mean_ties = _mean_sim(
            i, matches, teams, team_matches, preds, rps, ties
        )
        sub_out: Dict[str, Dict[int, Any]] = {"mean_rps": {}, "mean_tiebreaker": {}}
        for team in teams:
            sub_out["mean_rps"][team] = mean_rps[team]
            sub_out["mean_tiebreaker"][team] = mean_ties[team]
        out[i] = sub_out
    return out


def sim(year: int, event_key: str, iterations: int = 100):
    teams, matches, sd_score, oprs, ils, elos, rps, ties = get_dicts(event_key, year)

    out: Dict[int, Dict[str, Dict[int, Any]]] = {}
    for i in range(len(matches) + 1):
        oprs_c, ils_c, elos_c = get_curr_stats(i, teams, oprs, ils, elos)
        team_matches, preds = get_preds(
            i, matches, oprs_c, elos_c, ils_c, year, sd_score
        )
        mean_rps, mean_ties, avg_rps, avg_ranks, ranks = _index_sim(
            i, iterations, teams, matches, team_matches, preds, rps, ties
        )

        sub_out: Dict[str, Dict[int, Any]] = {
            "mean_rps": {},
            "mean_tiebreaker": {},
            "sim_rps": {},
            "sim_ranks": {},
            "sim_rank_probs": {},
        }
        for team in teams:
            sub_out["mean_rps"][team] = mean_rps[team]
            sub_out["mean_tiebreaker"][team] = mean_ties[team]
            sub_out["sim_rps"][team] = avg_rps[team]
            sub_out["sim_ranks"][team] = avg_ranks[team]
            sub_out["sim_rank_probs"][team] = ranks[team]
        out[i] = sub_out
    return out
