from collections import defaultdict
from statistics import stdev
from typing import Dict, List, Tuple, Union

from src.db.models.event import Event
from src.db.models.match import Match
from src.db.models.team_event import TeamEvent
from src.db.models.team_match import TeamMatch
from src.db.models.team_year import TeamYear
from src.db.models.year import Year
from src.utils import get_team_event_key, get_team_match_key


# TODO: run simulation on previous years to determine if any others are 0 or 1
# TODO: run simulation to determine if margin_func should reach 1 or ~0.8
def margin_func(year: int, x: int) -> float:
    if year in [2015]:
        return 0
    if year in [2018]:
        return 1
    return min(1, max(0, 1 / 24 * (x - 12)))


def percent_func(x: int) -> float:
    return min(0.5, max(0.3, 0.5 - 0.2 / 6 * (x - 6)))


def sum_func(arr: List[float], mean: float) -> float:
    return min(sum(arr), 2 * mean + 0.8 * (sum(arr) - 2 * mean))


# TODO: Handle RPs somehow
def process_year(
    year_num: int,
    team_years_all: Dict[int, Dict[int, TeamYear]],
    year: Year,
    team_years: List[TeamYear],
    events: List[Event],
    team_events: List[TeamEvent],
    matches: List[Match],
    team_matches: List[TeamMatch],
    year_mean_epas: Dict[int, float],
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

    # no_fouls_mean after 2016, score_mean before 2016
    TOTAL_MEAN = year.no_fouls_mean or year.score_mean or 0
    TOTAL_SD = year.score_sd or 0
    INIT_EPA = TOTAL_MEAN / NUM_TEAMS - 0.2 * TOTAL_SD

    # AUTO_MEAN = year.auto_mean or 0
    # TELEOP_MEAN = year.teleop_mean or 0
    # ENDGAME_MEAN = year.endgame_mean or 0

    team_counts: Dict[int, int] = defaultdict(int)  # for updating epa
    team_epas: Dict[int, float] = defaultdict(lambda: INIT_EPA)  # most recent epa

    team_years_dict: Dict[int, TeamYear] = {}
    team_events_dict: Dict[str, List[Tuple[float, bool]]] = {}
    team_matches_dict: Dict[int, List[float]] = {}
    team_match_ids: Dict[str, float] = {}

    # INITIALIZE
    for team_year in team_years:
        num = team_year.team
        team_years_dict[num] = team_year
        team_matches_dict[num] = []

        epa_1yr, epa_2yr = None, None
        if year_num in [2022, 2023]:
            # For 2022 and 2023, use past two years team competed (up to 4 years)
            past_epas: List[float] = []
            for past_year in range(year_num - 1, year_num - 5, -1):
                past_team_year = team_years_all.get(past_year, {}).get(num, None)
                if past_team_year is not None and past_team_year.epa_max is not None:
                    norm_epa = (
                        INIT_EPA * past_team_year.epa_max / year_mean_epas[past_year]
                    )
                    past_epas.append(norm_epa)
            epa_1yr = past_epas[0] if len(past_epas) > 0 else None
            epa_2yr = past_epas[1] if len(past_epas) > 1 else None
        else:
            # Otherwise use the two most recent years (regardless of team activity)
            team_year_1 = team_years_all.get(year_num - 1, {}).get(num, None)
            if team_year_1 is not None and team_year_1.epa_max is not None:
                epa_1yr = INIT_EPA * team_year_1.epa_max / year_mean_epas[year_num - 1]
            team_year_2 = team_years_all.get(year_num - 2, {}).get(num, None)
            if team_year_2 is not None and team_year_2.epa_max is not None:
                epa_2yr = INIT_EPA * team_year_2.epa_max / year_mean_epas[year_num - 2]

        epa_1yr = epa_1yr or INIT_EPA
        epa_2yr = epa_2yr or INIT_EPA
        epa_prior = 0.7 * epa_1yr + 0.3 * epa_2yr
        epa_prior = 0.8 * epa_prior + 0.2 * INIT_EPA
        team_epas[num] = INIT_EPA if year_num == 2002 else epa_prior
        team_year.epa_start = round(team_epas[num], 2)

        if USE_COMPONENTS:
            # TODO: add components calculations
            pass

    # win, loss, tie, count
    team_year_stats: Dict[int, List[int]] = defaultdict(lambda: [0, 0, 0, 0])
    team_event_stats: Dict[str, List[int]] = defaultdict(lambda: [0, 0, 0, 0])

    acc, mse, count = 0, 0, 0
    quals_acc, quals_mse, quals_count = 0, 0, 0
    elims_acc, elims_mse, elims_count = 0, 0, 0
    season_quals_acc, season_quals_mse, season_quals_count = 0, 0, 0
    season_elims_acc, season_elims_mse, season_elims_count = 0, 0, 0
    champs_quals_acc, champs_quals_mse, champs_quals_count = 0, 0, 0
    champs_elims_acc, champs_elims_mse, champs_elims_count = 0, 0, 0
    event_stats: Dict[str, List[Union[float, int]]] = defaultdict(lambda: [0, 0, 0])
    quals_event_stats: Dict[str, List[Union[float, int]]] = defaultdict(
        lambda: [0, 0, 0]
    )
    elims_event_stats: Dict[str, List[Union[float, int]]] = defaultdict(
        lambda: [0, 0, 0]
    )

    event_weeks = {e.key: e.week for e in events}
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
        red_epa_sum = sum_func(list(red_epa_pre.values()), TOTAL_MEAN)
        match.red_epa_sum = round(red_epa_sum, 2)
        blue_epa_sum = sum_func(list(blue_epa_pre.values()), TOTAL_MEAN)
        match.blue_epa_sum = round(blue_epa_sum, 2)
        norm_diff = (match.red_epa_sum - match.blue_epa_sum) / TOTAL_SD
        win_prob = 1 / (1 + 10 ** (-5 / 8 * norm_diff))
        match.epa_win_prob = round(win_prob, 4)
        match.epa_winner = "red" if win_prob >= 0.5 else "blue"

        for t in red:
            team_event_key = get_team_event_key(t, event_key)
            if team_event_key not in team_events_dict:
                team_events_dict[team_event_key] = [(red_epa_pre[t], match.playoff)]

        for t in blue:
            team_event_key = get_team_event_key(t, event_key)
            if team_event_key not in team_events_dict:
                team_events_dict[team_event_key] = [(blue_epa_pre[t], match.playoff)]

        winner = match.winner or "red"  # in practice, never None
        red_mapping = {"red": 0, "blue": 1, "draw": 2}
        blue_mapping = {"blue": 0, "red": 1, "draw": 2}

        # UPDATE EPA
        weight = 1 / 3 if match.playoff else 1
        red_score = match.red_no_fouls or match.red_score or 0
        red_pred = match.red_epa_sum
        blue_score = match.blue_no_fouls or match.blue_score or 0
        blue_pred = match.blue_epa_sum
        for t in red:
            team_count = team_counts[t]
            percent = percent_func(team_count)
            margin = margin_func(year_num, team_count)
            error = ((red_score - red_pred) + margin * (blue_pred - blue_score)) / (
                1 + margin
            )
            new_epa = max(0, red_epa_pre[t] + weight * percent * error / NUM_TEAMS)

            team_epas[t] = new_epa
            team_matches_dict[t].append(new_epa)
            team_event_key = get_team_event_key(t, event_key)
            team_events_dict[team_event_key].append((new_epa, match.playoff))
            team_year_stats[t][red_mapping[winner]] += 1
            team_year_stats[t][3] += 1
            team_event_stats[team_event_key][red_mapping[winner]] += 1
            team_event_stats[team_event_key][3] += 1

            if not match.playoff:
                team_counts[t] += 1

        for t in blue:
            team_count = team_counts[t]
            percent = percent_func(team_count)
            margin = margin_func(year_num, team_count)
            error = ((blue_score - blue_pred) + margin * (red_pred - red_score)) / (
                1 + margin
            )
            new_epa = max(0, blue_epa_pre[t] + weight * percent * error / NUM_TEAMS)

            team_epas[t] = new_epa
            team_matches_dict[t].append(new_epa)
            team_event_key = get_team_event_key(t, event_key)
            team_events_dict[team_event_key].append((new_epa, match.playoff))
            team_year_stats[t][blue_mapping[winner]] += 1
            team_year_stats[t][3] += 1
            team_event_stats[team_event_key][blue_mapping[winner]] += 1
            team_event_stats[team_event_key][3] += 1

            if not match.playoff:
                team_counts[t] += 1

        win_probs = {"red": 1, "blue": 0, "draw": 0.5}
        new_acc = 1 if winner == match.epa_winner else 0
        new_mse = (win_probs[winner] - match.epa_win_prob) ** 2
        event_stats[event_key][0] += new_acc  # acc
        event_stats[event_key][1] += new_mse  # mse
        event_stats[event_key][2] += 1  # count
        acc += new_acc
        mse += new_mse
        count += 1
        if match.playoff:
            elims_event_stats[event_key][0] += new_acc
            elims_event_stats[event_key][1] += new_mse
            elims_event_stats[event_key][2] += 1
            elims_mse += new_mse
            elims_acc += new_acc
            elims_count += 1
        else:
            quals_event_stats[event_key][0] += new_acc
            quals_event_stats[event_key][1] += new_mse
            quals_event_stats[event_key][2] += 1
            quals_mse += new_mse
            quals_acc += new_acc
            quals_count += 1
        if event_weeks[match.event] < 8:
            if match.playoff:
                season_elims_mse += new_mse
                season_elims_acc += new_acc
                season_elims_count += 1
            else:
                season_quals_mse += new_mse
                season_quals_acc += new_acc
                season_quals_count += 1
        else:
            if match.playoff:
                champs_elims_mse += new_mse
                champs_elims_acc += new_acc
                champs_elims_count += 1
            else:
                champs_quals_mse += new_mse
                champs_quals_acc += new_acc
                champs_quals_count += 1

    acc = None if count == 0 else round(acc / count, 4)
    mse = None if count == 0 else round(mse / count, 4)
    elims_acc = None if elims_count == 0 else round(elims_acc / elims_count, 4)
    elims_mse = None if elims_count == 0 else round(elims_mse / elims_count, 4)
    quals_acc = None if quals_count == 0 else round(quals_acc / quals_count, 4)
    quals_mse = None if quals_count == 0 else round(quals_mse / quals_count, 4)
    season_elims_acc = (
        None
        if season_elims_count == 0
        else round(season_elims_acc / season_elims_count, 4)
    )
    season_elims_mse = (
        None
        if season_elims_count == 0
        else round(season_elims_mse / season_elims_count, 4)
    )
    season_quals_acc = (
        None
        if season_quals_count == 0
        else round(season_quals_acc / season_quals_count, 4)
    )
    season_quals_mse = (
        None
        if season_quals_count == 0
        else round(season_quals_mse / season_quals_count, 4)
    )
    champs_elims_acc = (
        None
        if champs_elims_count == 0
        else round(champs_elims_acc / champs_elims_count, 4)
    )
    champs_elims_mse = (
        None
        if champs_elims_count == 0
        else round(champs_elims_mse / champs_elims_count, 4)
    )
    champs_quals_acc = (
        None
        if champs_quals_count == 0
        else round(champs_quals_acc / champs_quals_count, 4)
    )
    champs_quals_mse = (
        None
        if champs_quals_count == 0
        else round(champs_quals_mse / champs_quals_count, 4)
    )

    # TEAM MATCHES
    completed_team_matches = [m for m in team_matches if m.status == "Completed"]
    for team_match in completed_team_matches:
        match_key = get_team_match_key(team_match.team, team_match.match)
        team_match.epa = round(team_match_ids[match_key], 2)

    # TEAM EVENTS
    event_team_events: Dict[str, List[TeamEvent]] = defaultdict(list)
    team_team_events: Dict[int, List[TeamEvent]] = defaultdict(list)
    for team_event in sorted(team_events, key=lambda e: (e.week, e.time)):
        key = get_team_event_key(team_event.team, team_event.event)
        event_team_events[team_event.event].append(team_event)
        team_team_events[team_event.team].append(team_event)

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
        epa_pre_playoffs = epas[0] if len(qual_epas) == 0 else qual_epas[-1]
        team_event.epa_pre_playoffs = round(epa_pre_playoffs, 2)

        wins, losses, ties, event_count = team_event_stats[key]
        winrate = round((wins + ties / 2) / max(1, event_count), 4)
        team_event.wins = wins
        team_event.losses = losses
        team_event.ties = ties
        team_event.winrate = winrate

    # EVENTS
    event_types: Dict[str, int] = defaultdict(int)
    filtered_events = [e for e in events if e.status != "Upcoming"]
    for event in filtered_events:
        event_key = event.key
        event_types[event_key] = event.type

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

        quals_event_acc, quals_event_mse, quals_event_count = quals_event_stats[
            event_key
        ]
        event.quals_epa_acc = (
            None
            if quals_event_count == 0
            else round(quals_event_acc / quals_event_count, 4)
        )
        event.quals_epa_mse = (
            None
            if quals_event_count == 0
            else round(quals_event_mse / quals_event_count, 4)
        )

        elims_event_acc, elims_event_mse, elims_event_count = elims_event_stats[
            event_key
        ]
        event.elims_epa_acc = (
            None
            if elims_event_count == 0
            else round(elims_event_acc / elims_event_count, 4)
        )
        event.elims_epa_mse = (
            None
            if elims_event_count == 0
            else round(elims_event_mse / elims_event_count, 4)
        )

    # TEAM YEARS
    year_epas: List[float] = []
    to_remove: List[int] = []
    for team in team_years_dict:
        curr_team_epas = team_matches_dict[team]
        if curr_team_epas == []:
            to_remove.append(team)
            continue

        n = len(curr_team_epas)
        epa_max = round(max(curr_team_epas[min(n - 1, 8) :]), 2)
        year_epas.append(epa_max)

    for team in to_remove:
        team_years_dict.pop(team)

    year_epas.sort(reverse=True)
    team_year_count = len(team_years_dict)
    for team in team_years_dict:
        obj = team_years_dict[team]
        curr_team_epas = team_matches_dict[team]
        n = len(curr_team_epas)
        obj.epa_max = round(max(curr_team_epas[min(n - 1, 8) :]), 2)
        obj.epa_mean = round(sum(curr_team_epas) / n, 2)
        obj.epa_end = round(team_epas[team], 2)
        obj.epa_diff = round(obj.epa_end - (obj.epa_start or 0), 2)

        pre_champs = obj.epa_start or 0
        for team_event in sorted(team_team_events[team], key=lambda t: t.sort()):
            if event_types[team_event.event] < 3 and team_event.epa_end is not None:
                pre_champs = team_event.epa_end
        obj.epa_pre_champs = round(pre_champs, 2)

        wins, losses, ties, team_count = team_year_stats[team]
        winrate = round((wins + ties / 2) / max(1, team_count), 4)
        obj.wins = wins
        obj.losses = losses
        obj.ties = ties
        obj.winrate = winrate

        obj.epa_rank = rank = year_epas.index(obj.epa_max) + 1
        obj.epa_percentile = round(1 - rank / team_year_count, 4)

    # YEARS
    if len(year_epas) > 0:
        year_epas.sort(reverse=True)
        year.epa_max = round(year_epas[0], 2)
        year.epa_1p = round(year_epas[round(0.01 * len(year_epas))], 2)
        year.epa_5p = round(year_epas[round(0.05 * len(year_epas))], 2)
        year.epa_10p = round(year_epas[round(0.1 * len(year_epas))], 2)
        year.epa_25p = round(year_epas[round(0.25 * len(year_epas))], 2)
        year.epa_median = round(year_epas[round(0.5 * len(year_epas))], 2)
        year.epa_mean = round(sum(year_epas) / len(year_epas), 2)
        year.epa_sd = round(stdev(year_epas), 2)
        year.epa_acc = acc
        year.epa_mse = mse
        year.epa_elims_acc = elims_acc
        year.epa_elims_mse = elims_mse
        year.epa_quals_acc = quals_acc
        year.epa_quals_mse = quals_mse
        year.epa_season_elims_acc = season_elims_acc
        year.epa_season_elims_mse = season_elims_mse
        year.epa_season_quals_acc = season_quals_acc
        year.epa_season_quals_mse = season_quals_mse
        year.epa_champs_elims_acc = champs_elims_acc
        year.epa_champs_elims_mse = champs_elims_mse
        year.epa_champs_quals_acc = champs_quals_acc
        year.epa_champs_quals_mse = champs_quals_mse

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
