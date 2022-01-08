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
from helper.utils import get_team_event_key, get_team_match_key
from models.elo import (
    START_RATING,
    existing_rating,
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
    team_years_dict: Dict[int, TeamYear] = {}
    team_events_dict: Dict[str, List[Tuple[float, bool]]] = {}
    team_matches_dict: Dict[int, List[float]] = {}
    team_elos: Dict[int, float] = {}  # most recent elo
    team_match_ids: Dict[str, float] = {}

    # win, loss, tie, count
    team_year_stats: Dict[int, List[int]] = defaultdict(lambda: [0, 0, 0, 0])
    team_event_stats: Dict[str, List[int]] = defaultdict(lambda: [0, 0, 0, 0])

    sd_score = year.score_sd or 0

    # INITIALIZE
    for team_year in team_years:
        num = team_year.team
        team_years_dict[num] = team_year
        team_matches_dict[num] = []

        if year_num in [2022, 2023]:
            # For 2022 and 2023, use past two years team competed (up to 2018)
            past_elos: List[float] = []
            for past_year in range(year_num - 1, 2017, -1):
                past_team_year = team_years_all.get(past_year, {}).get(num, None)
                if past_team_year is not None and past_team_year.elo_max is not None:
                    past_elos.append(past_team_year.elo_max)
            elo_1yr = past_elos[0] if len(past_elos) > 0 else None
            elo_2yr = past_elos[1] if len(past_elos) > 1 else None
        else:
            # Otherwise use the two most recent years (regardless of team activity)
            team_year_2 = team_years_all.get(year_num - 2, {}).get(num, None)
            elo_2yr = team_year_2.elo_max if team_year_2 is not None else None
            team_year_1 = team_years_all.get(year_num - 1, {}).get(num, None)
            elo_1yr = team_year_1.elo_max if team_year_1 is not None else None

        start_elo = existing_rating(elo_1yr, elo_2yr)
        team_elos[num] = START_RATING if year_num == 2002 else start_elo
        team_year.elo_start = round(team_elos[num])

    # MATCHES
    acc, mse, count = 0, 0, 0
    event_stats: Dict[str, List[Union[float, int]]] = defaultdict(lambda: [0, 0, 0])

    sorted_matches = sorted(matches, key=lambda m: m.sort())
    for match in sorted_matches:
        event_key = match.event
        red, blue = match.get_teams()
        red_elo_pre: Dict[int, float] = {}
        blue_elo_pre: Dict[int, float] = {}
        for team in red:
            red_elo_pre[team] = team_elos[team]
            team_match_ids[get_team_match_key(team, match.key)] = team_elos[team]
        for team in blue:
            blue_elo_pre[team] = team_elos[team]
            team_match_ids[get_team_match_key(team, match.key)] = team_elos[team]

        match.red_elo_sum = round(sum(red_elo_pre.values()))
        match.blue_elo_sum = round(sum(blue_elo_pre.values()))
        win_prob = elo_win_prob(match.red_elo_sum, match.blue_elo_sum)
        match.elo_win_prob = round(win_prob, 4)
        match.elo_winner = "red" if win_prob > 0.5 else "blue"

        red_elo_post, blue_elo_post = elo_update_rating(
            sd_score,
            red_elo_pre,
            blue_elo_pre,
            match.red_score or 0,
            match.blue_score or 0,
            match.playoff == 1,
        )

        winner = match.winner or "red"  # in practice, never None
        red_mapping = {"red": 0, "blue": 1, "draw": 2}
        blue_mapping = {"blue": 0, "red": 1, "draw": 2}

        for t in red:
            team_elos[t] = red_elo_post[t]
            team_matches_dict[t].append(red_elo_post[t])
            team_event_key = get_team_event_key(t, event_key)
            if team_event_key not in team_events_dict:
                team_events_dict[team_event_key] = [(red_elo_pre[t], match.playoff == 1)]
            team_events_dict[team_event_key].append(
                (red_elo_post[t], match.playoff == 1)
            )
            team_year_stats[t][3] += 1
            team_year_stats[t][red_mapping[winner]] += 1
            team_event_stats[team_event_key][3] += 1
            team_event_stats[team_event_key][red_mapping[winner]] += 1

        for t in blue:
            team_elos[t] = blue_elo_post[t]
            team_matches_dict[t].append(blue_elo_post[t])
            team_event_key = get_team_event_key(t, event_key)
            if team_event_key not in team_events_dict:
                team_events_dict[team_event_key] = [
                    (blue_elo_pre[t], match.playoff == 1)
                ]
            team_events_dict[team_event_key].append(
                (blue_elo_post[t], match.playoff == 1)
            )
            team_year_stats[t][3] += 1
            team_year_stats[t][blue_mapping[winner]] += 1
            team_event_stats[team_event_key][3] += 1
            team_event_stats[team_event_key][blue_mapping[winner]] += 1

        win_probs = {"red": 1, "blue": 0, "draw": 0.5}
        error = (win_probs[winner] - match.elo_win_prob) ** 2
        event_stats[event_key][1] += error  # mse
        mse += error

        if winner == match.elo_winner:
            event_stats[event_key][0] += 1  # acc
            acc += 1

        event_stats[event_key][2] += 1  # count
        count += 1

    acc = None if count == 0 else round(acc / count, 4)
    mse = None if count == 0 else round(mse / count, 4)

    # TEAM MATCHES
    for team_match in team_matches:
        match_key = get_team_match_key(team_match.team, team_match.match)
        team_match.elo = round(team_match_ids[match_key])

    # TEAM EVENTS
    event_team_events: Dict[str, List[TeamEvent]] = defaultdict(list)
    team_team_events: Dict[int, List[TeamEvent]] = defaultdict(list)
    for team_event in team_events:
        key = get_team_event_key(team_event.team, team_event.event)
        if key not in team_events_dict:
            continue

        if team_event.status == "Upcoming":
            continue

        event_team_events[team_event.event].append(team_event)
        team_team_events[team_event.team].append(team_event)

        elos = [obj[0] for obj in team_events_dict[key]]
        team_event.elo_start = round(elos[0])
        team_event.elo_end = round(elos[-1])
        team_event.elo_max = round(max(elos))
        team_event.elo_mean = round(sum(elos) / len(elos))
        team_event.elo_diff = round(elos[-1] - elos[0])
        qual_elos = [obj[0] for obj in team_events_dict[key] if not obj[1]]
        elo_pre_playoffs = elos[0] if len(qual_elos) == 0 else qual_elos[-1]
        team_event.elo_pre_playoffs = round(elo_pre_playoffs)

        wins, losses, ties, count = team_event_stats[key]
        winrate = round((wins + ties / 2) / max(1, count), 4)
        team_event.wins = wins
        team_event.losses = losses
        team_event.ties = ties
        team_event.count = count
        team_event.winrate = winrate

    # EVENTS
    event_types: Dict[str, int] = defaultdict(int)
    for event in events:
        if event.status == "Upcoming":
            continue

        event_key = event.key
        event_types[event_key] = event.type

        elos: List[float] = []
        for team_event in event_team_events[event_key]:
            elos.append(team_event.elo_pre_playoffs or 0)
        elos.sort(reverse=True)

        event.elo_max = round(elos[0])
        event.elo_top8 = None if len(elos) < 8 else round(elos[7])
        event.elo_top24 = None if len(elos) < 24 else round(elos[23])
        event.elo_mean = round(sum(elos) / len(elos))
        event.elo_sd = round(statistics.pstdev(elos), 2)
        event_acc, event_mse, event_count = event_stats[event_key]
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

        elo_max = round(max(elos[min(len(elos) - 1, 8) :]))
        year_elos.append(elo_max)

    for team in to_remove:
        team_years_dict.pop(team)

    year_elos.sort(reverse=True)
    team_year_count = len(team_years)
    for team in team_years_dict:
        obj = team_years_dict[team]
        elos = team_matches_dict[team]
        obj.elo_max = round(max(elos[min(len(elos) - 1, 8) :]))
        obj.elo_mean = round(sum(elos) / len(elos))
        obj.elo_end = round(team_elos[team])
        obj.elo_diff = round(obj.elo_end - (obj.elo_start or 0))

        pre_champs = obj.elo_start or 0
        for team_event in sorted(team_team_events[team], key=lambda t: t.sort()):
            if event_types[team_event.event] < 3 and team_event.elo_end is not None:
                pre_champs = team_event.elo_end
        obj.elo_pre_champs = round(pre_champs)

        wins, losses, ties, count = team_year_stats[team]
        winrate = round((wins + ties / 2) / max(1, count), 4)
        obj.wins = wins
        obj.losses = losses
        obj.ties = ties
        obj.count = count
        obj.winrate = winrate

        obj.elo_rank = rank = year_elos.index(obj.elo_max) + 1
        obj.elo_percentile = round(rank / team_year_count, 4)

    # YEARS
    if len(year_elos) > 0:
        year_elos.sort(reverse=True)
        year.elo_max = round(year_elos[0])
        year.elo_1p = round(year_elos[round(0.01 * len(year_elos))])
        year.elo_5p = round(year_elos[round(0.05 * len(year_elos))])
        year.elo_10p = round(year_elos[round(0.10 * len(year_elos))])
        year.elo_25p = round(year_elos[round(0.25 * len(year_elos))])
        year.elo_median = round(year_elos[round(0.50 * len(year_elos))])
        year.elo_mean = round(sum(year_elos) / len(year_elos))
        year.elo_sd = round(statistics.pstdev(year_elos), 2)
        year.elo_acc = acc
        year.elo_mse = mse

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


# NOTE: should be updated every year to replace hardcoded values
def post_process(end_year: int) -> None:
    team_team_years: Dict[int, List[TeamYear]] = defaultdict(list)
    all_team_years = get_team_years_db()
    for team_year in all_team_years:
        team_team_years[team_year.team].append(team_year)

    all_teams = get_teams_db()
    for team in all_teams:
        years: Dict[int, float] = {}
        wins, losses, ties, count = 0, 0, 0, 0

        team.active = 0
        for team_year in team_team_years[team.team]:
            if team_year.year == end_year:
                team.active = 1
            if team_year.elo_max is not None:
                years[team_year.year] = team_year.elo_max
            wins += team_year.wins or 0
            losses += team_year.losses or 0
            ties += team_year.ties or 0
            count += team_year.count or 0
        keys, values = years.keys(), years.values()

        # get recent elos (last five years)
        recent: List[float] = []
        for year in range(end_year - 5, end_year):
            if year in keys:
                recent.append(years[year])
        r_y, y = len(recent), len(keys)

        team.elo = None if y == 0 else round(years[max(keys)])
        # NOTE: can be removed after 2022 season (condition never met)
        # temp solution applying mean reversion if no 2020 matches
        if team.active and y > 0 and max(keys) == 2019:
            yr_1 = 1450 if 2019 not in years else years[2019]
            yr_2 = 1450 if 2018 not in years else years[2018]
            team.elo = round(0.56 * yr_1 + 0.24 * yr_2 + 0.20 * 1450)

        team.elo_recent = None if r_y == 0 else round(sum(recent) / r_y)
        team.elo_mean = None if y == 0 else round(sum(values) / y)
        team.elo_max = None if y == 0 else round(max(values))

        winrate = round((wins + ties / 2) / max(1, count), 4)
        team.wins = wins
        team.losses = losses
        team.ties = ties
        team.count = count
        team.winrate = winrate

    update_teams_db(all_teams, False)
