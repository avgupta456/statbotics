from collections import defaultdict
from statistics import stdev
from typing import Dict, List, Tuple

import numpy as np
from scipy.stats import expon, exponnorm  # type: ignore

from src.db.models import Event, Match, TeamEvent, TeamMatch, TeamYear, Year
from src.db.read import get_team_years as get_team_years_db, get_teams as get_teams_db
from src.db.write.main import update_teams as update_teams_db
from src.utils.utils import get_team_event_key, get_team_match_key

# HELPER FUNCTIONS

NORM_MEAN = 1500
NORM_SD = 250

distrib = exponnorm(1.6, -0.3, 0.2)  # type: ignore


def ppf(x: float) -> float:
    return distrib.ppf(x)  # type: ignore


def norm_epa_to_sd(norm_epa: float) -> float:
    return (norm_epa - NORM_MEAN) / NORM_SD


def norm_epa_to_next_season_epa(
    norm_epa: float,
    curr_mean: float,
    curr_sd: float,
    curr_num_teams: int,
) -> float:
    return max(curr_mean / curr_num_teams + curr_sd * norm_epa_to_sd(norm_epa), 0)


def sigmoid(x: float) -> float:
    return 1 / (1 + np.exp(-4 * (x - 0.5)))


def inv_sigmoid(x: float) -> float:
    return 0.5 + np.log(x / (1 - x)) / 4


# TUNABLE PARAMETERS

YEAR_ONE_WEIGHT = 0.7
MEAN_REVERSION = 0.4
INIT_PENALTY = 0.2

PLAYOFF_WEIGHT = 1 / 3
MIN_RP_EPA = -1 / 3
RP_PERCENT = 0.3


def k_func(year: int) -> float:
    return -5 / 8 if year >= 2008 else -5 / 12


def margin_func(year: int, x: int) -> float:
    # TODO: better handle 2018, currently vastly overestimates scores
    if year in [2002, 2003, 2018]:
        return 1
    if year in [2015]:
        return 0
    return min(1, max(0, 1 / 24 * (x - 12)))


def percent_func(year: int, x: int) -> float:
    if year <= 2010:
        return 0.3
    return min(0.5, max(0.3, 0.5 - 0.2 / 6 * (x - 6)))


# TODO: I removed nonlinear sum_func, but it might be useful
# In general, model overpredicts when 2+ strong teams

# MAIN FUNCTION
def process_year(
    year_num: int,
    team_years_all: Dict[int, Dict[int, TeamYear]],
    year: Year,
    team_years: List[TeamYear],
    events: List[Event],
    team_events: List[TeamEvent],
    matches: List[Match],
    team_matches: List[TeamMatch],
    year_epa_stats: Dict[int, Tuple[float, float]],
) -> Tuple[
    Dict[int, Dict[int, TeamYear]],
    Year,
    List[TeamYear],
    List[Event],
    List[TeamEvent],
    List[Match],
    List[TeamMatch],
]:
    NUM_TEAMS = 2 if year_num <= 2004 else 3
    USE_COMPONENTS = year_num >= 2016
    K = k_func(year_num)

    # no_fouls_mean after 2016, score_mean before 2016
    TOTAL_MEAN = year.no_fouls_mean or year.score_mean or 0
    TOTAL_SD = year.score_sd or 0
    INIT_EPA = TOTAL_MEAN / NUM_TEAMS - INIT_PENALTY * TOTAL_SD

    AUTO_MEAN = year.auto_mean or 0
    INIT_AUTO_EPA = INIT_EPA * AUTO_MEAN / max(1, TOTAL_MEAN)

    TELEOP_MEAN = year.teleop_mean or 0
    INIT_TELEOP_EPA = INIT_EPA * TELEOP_MEAN / max(1, TOTAL_MEAN)

    ENDGAME_MEAN = year.endgame_mean or 0
    INIT_ENDGAME_EPA = INIT_EPA * ENDGAME_MEAN / max(1, TOTAL_MEAN)

    RP1_MEAN = year.rp_1_mean or sigmoid(MIN_RP_EPA * NUM_TEAMS)
    RP2_MEAN = year.rp_2_mean or sigmoid(MIN_RP_EPA * NUM_TEAMS)

    RP1_SEED = inv_sigmoid(RP1_MEAN) / NUM_TEAMS
    RP2_SEED = inv_sigmoid(RP2_MEAN) / NUM_TEAMS

    team_counts: Dict[int, int] = defaultdict(int)  # for updating epa
    team_epas: Dict[int, float] = defaultdict(lambda: INIT_EPA)  # most recent epa
    team_auto_epas: Dict[int, float] = defaultdict(lambda: INIT_AUTO_EPA)
    team_teleop_epas: Dict[int, float] = defaultdict(lambda: INIT_TELEOP_EPA)
    team_endgame_epas: Dict[int, float] = defaultdict(lambda: INIT_ENDGAME_EPA)
    team_rp_1_epas: Dict[int, float] = defaultdict(lambda: RP1_SEED)
    team_rp_2_epas: Dict[int, float] = defaultdict(lambda: RP2_SEED)

    team_years_dict: Dict[int, TeamYear] = {}
    team_events_dict: Dict[str, List[Tuple[float, bool]]] = {}
    team_matches_dict: Dict[int, List[float]] = {}
    team_match_ids: Dict[str, float] = {}
    component_team_events_dict: Dict[
        str, List[Tuple[float, float, float, float, float, bool]]
    ] = {}
    component_team_matches_dict: Dict[
        int, List[Tuple[float, float, float, float, float]]
    ] = {}
    component_team_match_ids: Dict[str, Tuple[float, float, float, float, float]] = {}

    # INITIALIZE
    for team_year in team_years:
        num = team_year.team
        team_years_dict[num] = team_year
        team_matches_dict[num] = []
        component_team_matches_dict[num] = []

        epa_1yr, epa_2yr = None, None
        if year_num in [2022, 2023]:
            # For 2022 and 2023, use past two years team competed (up to 4 years)
            past_epas: List[float] = []
            for past_year in range(year_num - 1, year_num - 5, -1):
                past_team_year = team_years_all.get(past_year, {}).get(num, None)
                if past_team_year is not None and past_team_year.epa_max is not None:
                    prev_norm_epa = past_team_year.norm_epa_end or NORM_MEAN
                    new_epa = norm_epa_to_next_season_epa(
                        prev_norm_epa, TOTAL_MEAN, TOTAL_SD, NUM_TEAMS
                    )
                    past_epas.append(new_epa)
            epa_1yr = past_epas[0] if len(past_epas) > 0 else None
            epa_2yr = past_epas[1] if len(past_epas) > 1 else None
        else:
            # Otherwise use the two most recent years (regardless of team activity)
            team_year_1 = team_years_all.get(year_num - 1, {}).get(num, None)
            if team_year_1 is not None and team_year_1.epa_max is not None:
                prev_norm_epa = team_year_1.norm_epa_end or NORM_MEAN
                epa_1yr = norm_epa_to_next_season_epa(
                    prev_norm_epa, TOTAL_MEAN, TOTAL_SD, NUM_TEAMS
                )
            team_year_2 = team_years_all.get(year_num - 2, {}).get(num, None)
            if team_year_2 is not None and team_year_2.epa_max is not None:
                prev_norm_epa = team_year_2.norm_epa_end or NORM_MEAN
                epa_2yr = norm_epa_to_next_season_epa(
                    prev_norm_epa, TOTAL_MEAN, TOTAL_SD, NUM_TEAMS
                )

        epa_1yr = epa_1yr or INIT_EPA
        epa_2yr = epa_2yr or INIT_EPA
        epa_prior = YEAR_ONE_WEIGHT * epa_1yr + (1 - YEAR_ONE_WEIGHT) * epa_2yr
        epa_prior = (1 - MEAN_REVERSION) * epa_prior + MEAN_REVERSION * INIT_EPA
        team_epas[num] = epa_prior
        team_year.epa_start = round(epa_prior, 2)

        if USE_COMPONENTS:
            team_auto_epas[num] = epa_prior * AUTO_MEAN / TOTAL_MEAN
            team_teleop_epas[num] = epa_prior * TELEOP_MEAN / TOTAL_MEAN
            team_endgame_epas[num] = epa_prior * ENDGAME_MEAN / TOTAL_MEAN
            team_year.auto_epa_start = round(team_auto_epas[num], 2)
            team_year.teleop_epa_start = round(team_teleop_epas[num], 2)
            team_year.endgame_epa_start = round(team_endgame_epas[num], 2)

            rp_factor = (epa_prior - TOTAL_MEAN / NUM_TEAMS) / (TOTAL_SD)
            team_rp_1_epas[num] = max(MIN_RP_EPA, RP1_SEED + 0.25 * rp_factor)
            team_rp_2_epas[num] = max(MIN_RP_EPA, RP2_SEED + 0.25 * rp_factor)
            team_year.rp_1_epa_start = round(team_rp_1_epas[num], 4)
            team_year.rp_2_epa_start = round(team_rp_2_epas[num], 4)

    # win, loss, tie, (rp), count
    team_year_stats: Dict[int, List[int]] = defaultdict(
        lambda: [0, 0, 0, 0]
    )  # no offseason
    full_team_year_stats: Dict[int, List[int]] = defaultdict(lambda: [0, 0, 0, 0])
    team_event_stats: Dict[str, List[int]] = defaultdict(lambda: [0, 0, 0, 0])
    qual_team_event_stats: Dict[str, List[int]] = defaultdict(lambda: [0, 0, 0, 0, 0])

    acc, mse, count = 0, 0, 0
    quals_acc, quals_mse, quals_count = 0, 0, 0
    elims_acc, elims_mse, elims_count = 0, 0, 0
    champs_acc, champs_mse, champs_count = 0, 0, 0
    event_stats: Dict[str, Tuple[float, float, int]] = defaultdict(lambda: (0, 0, 0))

    rp_1_acc, rp_1_mse, rp_1_count = 0, 0, 0
    champs_rp_1_acc, champs_rp_1_mse, champs_rp_1_count = 0, 0, 0
    rp_1_event_stats: Dict[str, Tuple[float, float, int]] = defaultdict(
        lambda: (0, 0, 0)
    )

    rp_2_acc, rp_2_mse, rp_2_count = 0, 0, 0
    champs_rp_2_acc, champs_rp_2_mse, champs_rp_2_count = 0, 0, 0
    rp_2_event_stats: Dict[str, Tuple[float, float, int]] = defaultdict(
        lambda: (0, 0, 0)
    )

    # TODO: compute RP Precision, Recall, F1-Score

    event_weeks = {e.key: e.week for e in events}
    event_types = {e.key: e.type for e in events}
    sorted_matches = sorted(matches, key=lambda m: m.sort())
    for match in sorted_matches:
        event_key = match.event
        red, blue = match.get_teams()

        red_epa_pre: Dict[int, float] = {}
        blue_epa_pre: Dict[int, float] = {}

        for team in red:
            red_epa_pre[team] = team_epas[team]
            team_match_ids[get_team_match_key(team, match.key)] = team_epas[team]
        for team in blue:
            blue_epa_pre[team] = team_epas[team]
            team_match_ids[get_team_match_key(team, match.key)] = team_epas[team]

        red_epa_sum = sum(red_epa_pre.values())
        blue_epa_sum = sum(blue_epa_pre.values())

        match.red_epa_sum = round(red_epa_sum, 2)
        match.blue_epa_sum = round(blue_epa_sum, 2)

        red_auto_epa_pre: Dict[int, float] = {}
        blue_auto_epa_pre: Dict[int, float] = {}
        red_endgame_epa_pre: Dict[int, float] = {}
        blue_endgame_epa_pre: Dict[int, float] = {}
        red_rp_1_epa_pre: Dict[int, float] = {}
        blue_rp_1_epa_pre: Dict[int, float] = {}
        red_rp_2_epa_pre: Dict[int, float] = {}
        blue_rp_2_epa_pre: Dict[int, float] = {}
        if USE_COMPONENTS:
            for team in red:
                red_auto_epa_pre[team] = team_auto_epas[team]
                red_endgame_epa_pre[team] = team_endgame_epas[team]
                red_rp_1_epa_pre[team] = team_rp_1_epas[team]
                red_rp_2_epa_pre[team] = team_rp_2_epas[team]
                component_team_match_ids[get_team_match_key(team, match.key)] = (
                    team_auto_epas[team],
                    team_teleop_epas[team],
                    team_endgame_epas[team],
                    team_rp_1_epas[team],
                    team_rp_2_epas[team],
                )
            for team in blue:
                blue_auto_epa_pre[team] = team_auto_epas[team]
                blue_endgame_epa_pre[team] = team_endgame_epas[team]
                blue_rp_1_epa_pre[team] = team_rp_1_epas[team]
                blue_rp_2_epa_pre[team] = team_rp_2_epas[team]
                component_team_match_ids[get_team_match_key(team, match.key)] = (
                    team_auto_epas[team],
                    team_teleop_epas[team],
                    team_endgame_epas[team],
                    team_rp_1_epas[team],
                    team_rp_2_epas[team],
                )

            red_auto_epa_sum = sum(red_auto_epa_pre.values())
            blue_auto_epa_sum = sum(blue_auto_epa_pre.values())
            red_endgame_epa_sum = sum(red_endgame_epa_pre.values())
            blue_endgame_epa_sum = sum(blue_endgame_epa_pre.values())
            red_rp_1_epa_sum = sum(list(red_rp_1_epa_pre.values()))
            blue_rp_1_epa_sum = sum(list(blue_rp_1_epa_pre.values()))
            red_rp_2_epa_sum = sum(list(red_rp_2_epa_pre.values()))
            blue_rp_2_epa_sum = sum(list(blue_rp_2_epa_pre.values()))

            match.red_auto_epa_sum = round(red_auto_epa_sum, 2)
            match.blue_auto_epa_sum = round(blue_auto_epa_sum, 2)
            match.red_endgame_epa_sum = round(red_endgame_epa_sum, 2)
            match.blue_endgame_epa_sum = round(blue_endgame_epa_sum, 2)
            match.red_teleop_epa_sum = round(match.red_epa_sum - red_auto_epa_sum - red_endgame_epa_sum, 2)  # type: ignore
            match.blue_teleop_epa_sum = round(match.blue_epa_sum - blue_auto_epa_sum - blue_endgame_epa_sum, 2)  # type: ignore
            match.red_rp_1_epa_sum = round(red_rp_1_epa_sum, 4)
            match.blue_rp_1_epa_sum = round(blue_rp_1_epa_sum, 4)
            match.red_rp_2_epa_sum = round(red_rp_2_epa_sum, 4)
            match.blue_rp_2_epa_sum = round(blue_rp_2_epa_sum, 4)

            match.red_rp_1_prob = round(sigmoid(red_rp_1_epa_sum), 4)
            match.blue_rp_1_prob = round(sigmoid(blue_rp_1_epa_sum), 4)
            match.red_rp_2_prob = round(sigmoid(red_rp_2_epa_sum), 4)
            match.blue_rp_2_prob = round(sigmoid(blue_rp_2_epa_sum), 4)

        norm_diff = (match.red_epa_sum - match.blue_epa_sum) / TOTAL_SD
        win_prob = 1 / (1 + 10 ** (K * norm_diff))

        match.epa_win_prob = round(win_prob, 4)
        match.epa_winner = "red" if win_prob >= 0.5 else "blue"

        for teams, epa_dict in [(red, red_epa_pre), (blue, blue_epa_pre)]:
            for t in teams:
                team_event_key = get_team_event_key(t, event_key)
                if team_event_key not in team_events_dict:
                    team_events_dict[team_event_key] = [(epa_dict[t], match.playoff)]
                    if USE_COMPONENTS:
                        (
                            auto_epa,
                            teleop_epa,
                            endgame_epa,
                            rp_1_epa,
                            rp_2_epa,
                        ) = component_team_match_ids[get_team_match_key(t, match.key)]
                        component_team_events_dict[team_event_key] = [
                            (
                                auto_epa,
                                teleop_epa,
                                endgame_epa,
                                rp_1_epa,
                                rp_2_epa,
                                match.playoff,
                            )
                        ]

        winner = match.winner or "red"  # in practice, never None
        red_mapping = {"red": 0, "blue": 1, "draw": 2}
        blue_mapping = {"blue": 0, "red": 1, "draw": 2}

        # UPDATE EPA
        weight = PLAYOFF_WEIGHT if match.playoff else 1
        rp_weight = 0 if match.playoff else 1
        red_score = match.red_no_fouls or match.red_score or 0
        red_pred = match.red_epa_sum
        blue_score = match.blue_no_fouls or match.blue_score or 0
        blue_pred = match.blue_epa_sum

        # Track surrogates and DQs for RP calculations
        red_surrogates = [
            int(x) for x in (match.red_surrogate or "").split(",") if x != ""
        ]
        blue_surrogates = [
            int(x) for x in (match.blue_surrogate or "").split(",") if x != ""
        ]
        red_dqs = [int(x) for x in (match.red_dq or "").split(",") if x != ""]
        blue_dqs = [int(x) for x in (match.blue_dq or "").split(",") if x != ""]

        # If either, do not update EPA values
        playoff_dq = match.playoff and (len(red_dqs) == 3 or len(blue_dqs) == 3)
        offseason_event = event_types[match.event] > 10

        for (
            teams,
            my_score,
            my_pred,
            opp_score,
            opp_pred,
            epa_pre,
            my_rp_1,
            my_rp_2,
            mapping,
            surrogates,
            dqs,
        ) in [
            (
                red,
                red_score,
                red_pred,
                blue_score,
                blue_pred,
                red_epa_pre,
                match.red_rp_1 or 0,
                match.red_rp_2 or 0,
                red_mapping,
                red_surrogates,
                red_dqs,
            ),
            (
                blue,
                blue_score,
                blue_pred,
                red_score,
                red_pred,
                blue_epa_pre,
                match.blue_rp_1 or 0,
                match.blue_rp_2 or 0,
                blue_mapping,
                blue_surrogates,
                blue_dqs,
            ),
        ]:
            for t in teams:
                team_count = team_counts[t]
                percent = percent_func(year_num, team_count)
                margin = margin_func(year_num, team_count)
                my_error, opp_error = (my_score - my_pred), (opp_score - opp_pred)
                error = (my_error - margin * opp_error) / (1 + margin)
                new_epa = max(0, epa_pre[t] + weight * percent * error / NUM_TEAMS)

                # Skip EPA update for playoff DQs
                if playoff_dq or offseason_event:
                    new_epa = epa_pre[t]

                team_epas[t] = new_epa
                team_event_key = get_team_event_key(t, event_key)
                team_events_dict[team_event_key].append((new_epa, match.playoff))
                team_matches_dict[t].append(new_epa)

                if not offseason_event:
                    team_year_stats[t][mapping[winner]] += 1
                    team_year_stats[t][3] += 1

                full_team_year_stats[t][mapping[winner]] += 1
                full_team_year_stats[t][3] += 1

                team_event_stats[team_event_key][mapping[winner]] += 1
                team_event_stats[team_event_key][3] += 1

                if not match.playoff:
                    if t not in surrogates:  # Count win/loss/ties for all qual matches
                        qual_team_event_stats[team_event_key][mapping[winner]] += 1
                        qual_team_event_stats[team_event_key][4] += 1
                    if t not in surrogates and t not in dqs:  # count RPs if not DQ
                        rps = my_rp_1 + my_rp_2 + (2 if mapping[winner] == 0 else 0)
                        qual_team_event_stats[team_event_key][3] += rps

                if not match.playoff and not offseason_event:
                    team_counts[t] += 1  # for EPA calculation

        if USE_COMPONENTS:
            red_auto_err = (match.red_auto or 0) - (match.red_auto_epa_sum or 0)
            blue_auto_err = (match.blue_auto or 0) - (match.blue_auto_epa_sum or 0)
            red_endgame_err = (match.red_endgame or 0) - (
                match.red_endgame_epa_sum or 0
            )
            blue_endgame_err = (match.blue_endgame or 0) - (
                match.blue_endgame_epa_sum or 0
            )
            red_rp_1_err = (match.red_rp_1 or 0) - (match.red_rp_1_prob or 0)
            blue_rp_1_err = (match.blue_rp_1 or 0) - (match.blue_rp_1_prob or 0)
            red_rp_2_err = (match.red_rp_2 or 0) - (match.red_rp_2_prob or 0)
            blue_rp_2_err = (match.blue_rp_2 or 0) - (match.blue_rp_2_prob or 0)
            for (
                teams,
                auto_epa_pre,
                endgame_epa_pre,
                rp_1_epa_pre,
                rp_2_epa_pre,
                auto_err,
                endgame_err,
                rp_1_err,
                rp_2_err,
            ) in [
                (red, red_auto_epa_pre, red_endgame_epa_pre, red_rp_1_epa_pre, red_rp_2_epa_pre, red_auto_err, red_endgame_err, red_rp_1_err, red_rp_2_err),  # type: ignore
                (blue, blue_auto_epa_pre, blue_endgame_epa_pre, blue_rp_1_epa_pre, blue_rp_2_epa_pre, blue_auto_err, blue_endgame_err, blue_rp_1_err, blue_rp_2_err),  # type: ignore
            ]:
                for t in teams:
                    a_epa = auto_epa_pre[t] + weight * percent * auto_err / NUM_TEAMS  # type: ignore
                    e_epa = endgame_epa_pre[t] + weight * percent * endgame_err / NUM_TEAMS  # type: ignore
                    t_epa = team_epas[t] - a_epa - e_epa  # type: ignore
                    rp_1_epa = max(MIN_RP_EPA, rp_1_epa_pre[t] + rp_weight * RP_PERCENT * rp_1_err / NUM_TEAMS)  # type: ignore
                    rp_2_epa = max(MIN_RP_EPA, rp_2_epa_pre[t] + rp_weight * RP_PERCENT * rp_2_err / NUM_TEAMS)  # type: ignore

                    if playoff_dq or offseason_event:
                        a_epa = auto_epa_pre[t]
                        e_epa = endgame_epa_pre[t]
                        t_epa = team_epas[t] - a_epa - e_epa
                        rp_1_epa = rp_1_epa_pre[t]
                        rp_2_epa = rp_2_epa_pre[t]

                    team_auto_epas[t] = a_epa
                    team_teleop_epas[t] = t_epa
                    team_endgame_epas[t] = e_epa
                    team_rp_1_epas[t] = rp_1_epa
                    team_rp_2_epas[t] = rp_2_epa
                    team_event_key = get_team_event_key(t, event_key)
                    component_team_events_dict[team_event_key].append(
                        (a_epa, t_epa, e_epa, rp_1_epa, rp_2_epa, match.playoff)
                    )
                    component_team_matches_dict[t].append(
                        (a_epa, t_epa, e_epa, rp_1_epa, rp_2_epa)
                    )

        win_probs = {"red": 1, "blue": 0, "draw": 0.5}
        new_acc = 1 if winner == match.epa_winner else 0
        new_mse = (win_probs[winner] - match.epa_win_prob) ** 2
        _a, _m, _c = event_stats[event_key]
        event_stats[event_key] = (_a + new_acc, _m + new_mse, _c + 1)

        if offseason_event:
            continue

        acc += new_acc
        mse += new_mse
        count += 1
        if match.playoff:
            elims_mse += new_mse
            elims_acc += new_acc
            elims_count += 1
        else:
            quals_mse += new_mse
            quals_acc += new_acc
            quals_count += 1
        if event_weeks[match.event] == 8:
            champs_mse += new_mse
            champs_acc += new_acc
            champs_count += 1

        if not match.playoff and USE_COMPONENTS:
            rp_1_new_acc = 0
            rp_1_new_mse = 0
            if (match.red_rp_1 or 0) == round(match.red_rp_1_prob or 0):
                rp_1_new_acc += 1
            if (match.blue_rp_1 or 0) == round(match.blue_rp_1_prob or 0):
                rp_1_new_acc += 1
            rp_1_new_mse += ((match.red_rp_1 or 0) - (match.red_rp_1_prob or 0)) ** 2
            rp_1_new_mse += ((match.blue_rp_1 or 0) - (match.blue_rp_1_prob or 0)) ** 2

            rp_2_new_acc = 0
            rp_2_new_mse = 0
            if (match.red_rp_2 or 0) == round(match.red_rp_2_prob or 0):
                rp_2_new_acc += 1
            if (match.blue_rp_2 or 0) == round(match.blue_rp_2_prob or 0):
                rp_2_new_acc += 1
            rp_2_new_mse += ((match.red_rp_2 or 0) - (match.red_rp_2_prob or 0)) ** 2
            rp_2_new_mse += ((match.blue_rp_2 or 0) - (match.blue_rp_2_prob or 0)) ** 2

            _a, _m, _c = rp_1_event_stats[event_key]
            rp_1_event_stats[event_key] = (_a + rp_1_new_acc, _m + rp_1_new_mse, _c + 2)

            _a, _m, _c = rp_2_event_stats[event_key]
            rp_2_event_stats[event_key] = (_a + rp_2_new_acc, _m + rp_2_new_mse, _c + 2)

            rp_1_acc += rp_1_new_acc
            rp_1_mse += rp_1_new_mse
            rp_1_count += 2

            rp_2_acc += rp_2_new_acc
            rp_2_mse += rp_2_new_mse
            rp_2_count += 2

            if event_weeks[match.event] == 8:
                champs_rp_1_mse += rp_1_new_mse
                champs_rp_1_acc += rp_1_new_acc
                champs_rp_1_count += 2

                champs_rp_2_mse += rp_2_new_mse
                champs_rp_2_acc += rp_2_new_acc
                champs_rp_2_count += 2

    acc = None if count == 0 else round(acc / count, 4)
    mse = None if count == 0 else round(mse / count, 4)
    elims_acc = None if elims_count == 0 else round(elims_acc / elims_count, 4)
    elims_mse = None if elims_count == 0 else round(elims_mse / elims_count, 4)
    quals_acc = None if quals_count == 0 else round(quals_acc / quals_count, 4)
    quals_mse = None if quals_count == 0 else round(quals_mse / quals_count, 4)
    champs_acc = None if champs_count == 0 else round(champs_acc / champs_count, 4)
    champs_mse = None if champs_count == 0 else round(champs_mse / champs_count, 4)

    rp_1_acc = None if rp_1_count == 0 else round(rp_1_acc / rp_1_count, 4)
    rp_1_mse = None if rp_1_count == 0 else round(rp_1_mse / rp_1_count, 4)
    rp_2_acc = None if rp_2_count == 0 else round(rp_2_acc / rp_2_count, 4)
    rp_2_mse = None if rp_2_count == 0 else round(rp_2_mse / rp_2_count, 4)
    champs_rp_1_acc = None if champs_rp_1_count == 0 else round(champs_rp_1_acc / champs_rp_1_count, 4)  # type: ignore
    champs_rp_1_mse = None if champs_rp_1_count == 0 else round(champs_rp_1_mse / champs_rp_1_count, 4)  # type: ignore
    champs_rp_2_acc = None if champs_rp_2_count == 0 else round(champs_rp_2_acc / champs_rp_2_count, 4)  # type: ignore
    champs_rp_2_mse = None if champs_rp_2_count == 0 else round(champs_rp_2_mse / champs_rp_2_count, 4)  # type: ignore

    # TEAM MATCHES
    completed_team_matches = [m for m in team_matches if m.status == "Completed"]
    for team_match in completed_team_matches:
        match_key = get_team_match_key(team_match.team, team_match.match)
        team_match.epa = round(team_match_ids[match_key], 2)
        if USE_COMPONENTS:
            auto, teleop, endgame, rp_1, rp_2 = component_team_match_ids[match_key]
            team_match.auto_epa = round(auto, 2)
            team_match.teleop_epa = round(teleop, 2)
            team_match.endgame_epa = round(endgame, 2)
            team_match.rp_1_epa = round(rp_1, 4)
            team_match.rp_2_epa = round(rp_2, 4)

    # TEAM EVENTS
    event_team_events: Dict[str, List[TeamEvent]] = defaultdict(list)
    team_team_events: Dict[int, List[TeamEvent]] = defaultdict(list)
    for team_event in sorted(team_events, key=lambda e: (e.week, e.time)):
        key = get_team_event_key(team_event.team, team_event.event)
        event_team_events[team_event.event].append(team_event)
        team_team_events[team_event.team].append(team_event)

        upcoming_epas = [(team_epas[team_event.team], False)]
        epas = [obj[0] for obj in team_events_dict.get(key, upcoming_epas)]
        qual_epas = [obj[0] for obj in team_events_dict.get(key, upcoming_epas) if not obj[1]]  # type: ignore

        team_event.epa_start = round(epas[0], 2)
        team_event.epa_end = round(epas[-1], 2)
        team_event.epa_max = round(max(epas), 2)
        team_event.epa_mean = round(sum(epas) / len(epas), 2)
        team_event.epa_diff = round(epas[-1] - epas[0], 2)
        epa_pre_playoffs = epas[0] if len(qual_epas) == 0 else qual_epas[-1]
        team_event.epa_pre_playoffs = round(epa_pre_playoffs, 2)

        if USE_COMPONENTS:
            component_epas = [obj[0:5] for obj in component_team_events_dict[key]]
            qual_component_epas = [
                obj[0:5] for obj in component_team_events_dict[key] if not obj[-1]  # type: ignore
            ]

            auto_epas = [obj[0] for obj in component_epas]
            teleop_epas = [obj[1] for obj in component_epas]
            endgame_epas = [obj[2] for obj in component_epas]

            auto_qual_epas = [obj[0] for obj in qual_component_epas]
            teleop_qual_epas = [obj[1] for obj in qual_component_epas]
            endgame_qual_epas = [obj[2] for obj in qual_component_epas]
            rp_1_qual_epas = [obj[3] for obj in qual_component_epas]
            rp_2_qual_epas = [obj[4] for obj in qual_component_epas]

            team_event.auto_epa_start = round(auto_epas[0], 2)
            team_event.auto_epa_end = round(auto_epas[-1], 2)
            team_event.auto_epa_max = round(max(auto_epas), 2)
            team_event.auto_epa_mean = round(sum(auto_epas) / len(auto_epas), 2)
            auto_epa_pre_playoffs = auto_epas[0]
            if len(auto_qual_epas) > 0:
                auto_epa_pre_playoffs = auto_qual_epas[-1]
            team_event.auto_epa_pre_playoffs = round(auto_epa_pre_playoffs, 2)

            team_event.teleop_epa_start = round(teleop_epas[0], 2)
            team_event.teleop_epa_end = round(teleop_epas[-1], 2)
            team_event.teleop_epa_max = round(max(teleop_epas), 2)
            team_event.teleop_epa_mean = round(sum(teleop_epas) / len(teleop_epas), 2)
            teleop_epa_pre_playoffs = teleop_epas[0]
            if len(teleop_qual_epas) > 0:
                teleop_epa_pre_playoffs = teleop_qual_epas[-1]
            team_event.teleop_epa_pre_playoffs = round(teleop_epa_pre_playoffs, 2)

            team_event.endgame_epa_start = round(endgame_epas[0], 2)
            team_event.endgame_epa_end = round(endgame_epas[-1], 2)
            team_event.endgame_epa_max = round(max(endgame_epas), 2)
            team_event.endgame_epa_mean = round(sum(endgame_epas) / len(endgame_epas), 2)  # type: ignore
            endgame_epa_pre_playoffs = endgame_epas[0]
            if len(endgame_qual_epas) > 0:
                endgame_epa_pre_playoffs = endgame_qual_epas[-1]
            team_event.endgame_epa_pre_playoffs = round(endgame_epa_pre_playoffs, 2)

            if len(rp_1_qual_epas) > 0:
                team_event.rp_1_epa_start = round(rp_1_qual_epas[0], 4)
                team_event.rp_1_epa_end = round(rp_1_qual_epas[-1], 4)
                team_event.rp_1_epa_max = round(max(rp_1_qual_epas), 4)
                team_event.rp_1_epa_mean = round(sum(rp_1_qual_epas) / len(rp_1_qual_epas), 4)  # type: ignore

            if len(rp_2_qual_epas) > 0:
                team_event.rp_2_epa_start = round(rp_2_qual_epas[0], 4)
                team_event.rp_2_epa_end = round(rp_2_qual_epas[-1], 4)
                team_event.rp_2_epa_max = round(max(rp_2_qual_epas), 4)
                team_event.rp_2_epa_mean = round(sum(rp_2_qual_epas) / len(rp_2_qual_epas), 4)  # type: ignore

        wins, losses, ties, event_count = team_event_stats[key]
        winrate = round((wins + ties / 2) / max(1, event_count), 4)
        team_event.wins = wins
        team_event.losses = losses
        team_event.ties = ties
        team_event.count = event_count
        team_event.winrate = winrate

        (
            qual_wins,
            qual_losses,
            qual_ties,
            qual_rps,
            qual_event_count,
        ) = qual_team_event_stats[key]
        team_event.qual_wins = qual_wins
        team_event.qual_losses = qual_losses
        team_event.qual_ties = qual_ties
        team_event.rps = qual_rps
        team_event.rps_per_match = qual_rps / max(1, qual_event_count)
        team_event.qual_count = qual_event_count

    # EVENTS
    filtered_events = [e for e in events if e.status != "Upcoming"]
    for event in filtered_events:
        event_key = event.key

        event_epas: List[float] = []
        for team_event in event_team_events[event_key]:
            event_epas.append(team_event.epa_pre_playoffs or 0)
        event_epas.sort(reverse=True)

        if len(event_epas) > 0 and max(event_epas) > 0:
            event.epa_max = round(event_epas[0], 2)
            event.epa_top8 = None if len(event_epas) < 8 else round(event_epas[7], 2)
            event.epa_top24 = None if len(event_epas) < 24 else round(event_epas[23], 2)
            event.epa_mean = round(sum(event_epas) / len(event_epas), 2)
            event.epa_sd = round(stdev(event_epas), 2)

        event_acc, event_mse, event_count = event_stats[event_key]
        event.epa_acc = None if event_count == 0 else round(event_acc / event_count, 4)
        event.epa_mse = None if event_count == 0 else round(event_mse / event_count, 4)

        event_rp_1_acc, event_mse, event_count = rp_1_event_stats[event_key]
        event.rp_1_acc = (
            None if event_count == 0 else round(event_rp_1_acc / event_count, 4)
        )
        event.rp_1_mse = None if event_count == 0 else round(event_mse / event_count, 4)

        event_rp_2_acc, event_mse, event_count = rp_2_event_stats[event_key]
        event.rp_2_acc = (
            None if event_count == 0 else round(event_rp_2_acc / event_count, 4)
        )
        event.rp_2_mse = None if event_count == 0 else round(event_mse / event_count, 4)

    # TEAM YEARS
    year_epas: List[float] = []
    year_epas_dict: Dict[int, float] = {}  # for norm epa
    country_year_epas: Dict[str, List[float]] = defaultdict(list)  # for rank/percentile
    state_year_epas: Dict[str, List[float]] = defaultdict(list)
    district_year_epas: Dict[str, List[float]] = defaultdict(list)
    year_auto_epas: List[float] = []
    year_teleop_epas: List[float] = []
    year_endgame_epas: List[float] = []
    year_rp_1_epas: List[float] = []
    year_rp_2_epas: List[float] = []
    to_remove: List[int] = []
    for team in team_years_dict:
        curr_team_epas = team_matches_dict[team]
        if curr_team_epas == []:
            to_remove.append(team)
            continue

        # Use end of season epa
        end_epa = curr_team_epas[-1]
        year_epas.append(round(end_epa, 2))
        year_epas_dict[team] = round(end_epa, 2)

        team_year_obj = team_years_dict[team]
        if team_year_obj.country is not None:
            country_year_epas[team_year_obj.country].append(round(end_epa, 2))
        if team_year_obj.state is not None:
            state_year_epas[team_year_obj.state].append(round(end_epa, 2))
        if team_year_obj.district is not None:
            district_year_epas[team_year_obj.district].append(round(end_epa, 2))

        if USE_COMPONENTS:
            curr_component_team_epas = component_team_matches_dict[team]
            year_auto_epas.append(round(curr_component_team_epas[-1][0], 2))
            year_teleop_epas.append(round(curr_component_team_epas[-1][1], 2))
            year_endgame_epas.append(round(curr_component_team_epas[-1][2], 2))
            year_rp_1_epas.append(round(curr_component_team_epas[-1][3], 4))
            year_rp_2_epas.append(round(curr_component_team_epas[-1][4], 4))

    for team in to_remove:
        team_years_dict.pop(team)

    year_epas.sort(reverse=True)
    country_year_epas = {
        k: sorted(v, reverse=True) for k, v in country_year_epas.items()
    }
    state_year_epas = {k: sorted(v, reverse=True) for k, v in state_year_epas.items()}
    district_year_epas = {
        k: sorted(v, reverse=True) for k, v in district_year_epas.items()
    }

    total_N, cutoff_N = len(year_epas), int(len(year_epas) / 10)
    exponnorm_disrib = None if total_N == 0 else exponnorm(*exponnorm.fit(year_epas))  # type: ignore
    expon_distrib = None if cutoff_N == 0 else expon(*expon.fit(year_epas[:cutoff_N]))  # type: ignore

    def get_norm_epa(epa: float, i: int) -> float:
        exponnorm_value: float = exponnorm_disrib.cdf(epa)  # type: ignore
        percentile = exponnorm_value
        if i < cutoff_N:
            expon_value: float = expon_distrib.cdf(epa)  # type: ignore
            expon_value = 1 - cutoff_N / total_N * (1 - expon_value)
            # Linearly interpolate between the two distributions from 10% to 5%
            expon_frac = min(1, 2 * (cutoff_N - i) / cutoff_N)
            percentile = expon_frac * expon_value + (1 - expon_frac) * exponnorm_value
        out: float = distrib.ppf(percentile)  # type: ignore
        return NORM_MEAN + NORM_SD * out

    team_year_count = len(team_years_dict)
    for team in team_years_dict:
        obj = team_years_dict[team]
        curr_team_epas = team_matches_dict[team]
        curr_component_team_epas = component_team_matches_dict[team]
        curr_auto_team_epas = [x[0] for x in curr_component_team_epas]
        curr_teleop_team_epas = [x[1] for x in curr_component_team_epas]
        curr_endgame_team_epas = [x[2] for x in curr_component_team_epas]
        curr_rp_1_team_epas = [x[3] for x in curr_component_team_epas]
        curr_rp_2_team_epas = [x[4] for x in curr_component_team_epas]

        n = len(curr_team_epas)
        obj.epa_max = round(max(curr_team_epas[min(n - 1, 8) :]), 2)
        obj.epa_mean = round(sum(curr_team_epas) / n, 2)
        obj.epa_end = round(team_epas[team], 2)
        obj.epa_diff = round(obj.epa_end - (obj.epa_start or 0), 2)

        epa_index = year_epas.index(obj.epa_end)
        obj.norm_epa_end = round(get_norm_epa(obj.epa_end, epa_index), 2)

        if USE_COMPONENTS:
            obj.auto_epa_max = round(max(curr_auto_team_epas[min(n - 1, 8) :]), 2)
            obj.auto_epa_mean = round(sum(curr_auto_team_epas) / n, 2)
            obj.auto_epa_end = round(team_auto_epas[team], 2)

            obj.teleop_epa_max = round(max(curr_teleop_team_epas[min(n - 1, 8) :]), 2)
            obj.teleop_epa_mean = round(sum(curr_teleop_team_epas) / n, 2)
            obj.teleop_epa_end = round(team_teleop_epas[team], 2)

            obj.endgame_epa_max = round(max(curr_endgame_team_epas[min(n - 1, 8) :]), 2)
            obj.endgame_epa_mean = round(sum(curr_endgame_team_epas) / n, 2)
            obj.endgame_epa_end = round(team_endgame_epas[team], 2)

            obj.rp_1_epa_max = round(max(curr_rp_1_team_epas[min(n - 1, 8) :]), 4)
            obj.rp_1_epa_mean = round(sum(curr_rp_1_team_epas) / n, 4)
            obj.rp_1_epa_end = round(team_rp_1_epas[team], 4)

            obj.rp_2_epa_max = round(max(curr_rp_2_team_epas[min(n - 1, 8) :]), 4)
            obj.rp_2_epa_mean = round(sum(curr_rp_2_team_epas) / n, 4)
            obj.rp_2_epa_end = round(team_rp_2_epas[team], 4)

        pre_champs = obj.epa_start or 0
        auto_pre_champs = obj.auto_epa_start or 0
        teleop_pre_champs = obj.teleop_epa_start or 0
        endgame_pre_champs = obj.endgame_epa_start or 0
        rp_1_pre_champs = obj.rp_1_epa_start or 0
        rp_2_pre_champs = obj.rp_2_epa_start or 0
        for team_event in sorted(team_team_events[team], key=lambda t: t.sort()):
            if event_types[team_event.event] < 3 and team_event.epa_end is not None:
                pre_champs = team_event.epa_end
                auto_pre_champs = team_event.auto_epa_end or 0
                teleop_pre_champs = team_event.teleop_epa_end or 0
                endgame_pre_champs = team_event.endgame_epa_end or 0
                rp_1_pre_champs = team_event.rp_1_epa_end or 0
                rp_2_pre_champs = team_event.rp_2_epa_end or 0
        obj.epa_pre_champs = round(pre_champs, 2)
        if USE_COMPONENTS:
            obj.auto_epa_pre_champs = round(auto_pre_champs, 2)
            obj.teleop_epa_pre_champs = round(teleop_pre_champs, 2)
            obj.endgame_epa_pre_champs = round(endgame_pre_champs, 2)
            obj.rp_1_epa_pre_champs = round(rp_1_pre_champs, 4)
            obj.rp_2_epa_pre_champs = round(rp_2_pre_champs, 4)

        wins, losses, ties, team_count = team_year_stats[team]
        winrate = round((wins + ties / 2) / max(1, team_count), 4)
        obj.wins = wins
        obj.losses = losses
        obj.ties = ties
        obj.count = team_count
        obj.winrate = winrate

        wins, losses, ties, team_count = full_team_year_stats[team]
        winrate = round((wins + ties / 2) / max(1, team_count), 4)
        obj.full_wins = wins
        obj.full_losses = losses
        obj.full_ties = ties
        obj.full_count = team_count
        obj.full_winrate = winrate

        obj.total_epa_rank = rank = year_epas.index(obj.epa_end) + 1
        obj.total_epa_percentile = round(1 - rank / team_year_count, 4)
        obj.total_team_count = team_year_count

        if obj.country is not None:
            rank = country_year_epas[obj.country].index(obj.epa_end) + 1
            country_count = len(country_year_epas[obj.country])
            obj.country_epa_rank = rank
            obj.country_epa_percentile = round(1 - rank / country_count, 4)
            obj.country_team_count = country_count
        if obj.state is not None:
            rank = state_year_epas[obj.state].index(obj.epa_end) + 1
            state_count = len(state_year_epas[obj.state])
            obj.state_epa_rank = rank
            obj.state_epa_percentile = round(1 - rank / state_count, 4)
            obj.state_team_count = state_count
        if obj.district is not None:
            rank = district_year_epas[obj.district].index(obj.epa_end) + 1
            district_count = len(district_year_epas[obj.district])
            obj.district_epa_rank = rank
            obj.district_epa_percentile = round(1 - rank / district_count, 4)
            obj.district_team_count = district_count

    # YEARS
    if len(year_epas) > 0:
        year_epas.sort(reverse=True)
        year.epa_max = round(year_epas[0], 2)
        year.epa_1p = round(year_epas[round(0.01 * len(year_epas))], 2)
        year.epa_5p = round(year_epas[round(0.05 * len(year_epas))], 2)
        year.epa_10p = round(year_epas[round(0.1 * len(year_epas))], 2)
        year.epa_25p = round(year_epas[round(0.25 * len(year_epas))], 2)
        year.epa_median = round(year_epas[round(0.5 * len(year_epas))], 2)
        year.epa_75p = round(year_epas[round(0.75 * len(year_epas))], 2)
        year.epa_mean = round(sum(year_epas) / len(year_epas), 2)
        year.epa_sd = round(stdev(year_epas), 2)

        if USE_COMPONENTS:
            year_auto_epas.sort(reverse=True)
            year.auto_epa_max = round(year_auto_epas[0], 2)
            year.auto_epa_1p = round(
                year_auto_epas[round(0.01 * len(year_auto_epas))], 2
            )
            year.auto_epa_5p = round(
                year_auto_epas[round(0.05 * len(year_auto_epas))], 2
            )
            year.auto_epa_10p = round(
                year_auto_epas[round(0.1 * len(year_auto_epas))], 2
            )
            year.auto_epa_25p = round(
                year_auto_epas[round(0.25 * len(year_auto_epas))], 2
            )
            year.auto_epa_median = round(
                year_auto_epas[round(0.5 * len(year_auto_epas))], 2
            )
            year.auto_epa_75p = round(
                year_auto_epas[round(0.75 * len(year_auto_epas))], 2
            )
            year.auto_epa_mean = round(sum(year_auto_epas) / len(year_auto_epas), 2)
            year.auto_epa_sd = round(stdev(year_auto_epas), 2)

            year_teleop_epas.sort(reverse=True)
            year.teleop_epa_max = round(year_teleop_epas[0], 2)
            year.teleop_epa_1p = round(
                year_teleop_epas[round(0.01 * len(year_teleop_epas))], 2
            )
            year.teleop_epa_5p = round(
                year_teleop_epas[round(0.05 * len(year_teleop_epas))], 2
            )
            year.teleop_epa_10p = round(
                year_teleop_epas[round(0.1 * len(year_teleop_epas))], 2
            )
            year.teleop_epa_25p = round(
                year_teleop_epas[round(0.25 * len(year_teleop_epas))], 2
            )
            year.teleop_epa_median = round(
                year_teleop_epas[round(0.5 * len(year_teleop_epas))], 2
            )
            year.teleop_epa_75p = round(
                year_teleop_epas[round(0.75 * len(year_teleop_epas))], 2
            )
            year.teleop_epa_mean = round(
                sum(year_teleop_epas) / len(year_teleop_epas), 2
            )
            year.teleop_epa_sd = round(stdev(year_teleop_epas), 2)

            year_endgame_epas.sort(reverse=True)
            year.endgame_epa_max = round(year_endgame_epas[0], 2)
            year.endgame_epa_1p = round(
                year_endgame_epas[round(0.01 * len(year_endgame_epas))], 2
            )
            year.endgame_epa_5p = round(
                year_endgame_epas[round(0.05 * len(year_endgame_epas))], 2
            )
            year.endgame_epa_10p = round(
                year_endgame_epas[round(0.1 * len(year_endgame_epas))], 2
            )
            year.endgame_epa_25p = round(
                year_endgame_epas[round(0.25 * len(year_endgame_epas))], 2
            )
            year.endgame_epa_median = round(
                year_endgame_epas[round(0.5 * len(year_endgame_epas))], 2
            )
            year.endgame_epa_75p = round(
                year_endgame_epas[round(0.75 * len(year_endgame_epas))], 2
            )
            year.endgame_epa_mean = round(
                sum(year_endgame_epas) / len(year_endgame_epas), 2
            )
            year.endgame_epa_sd = round(stdev(year_endgame_epas), 2)

            year_rp_1_epas.sort(reverse=True)
            year.rp_1_epa_max = round(year_rp_1_epas[0], 4)
            year.rp_1_epa_1p = round(
                year_rp_1_epas[round(0.01 * len(year_rp_1_epas))], 4
            )
            year.rp_1_epa_5p = round(
                year_rp_1_epas[round(0.05 * len(year_rp_1_epas))], 4
            )
            year.rp_1_epa_10p = round(
                year_rp_1_epas[round(0.1 * len(year_rp_1_epas))], 4
            )
            year.rp_1_epa_25p = round(
                year_rp_1_epas[round(0.25 * len(year_rp_1_epas))], 4
            )
            year.rp_1_epa_median = round(
                year_rp_1_epas[round(0.5 * len(year_rp_1_epas))], 4
            )
            year.rp_1_epa_75p = round(
                year_rp_1_epas[round(0.75 * len(year_rp_1_epas))], 4
            )
            year.rp_1_epa_mean = round(sum(year_rp_1_epas) / len(year_rp_1_epas), 4)
            year.rp_1_epa_sd = round(stdev(year_rp_1_epas), 4)

            year_rp_2_epas.sort(reverse=True)
            year.rp_2_epa_max = round(year_rp_2_epas[0], 4)
            year.rp_2_epa_1p = round(
                year_rp_2_epas[round(0.01 * len(year_rp_2_epas))], 4
            )
            year.rp_2_epa_5p = round(
                year_rp_2_epas[round(0.05 * len(year_rp_2_epas))], 4
            )
            year.rp_2_epa_10p = round(
                year_rp_2_epas[round(0.1 * len(year_rp_2_epas))], 4
            )
            year.rp_2_epa_25p = round(
                year_rp_2_epas[round(0.25 * len(year_rp_2_epas))], 4
            )
            year.rp_2_epa_median = round(
                year_rp_2_epas[round(0.5 * len(year_rp_2_epas))], 4
            )
            year.rp_2_epa_75p = round(
                year_rp_2_epas[round(0.75 * len(year_rp_2_epas))], 4
            )
            year.rp_2_epa_mean = round(sum(year_rp_2_epas) / len(year_rp_2_epas), 4)
            year.rp_2_epa_sd = round(stdev(year_rp_2_epas), 4)

        year.epa_acc = acc
        year.epa_mse = mse
        year.count = count
        year.epa_elims_acc = elims_acc
        year.epa_elims_mse = elims_mse
        year.elims_count = elims_count
        year.epa_quals_acc = quals_acc
        year.epa_quals_mse = quals_mse
        year.quals_count = quals_count
        year.epa_champs_acc = champs_acc
        year.epa_champs_mse = champs_mse
        year.champs_count = champs_count
        year.rp_1_acc = rp_1_acc
        year.rp_1_mse = rp_1_mse
        year.rp_2_acc = rp_2_acc
        year.rp_2_mse = rp_2_mse
        year.rp_count = rp_2_count
        year.rp_1_champs_acc = champs_rp_1_acc
        year.rp_1_champs_mse = champs_rp_1_mse
        year.rp_2_champs_acc = champs_rp_2_acc
        year.rp_2_champs_mse = champs_rp_2_mse
        year.rp_champs_count = champs_rp_1_count

    team_years_all[year_num] = team_years_dict

    return (
        team_years_all,
        year,
        team_years,
        events,
        team_events,
        matches,
        team_matches,
    )


def post_process(end_year: int):
    team_team_years: Dict[int, List[TeamYear]] = defaultdict(list)
    all_team_years = get_team_years_db()
    for team_year in all_team_years:
        team_team_years[team_year.team].append(team_year)

    all_teams = get_teams_db()
    for team in all_teams:
        years: Dict[int, float] = {}
        wins, losses, ties, count = 0, 0, 0, 0
        full_wins, full_losses, full_ties, full_count = 0, 0, 0, 0

        team.active = False
        for team_year in team_team_years[team.team]:
            if team_year.year == end_year:
                team.active = True
            if team_year.norm_epa_end is not None:
                years[team_year.year] = team_year.norm_epa_end

            wins += team_year.wins
            losses += team_year.losses
            ties += team_year.ties
            count += team_year.count

            full_wins += team_year.full_wins
            full_losses += team_year.full_losses
            full_ties += team_year.full_ties
            full_count += team_year.full_count

        keys, values = years.keys(), years.values()

        # get recent epas (last five years)
        recent: List[float] = []
        for year in range(end_year - 5, end_year + 1):
            if year in keys:
                recent.append(years[year])
        r_y, y = len(recent), len(keys)

        team.norm_epa = None if y == 0 else round(years[max(keys)])
        team.norm_epa_recent = None if r_y == 0 else round(sum(recent) / r_y)
        team.norm_epa_mean = None if y == 0 else round(sum(values) / y)
        team.norm_epa_max = None if y == 0 else round(max(values))

        winrate = round((wins + ties / 2) / max(1, count), 4)
        team.wins = wins
        team.losses = losses
        team.ties = ties
        team.count = count
        team.winrate = winrate

        full_winrate = round((full_wins + full_ties / 2) / max(1, full_count), 4)
        team.full_wins = full_wins
        team.full_losses = full_losses
        team.full_ties = full_ties
        team.full_count = full_count
        team.full_winrate = full_winrate

    update_teams_db(all_teams, False)
