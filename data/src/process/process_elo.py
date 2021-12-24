import statistics
from collections import defaultdict
from typing import Dict, List, Tuple, Union

from db.models.event import Event
from db.models.match import Match
from db.models.team_event import TeamEvent
from db.models.team_match import TeamMatch
from db.models.team_year import TeamYear
from db.models.year import Year
from db.read.team import get_teams as get_teams_db
from db.read.team_year import get_team_years as get_team_years_db
from db.write.main import update_teams as update_teams_db
from helper.utils import get_team_event_id, get_team_match_id
from models.elo import (
    existing_rating,
    mean_reversion,
    start_rating,
    update_rating as elo_update_rating,
    win_prob as elo_win_prob,
)


def process_year(
    year_num: int,
    team_years_all: Dict[int, Dict[int, TeamYear]],
    year: Year,
    team_years: List[TeamYear],
    events: List[Event],
    team_events: List[TeamEvent],
    matches: List[Match],
    team_matches: List[TeamMatch],
) -> Tuple[
    Dict[int, Dict[int, TeamYear]],
    Year,
    List[TeamYear],
    List[Event],
    List[TeamEvent],
    List[Match],
    List[TeamMatch],
]:
    global_start_elo = start_rating()
    reversion = mean_reversion()

    team_years_dict: Dict[int, TeamYear] = {}
    team_events_dict: Dict[int, List[Tuple[float, bool]]] = {}
    team_matches_dict: Dict[int, List[float]] = {}
    team_elos: Dict[int, float] = {}  # most recent elo
    team_match_ids: Dict[int, float] = {}

    # win, loss, tie, count
    team_year_stats: Dict[int, List[int]] = defaultdict(lambda: [0, 0, 0, 0])
    team_event_stats: Dict[int, List[int]] = defaultdict(lambda: [0, 0, 0, 0])

    sd_score = year.score_sd

    # INITIALIZE
    for team_year in team_years:
        num = team_year.team_id
        team_years_dict[num] = team_year
        team_matches_dict[num] = []

        team_year_2 = team_years_all.get(year_num - 2, {}).get(num, None)
        elo_2yr = team_year_2.elo_max if team_year_2 is not None else reversion

        team_year_1 = team_years_all.get(year_num - 1, {}).get(num, None)
        elo_1yr = team_year_1.elo_max if team_year_1 is not None else reversion

        start_elo = existing_rating(elo_1yr, elo_2yr)
        team_elos[num] = global_start_elo if year_num == 2002 else start_elo
        team_year.elo_start = team_elos[num]

    # MATCHES
    acc, mse, count = 0, 0, 0
    event_stats: Dict[int, List[Union[float, int]]] = defaultdict(lambda: [0, 0, 0])

    for match in sorted(matches):
        event_id = match.event_id
        red, blue = match.get_teams()
        red_elo_pre: Dict[int, float] = {}
        blue_elo_pre: Dict[int, float] = {}
        for team in red:
            red_elo_pre[team] = team_elos[team]
            team_match_ids[get_team_match_id(team, match.id)] = team_elos[team]
        for team in blue:
            blue_elo_pre[team] = team_elos[team]
            team_match_ids[get_team_match_id(team, match.id)] = team_elos[team]

        match.red_elo_sum = sum(red_elo_pre.values())
        match.blue_elo_sum = sum(blue_elo_pre.values())
        win_prob = elo_win_prob(match.red_elo_sum, match.blue_elo_sum)
        match.elo_win_prob = win_prob
        match.elo_winner = "red" if win_prob > 0.5 else "blue"

        red_elo_post, blue_elo_post = elo_update_rating(
            sd_score,
            red_elo_pre,
            blue_elo_pre,
            match.red_score,
            match.blue_score,
            match.playoff == 1,
        )

        winner = match.winner or "red"  # in practice, never None
        red_mapping = {"red": 0, "blue": 1, "draw": 2}
        blue_mapping = {"blue": 0, "red": 1, "draw": 2}

        for t in red:
            team_elos[t] = red_elo_post[t]
            team_matches_dict[t].append(red_elo_post[t])
            team_event_id = get_team_event_id(t, event_id)
            if team_event_id not in team_events_dict:
                team_events_dict[team_event_id] = [(red_elo_pre[t], match.playoff == 1)]
            team_events_dict[team_event_id].append(
                (red_elo_post[t], match.playoff == 1)
            )
            team_year_stats[t][3] += 1
            team_year_stats[t][red_mapping[winner]] += 1
            team_event_stats[team_event_id][3] += 1
            team_event_stats[t][red_mapping[winner]] += 1

        for t in blue:
            team_elos[t] = blue_elo_post[t]
            team_matches_dict[t].append(blue_elo_post[t])
            team_event_id = get_team_event_id(t, event_id)
            if team_event_id not in team_events_dict:
                team_events_dict[team_event_id] = [
                    (blue_elo_pre[t], match.playoff == 1)
                ]
            team_events_dict[team_event_id].append(
                (blue_elo_post[t], match.playoff == 1)
            )
            team_year_stats[t][3] += 1
            team_year_stats[t][blue_mapping[winner]] += 1
            team_event_stats[team_event_id][3] += 1
            team_event_stats[t][blue_mapping[winner]] += 1

        win_probs = {"red": 1, "blue": 0, "draw": 0.5}
        error = (win_probs[winner] - match.elo_win_prob) ** 2
        event_stats[event_id][1] += error  # mse
        mse += error

        if winner == match.elo_winner:
            event_stats[event_id][0] += 1  # acc
            acc += 1

        event_stats[event_id][2] += 1  # count
        count += 1

    acc = round(acc / count, 4)
    mse = round(mse / count, 4)

    # TEAM MATCHES
    for team_match in team_matches:
        team_match.elo = team_match_ids[team_match.id]
    del team_match_ids

    # TEAM EVENTS
    event_team_events: Dict[int, List[TeamEvent]] = defaultdict(list)
    team_team_events: Dict[int, List[TeamEvent]] = defaultdict(list)
    for team_event in team_events:
        id = team_event.id
        if id not in team_events_dict:
            continue

        event_team_events[team_event.event_id].append(team_event)
        team_team_events[team_event.team_id].append(team_event)

        elos = [obj[0] for obj in team_events_dict[id]]
        team_event.elo_start = elos[0]
        team_event.elo_end = elos[-1]
        team_event.elo_max = max(elos)
        team_event.elo_mean = sum(elos) / len(elos)
        team_event.elo_diff = elos[-1] - elos[0]
        qual_elos = [obj[0] for obj in team_events_dict[id] if not obj[1]]
        team_event.elo_pre_playoffs = elos[0] if len(qual_elos) == 0 else qual_elos[-1]

        wins, losses, ties, count = team_event_stats[id]
        winrate = round((wins + ties / 2) / max(1, count), 4)
        team_event.wins = wins
        team_event.losses = losses
        team_event.ties = ties
        team_event.count = count
        team_event.winrate = winrate

    del team_events_dict
    del team_event_stats

    # EVENTS
    event_types: Dict[int, int] = defaultdict(int)
    for event in events:
        event_id = event.id
        event_types[event_id] = event.type

        elos: List[float] = []
        for team_event in event_team_events[event_id]:
            elos.append(team_event.elo_pre_playoffs)
        elos.sort(reverse=True)

        event.elo_max = elos[0]
        event.elo_top8 = -1 if len(elos) < 8 else elos[7]
        event.elo_top24 = -1 if len(elos) < 24 else elos[23]
        event.elo_mean = round(sum(elos) / len(elos), 2)
        event.elo_sd = round(statistics.pstdev(elos), 2)
        event_acc, event_mse, event_count = event_stats[event_id]
        event.elo_acc = round(event_acc / event_count, 4)
        event.elo_mse = round(event_mse / event_count, 4)

    # TEAM YEARS
    year_elos: List[float] = []
    to_remove: List[int] = []
    for team in team_years_dict:
        elos = team_matches_dict[team]
        if elos == []:
            to_remove.append(team)
            continue

        elo_max = max(elos[min(len(elos) - 1, 8) :])
        year_elos.append(elo_max)

    for team in to_remove:
        team_years_dict.pop(team)

    year_elos.sort(reverse=True)
    team_year_count = len(team_years)
    for team in team_years_dict:
        obj = team_years_dict[team]
        elos = team_matches_dict[team]
        obj.elo_max = max(elos[min(len(elos) - 1, 8) :])
        obj.elo_mean = round(sum(elos) / len(elos), 2)
        obj.elo_end = team_elos[team]
        obj.elo_diff = obj.elo_end - obj.elo_start

        pre_champs = obj.elo_start
        for team_event in sorted(team_team_events[team]):
            if event_types[team_event.event_id] < 3:
                pre_champs = team_event.elo_end
        obj.elo_pre_champs = pre_champs

        wins, losses, ties, count = team_year_stats[team]
        winrate = round((wins + ties / 2) / max(1, count), 4)
        obj.wins = wins
        obj.losses = losses
        obj.ties = ties
        obj.count = count
        obj.winrate = winrate

        obj.elo_rank = rank = year_elos.index(obj.elo_max) + 1
        obj.elo_percentile = round(rank / team_year_count, 4)

    del team_matches_dict
    del team_elos
    del team_year_stats

    # YEARS
    year_elos.sort(reverse=True)
    year.elo_max = year_elos[0]
    year.elo_1p = year_elos[round(0.01 * len(year_elos))]
    year.elo_5p = year_elos[round(0.05 * len(year_elos))]
    year.elo_10p = year_elos[round(0.10 * len(year_elos))]
    year.elo_25p = year_elos[round(0.25 * len(year_elos))]
    year.elo_median = year_elos[round(0.50 * len(year_elos))]
    year.elo_mean = round(sum(year_elos) / len(year_elos), 2)
    year.elo_sd = round(statistics.pstdev(year_elos), 2)
    year.elo_acc = acc
    year.elo_mse = mse

    team_years_all[year_num] = team_years_dict
    del team_years_dict

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
        team_team_years[team_year.team_id].append(team_year)

    all_teams = get_teams_db()
    for team in all_teams:
        years: Dict[int, float] = {}
        wins, losses, ties, count = 0, 0, 0, 0
        for team_year in team_team_years[team.id]:
            years[team_year.year_id] = team_year.elo_max
            wins += team_year.wins
            losses += team_year.losses
            ties += team_year.ties
            count += team_year.count
        keys = years.keys()
        values = years.values()
        recent: List[float] = []
        for year in range(2017, end_year + 1):
            if year in years:
                recent.append(years[year])
        r_y, y = len(recent), len(keys)
        team.elo = -1 if not team.active or y == 0 else years[max(keys)]

        # temp solution applying mean reversion if no 2020 matches
        if team.active and y > 0 and max(keys) == 2019:
            yr_1 = 1450 if 2019 not in years else years[2019]
            yr_2 = 1450 if 2018 not in years else years[2018]
            team.elo = 0.56 * yr_1 + 0.24 * yr_2 + 0.20 * 1450

        team.elo_recent = -1 if r_y == 0 else round(sum(recent) / r_y, 2)
        team.elo_mean = -1 if y == 0 else round(sum(values) / y, 2)
        team.elo_max = -1 if y == 0 else max(values)

        winrate = round((wins + ties / 2) / max(1, count), 4)
        team.wins = wins
        team.losses = losses
        team.ties = ties
        team.count = count
        team.winrate = winrate

    update_teams_db(all_teams, False)
