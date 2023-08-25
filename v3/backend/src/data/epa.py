from collections import defaultdict
from statistics import stdev
from typing import Dict, List, Tuple

import numpy as np
from scipy.stats import expon, exponnorm  # type: ignore

from src.constants import CURR_YEAR
from src.data.nepa import epa_to_unitless_epa
from src.data.utils import objs_type
from src.db.models import Team, TeamEvent, TeamYear
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

ELIM_WEIGHT = 1 / 3
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
    objs: objs_type, all_team_years: Dict[int, Dict[str, TeamYear]]
) -> objs_type:
    year = objs[0]
    team_years = list(objs[1].values())
    events = list(objs[2].values())
    team_events = list(objs[3].values())
    matches = list(objs[4].values())
    alliances = list(objs[5].values())
    team_matches = list(objs[6].values())
    etags = list(objs[7].values())

    year_num = year.year

    NUM_TEAMS = 2 if year_num <= 2004 else 3
    USE_COMPONENTS = year_num >= 2016
    K = k_func(year_num)

    # no_foul_mean after 2016, score_mean before 2016
    TOTAL_MEAN = year.no_foul_mean or year.score_mean or 0
    TOTAL_SD = year.score_sd or 0
    INIT_EPA = TOTAL_MEAN / NUM_TEAMS - INIT_PENALTY * TOTAL_SD

    RP1_MEAN = year.rp_1_mean or sigmoid(MIN_RP_EPA * NUM_TEAMS)
    RP2_MEAN = year.rp_2_mean or sigmoid(MIN_RP_EPA * NUM_TEAMS)

    RP1_SEED = inv_sigmoid(RP1_MEAN) / NUM_TEAMS
    RP2_SEED = inv_sigmoid(RP2_MEAN) / NUM_TEAMS

    team_counts: Dict[str, int] = defaultdict(int)  # for updating epa
    team_epas: Dict[str, float] = defaultdict(lambda: INIT_EPA)  # most recent epa
    team_rp_1_epas: Dict[str, float] = defaultdict(lambda: RP1_SEED)
    team_rp_2_epas: Dict[str, float] = defaultdict(lambda: RP2_SEED)

    team_years_dict: Dict[str, TeamYear] = {}
    team_events_dict: Dict[str, List[Tuple[float, bool]]] = {}
    team_matches_dict: Dict[str, List[float]] = defaultdict(list)
    team_match_ids: Dict[str, float] = {}
    team_match_ids_post: Dict[str, float] = {}
    component_team_events_dict: Dict[str, List[Tuple[float, float, bool]]] = {}
    component_team_matches_dict: Dict[str, List[Tuple[float, float]]] = defaultdict(
        list
    )
    component_team_match_ids: Dict[str, Tuple[float, float]] = {}

    # INITIALIZE
    for team_year in team_years:
        num = team_year.team
        team_years_dict[num] = team_year
        epa_1yr, epa_2yr = None, None
        if year_num in [2022, 2023]:
            # For 2022 and 2023, use past two years team competed (up to 4 years)
            past_epas: List[float] = []
            for past_year in range(year_num - 1, year_num - 5, -1):
                past_team_year = all_team_years.get(past_year, {}).get(num, None)
                if past_team_year is not None:
                    prev_norm_epa = past_team_year.norm_epa_end or NORM_MEAN
                    new_epa = norm_epa_to_next_season_epa(
                        prev_norm_epa, TOTAL_MEAN, TOTAL_SD, NUM_TEAMS
                    )
                    past_epas.append(new_epa)
            epa_1yr = past_epas[0] if len(past_epas) > 0 else None
            epa_2yr = past_epas[1] if len(past_epas) > 1 else None
        else:
            # Otherwise use the two most recent years (regardless of team activity)
            team_year_1 = all_team_years.get(year_num - 1, {}).get(num, None)
            if team_year_1 is not None:
                prev_norm_epa = team_year_1.norm_epa_end or NORM_MEAN
                epa_1yr = norm_epa_to_next_season_epa(
                    prev_norm_epa, TOTAL_MEAN, TOTAL_SD, NUM_TEAMS
                )
            team_year_2 = all_team_years.get(year_num - 2, {}).get(num, None)
            if team_year_2 is not None:
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
        team_year.epa_pre_champs = round(epa_prior, 2)
        team_year.epa_end = round(epa_prior, 2)
        team_year.epa_mean = round(epa_prior, 2)
        team_year.epa_max = round(epa_prior, 2)
        team_year.epa_diff = 0

        unitless_epa: float = epa_to_unitless_epa(epa_prior, TOTAL_MEAN, TOTAL_SD)
        team_year.unitless_epa_end = round(unitless_epa, 0)

        if USE_COMPONENTS:
            rp_factor = (epa_prior - TOTAL_MEAN / NUM_TEAMS) / (TOTAL_SD)
            team_rp_1_epas[num] = max(MIN_RP_EPA, RP1_SEED + 0.25 * rp_factor)
            team_rp_2_epas[num] = max(MIN_RP_EPA, RP2_SEED + 0.25 * rp_factor)
            team_year.rp_1_epa_start = round(team_rp_1_epas[num], 4)
            team_year.rp_2_epa_start = round(team_rp_2_epas[num], 4)

    acc, mse, count = 0, 0, 0
    qual_acc, qual_mse, qual_count = 0, 0, 0
    elim_acc, elim_mse, elim_count = 0, 0, 0
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

        red_epa_pre: Dict[str, float] = {}
        blue_epa_pre: Dict[str, float] = {}

        for team in red:
            red_epa_pre[team] = team_epas[team]
            team_match_ids[get_team_match_key(team, match.key)] = team_epas[team]
        for team in blue:
            blue_epa_pre[team] = team_epas[team]
            team_match_ids[get_team_match_key(team, match.key)] = team_epas[team]

        red_epa_sum = sum(red_epa_pre.values())
        blue_epa_sum = sum(blue_epa_pre.values())

        match.red_score_pred = round(red_epa_sum, 2)
        match.blue_score_pred = round(blue_epa_sum, 2)

        red_rp_1_epa_pre: Dict[str, float] = {}
        blue_rp_1_epa_pre: Dict[str, float] = {}
        red_rp_2_epa_pre: Dict[str, float] = {}
        blue_rp_2_epa_pre: Dict[str, float] = {}
        if USE_COMPONENTS:
            for team in red:
                red_rp_1_epa_pre[team] = team_rp_1_epas[team]
                red_rp_2_epa_pre[team] = team_rp_2_epas[team]
                component_team_match_ids[get_team_match_key(team, match.key)] = (
                    team_rp_1_epas[team],
                    team_rp_2_epas[team],
                )
            for team in blue:
                blue_rp_1_epa_pre[team] = team_rp_1_epas[team]
                blue_rp_2_epa_pre[team] = team_rp_2_epas[team]
                component_team_match_ids[get_team_match_key(team, match.key)] = (
                    team_rp_1_epas[team],
                    team_rp_2_epas[team],
                )

            red_rp_1_epa_sum = sum(list(red_rp_1_epa_pre.values()))
            blue_rp_1_epa_sum = sum(list(blue_rp_1_epa_pre.values()))
            red_rp_2_epa_sum = sum(list(red_rp_2_epa_pre.values()))
            blue_rp_2_epa_sum = sum(list(blue_rp_2_epa_pre.values()))

            match.red_rp_1_pred = round(sigmoid(red_rp_1_epa_sum), 4)
            match.blue_rp_1_pred = round(sigmoid(blue_rp_1_epa_sum), 4)
            match.red_rp_2_pred = round(sigmoid(red_rp_2_epa_sum), 4)
            match.blue_rp_2_pred = round(sigmoid(blue_rp_2_epa_sum), 4)

        norm_diff = (match.red_score_pred - match.blue_score_pred) / TOTAL_SD
        win_prob = 1 / (1 + 10 ** (K * norm_diff))

        match.epa_win_prob = round(win_prob, 4)
        match.epa_winner = "red" if win_prob >= 0.5 else "blue"

        for teams, epa_dict in [(red, red_epa_pre), (blue, blue_epa_pre)]:
            for t in teams:
                team_event_key = get_team_event_key(t, event_key)
                if team_event_key not in team_events_dict:
                    team_events_dict[team_event_key] = [(epa_dict[t], match.elim)]
                    if USE_COMPONENTS:
                        temp_epas = component_team_match_ids[
                            get_team_match_key(t, match.key)
                        ]
                        component_team_events_dict[team_event_key] = [
                            (*temp_epas, match.elim)
                        ]

        if match.status != "Completed":
            continue

        winner = match.winner or "red"  # in practice, never None

        # UPDATE EPA
        weight = ELIM_WEIGHT if match.elim else 1
        red_score = match.red_no_foul or match.red_score or 0
        red_pred = match.red_score_pred
        blue_score = match.blue_no_foul or match.blue_score or 0
        blue_pred = match.blue_score_pred

        # Track surrogates and DQs for RP calculations
        red_dqs = match.get_red_dqs()
        blue_dqs = match.get_blue_dqs()

        # If either, do not update EPA values
        elim_dq = match.elim and (len(red_dqs) == 3 or len(blue_dqs) == 3)
        offseason_event = event_types[match.event] > 10

        for teams, my_score, my_pred, opp_score, opp_pred, epa_pre in [
            (red, red_score, red_pred, blue_score, blue_pred, red_epa_pre),
            (blue, blue_score, blue_pred, red_score, red_pred, blue_epa_pre),
        ]:
            for t in teams:
                team_count = team_counts[t]
                percent = percent_func(year_num, team_count)
                margin = margin_func(year_num, team_count)
                my_error, opp_error = (my_score - my_pred), (opp_score - opp_pred)
                error = (my_error - margin * opp_error) / (1 + margin)
                new_epa = max(0, epa_pre[t] + weight * percent * error / NUM_TEAMS)

                # Skip EPA update for elim DQs
                if elim_dq or offseason_event:
                    new_epa = epa_pre[t]

                team_epas[t] = new_epa
                team_event_key = get_team_event_key(t, event_key)
                team_events_dict[team_event_key].append((new_epa, match.elim))
                team_matches_dict[t].append(new_epa)
                team_match_ids_post[get_team_match_key(t, match.key)] = new_epa

                if not match.elim and not offseason_event:
                    team_counts[t] += 1  # for EPA calculation

        win_probs = {"red": 1, "blue": 0, "tie": 0.5}
        new_acc = 1 if winner == match.epa_winner else 0
        new_mse = (win_probs[winner] - match.epa_win_prob) ** 2
        _a, _m, _c = event_stats[event_key]
        event_stats[event_key] = (_a + new_acc, _m + new_mse, _c + 1)

        if offseason_event:
            continue

        acc += new_acc
        mse += new_mse
        count += 1
        if match.elim:
            elim_mse += new_mse
            elim_acc += new_acc
            elim_count += 1
        else:
            qual_mse += new_mse
            qual_acc += new_acc
            qual_count += 1
        if event_weeks[match.event] == 8:
            champs_mse += new_mse
            champs_acc += new_acc
            champs_count += 1

        if not match.elim and USE_COMPONENTS:
            rp_1_new_acc = 0
            rp_1_new_mse = 0
            if (match.red_rp_1 or 0) == round(match.red_rp_1_pred or 0):
                rp_1_new_acc += 1
            if (match.blue_rp_1 or 0) == round(match.blue_rp_1_pred or 0):
                rp_1_new_acc += 1
            rp_1_new_mse += ((match.red_rp_1 or 0) - (match.red_rp_1_pred or 0)) ** 2
            rp_1_new_mse += ((match.blue_rp_1 or 0) - (match.blue_rp_1_pred or 0)) ** 2

            rp_2_new_acc = 0
            rp_2_new_mse = 0
            if (match.red_rp_2 or 0) == round(match.red_rp_2_pred or 0):
                rp_2_new_acc += 1
            if (match.blue_rp_2 or 0) == round(match.blue_rp_2_pred or 0):
                rp_2_new_acc += 1
            rp_2_new_mse += ((match.red_rp_2 or 0) - (match.red_rp_2_pred or 0)) ** 2
            rp_2_new_mse += ((match.blue_rp_2 or 0) - (match.blue_rp_2_pred or 0)) ** 2

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
    elim_acc = None if elim_count == 0 else round(elim_acc / elim_count, 4)
    elim_mse = None if elim_count == 0 else round(elim_mse / elim_count, 4)
    qual_acc = None if qual_count == 0 else round(qual_acc / qual_count, 4)
    qual_mse = None if qual_count == 0 else round(qual_mse / qual_count, 4)
    champs_acc = None if champs_count == 0 else round(champs_acc / champs_count, 4)
    champs_mse = None if champs_count == 0 else round(champs_mse / champs_count, 4)

    rp_1_acc = None if rp_1_count == 0 else round(rp_1_acc / rp_1_count, 4)
    rp_1_mse = None if rp_1_count == 0 else round(rp_1_mse / rp_1_count, 4)
    rp_2_acc = None if rp_2_count == 0 else round(rp_2_acc / rp_2_count, 4)
    rp_2_mse = None if rp_2_count == 0 else round(rp_2_mse / rp_2_count, 4)
    champs_rp_1_acc = (
        None
        if champs_rp_1_count == 0
        else round(champs_rp_1_acc / champs_rp_1_count, 4)
    )
    champs_rp_1_mse = (
        None
        if champs_rp_1_count == 0
        else round(champs_rp_1_mse / champs_rp_1_count, 4)
    )
    champs_rp_2_acc = (
        None
        if champs_rp_2_count == 0
        else round(champs_rp_2_acc / champs_rp_2_count, 4)
    )
    champs_rp_2_mse = (
        None
        if champs_rp_2_count == 0
        else round(champs_rp_2_mse / champs_rp_2_count, 4)
    )

    # TEAM MATCHES
    for team_match in team_matches:
        match_key = get_team_match_key(team_match.team, team_match.match)
        team_match.epa = round(team_match_ids.get(match_key, -1), 2)
        if team_match.status == "Completed":
            team_match.post_epa = round(team_match_ids_post.get(match_key, -1), 2)

        if USE_COMPONENTS:
            rp_1, rp_2 = component_team_match_ids.get(match_key, (-1, -1))
            team_match.rp_1_epa = round(rp_1, 4)
            team_match.rp_2_epa = round(rp_2, 4)

    # TEAM EVENTS
    event_team_events: Dict[str, List[TeamEvent]] = defaultdict(list)
    team_team_events: Dict[str, List[TeamEvent]] = defaultdict(list)
    for team_event in sorted(team_events, key=lambda e: (e.week, e.time)):
        key = get_team_event_key(team_event.team, team_event.event)
        event_team_events[team_event.event].append(team_event)
        team_team_events[team_event.team].append(team_event)

        # Default if no matches played
        upcoming_epas = [(team_epas[team_event.team], False)]
        epas = [obj[0] for obj in team_events_dict.get(key, upcoming_epas)]
        qual_epas = [
            obj[0] for obj in team_events_dict.get(key, upcoming_epas) if not obj[1]
        ]

        team_event.epa_start = round(epas[0], 2)
        team_event.epa_end = round(epas[-1], 2)
        team_event.epa_max = round(max(epas), 2)
        team_event.epa_mean = round(sum(epas) / len(epas), 2)
        team_event.epa_diff = round(epas[-1] - epas[0], 2)
        epa_pre_elim = epas[0] if len(qual_epas) == 0 else qual_epas[-1]
        team_event.epa_pre_elim = round(epa_pre_elim, 2)

        if USE_COMPONENTS:
            # Default if no matches played
            upcoming_component_epas = [
                (
                    team_rp_1_epas[team_event.team],
                    team_rp_2_epas[team_event.team],
                    False,
                )
            ]

            qual_component_epas = [
                obj[:2]
                for obj in component_team_events_dict.get(key, upcoming_component_epas)
                if not obj[-1]
            ]

            rp_1_qual_epas = [obj[0] for obj in qual_component_epas]
            rp_2_qual_epas = [obj[1] for obj in qual_component_epas]

            if len(rp_1_qual_epas) > 0:
                team_event.rp_1_epa_start = round(rp_1_qual_epas[0], 4)
                team_event.rp_1_epa_end = round(rp_1_qual_epas[-1], 4)
                team_event.rp_1_epa_max = round(max(rp_1_qual_epas), 4)
                team_event.rp_1_epa_mean = round(
                    sum(rp_1_qual_epas) / len(rp_1_qual_epas), 4
                )

            if len(rp_2_qual_epas) > 0:
                team_event.rp_2_epa_start = round(rp_2_qual_epas[0], 4)
                team_event.rp_2_epa_end = round(rp_2_qual_epas[-1], 4)
                team_event.rp_2_epa_max = round(max(rp_2_qual_epas), 4)
                team_event.rp_2_epa_mean = round(
                    sum(rp_2_qual_epas) / len(rp_2_qual_epas), 4
                )

    # EVENTS
    for event in events:
        event_key = event.key

        event_epas: List[float] = []
        for team_event in event_team_events[event_key]:
            event_epas.append(team_event.epa_pre_elim or 0)
        event_epas.sort(reverse=True)

        if len(event_epas) > 0 and max(event_epas) > 0:
            event.epa_max = round(event_epas[0], 2)
            event.epa_top8 = None if len(event_epas) < 8 else round(event_epas[7], 2)
            event.epa_top24 = None if len(event_epas) < 24 else round(event_epas[23], 2)
            event.epa_mean = round(sum(event_epas) / len(event_epas), 2)

            if len(event_epas) > 1:
                event.epa_sd = round(stdev(event_epas), 2)

        if event.status == "Upcoming":
            continue

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
    year_epas_dict: Dict[str, float] = {}  # for norm epa
    country_year_epas: Dict[str, List[float]] = defaultdict(list)  # for rank/percentile
    state_year_epas: Dict[str, List[float]] = defaultdict(list)
    district_year_epas: Dict[str, List[float]] = defaultdict(list)
    to_remove: List[str] = []
    for team in team_years_dict:
        curr_team_epas = team_matches_dict[team]
        if curr_team_epas == []:
            if year.year == CURR_YEAR:
                curr_team_epas = [team_epas[team]]
            else:
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
        percentile = exponnorm_value  # type: ignore
        if i < cutoff_N:
            expon_value: float = expon_distrib.cdf(epa)  # type: ignore
            expon_value = 1 - cutoff_N / total_N * (1 - expon_value)  # type: ignore
            # Linearly interpolate between the two distributions from 10% to 5%
            expon_frac = min(1, 2 * (cutoff_N - i) / cutoff_N)
            percentile = expon_frac * expon_value + (1 - expon_frac) * exponnorm_value  # type: ignore
        out: float = distrib.ppf(percentile)  # type: ignore
        return NORM_MEAN + NORM_SD * out  # type: ignore

    team_year_count = len(team_years_dict)
    for team in team_years_dict:
        obj = team_years_dict[team]
        curr_team_epas = team_matches_dict[team]
        if curr_team_epas == []:
            curr_team_epas = [team_epas[team]]

        curr_component_team_epas = component_team_matches_dict[team]
        if curr_component_team_epas == []:
            curr_component_team_epas = [
                [
                    team_rp_1_epas[team],
                    team_rp_2_epas[team],
                ]
            ]

        n = len(curr_team_epas)
        obj.epa_max = round(max(curr_team_epas[min(n - 1, 8) :]), 2)
        obj.epa_mean = round(sum(curr_team_epas) / n, 2)
        obj.epa_end = round(team_epas[team], 2)
        obj.epa_diff = round(obj.epa_end - (obj.epa_start or 0), 2)

        unitless_epa: float = epa_to_unitless_epa(obj.epa_end, TOTAL_MEAN, TOTAL_SD)
        obj.unitless_epa_end = round(unitless_epa, 0)
        epa_index = year_epas.index(obj.epa_end)
        obj.norm_epa_end = round(get_norm_epa(obj.epa_end, epa_index), 0)

        pre_champs = obj.epa_start or 0
        rp_1_pre_champs = obj.rp_1_epa_start or 0
        rp_2_pre_champs = obj.rp_2_epa_start or 0
        for team_event in sorted(team_team_events[team], key=lambda t: t.sort()):
            if event_types[team_event.event] < 3:
                pre_champs = team_event.epa_end
                rp_1_pre_champs = team_event.rp_1_epa_end or 0
                rp_2_pre_champs = team_event.rp_2_epa_end or 0
        obj.epa_pre_champs = round(pre_champs, 2)
        if USE_COMPONENTS:
            obj.rp_1_epa_pre_champs = round(rp_1_pre_champs, 4)
            obj.rp_2_epa_pre_champs = round(rp_2_pre_champs, 4)

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
        year.epa_1p = round(year_epas[round(0.01 * len(year_epas))], 2)
        year.epa_10p = round(year_epas[round(0.1 * len(year_epas))], 2)
        year.epa_25p = round(year_epas[round(0.25 * len(year_epas))], 2)
        year.epa_75p = round(year_epas[round(0.75 * len(year_epas))], 2)

        year.epa_acc = acc
        year.epa_mse = mse
        year.count = count
        year.epa_elim_acc = elim_acc
        year.epa_elim_mse = elim_mse
        year.elim_count = elim_count
        year.epa_qual_acc = qual_acc
        year.epa_qual_mse = qual_mse
        year.qual_count = qual_count
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

    out_team_years_dict = {ty.pk(): ty for ty in team_years}
    out_events_dict = {e.pk(): e for e in events}
    out_team_events_dict = {te.pk(): te for te in team_events}
    out_matches_dict = {m.pk(): m for m in matches}
    out_alliances_dict = {a.pk(): a for a in alliances}
    out_team_matches_dict = {tm.pk(): tm for tm in team_matches}
    out_etags_dict = {e.pk(): e for e in etags}

    return (
        year,
        out_team_years_dict,
        out_events_dict,
        out_team_events_dict,
        out_matches_dict,
        out_alliances_dict,
        out_team_matches_dict,
        out_etags_dict,
    )


def post_process(
    teams: List[Team], all_team_years: Dict[int, Dict[str, TeamYear]]
) -> List[Team]:
    team_team_years: Dict[str, List[TeamYear]] = defaultdict(list)
    for team_years in all_team_years.values():
        for team_year in team_years.values():
            team_team_years[team_year.team].append(team_year)

    for team in teams:
        years: Dict[int, float] = {}

        for team_year in team_team_years[team.team]:
            if team_year.norm_epa_end is not None:
                years[team_year.year] = team_year.norm_epa_end

        keys, values = years.keys(), years.values()

        # get recent epas (last four years)
        recent: List[float] = []
        for year in range(CURR_YEAR - 4, CURR_YEAR + 1):
            if year in keys:
                recent.append(years[year])
        r_y, y = len(recent), len(keys)

        team.norm_epa = None if y == 0 else round(years[max(keys)])
        team.norm_epa_recent = None if r_y == 0 else round(sum(recent) / r_y)
        team.norm_epa_mean = None if y == 0 else round(sum(values) / y)
        team.norm_epa_max = None if y == 0 else round(max(values))

    return teams
