import statistics
from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Tuple, Union

from db.models.team_event import TeamEvent
from db.models.team_year import TeamYear
from db.read.event import get_events as get_events_db
from db.read.match import get_matches as get_matches_db
from db.read.team import get_teams as get_teams_db
from db.read.team_event import get_team_events as get_team_events_db

from db.read.team_match import get_team_matches as get_team_matches_db
from db.read.team_year import get_team_years as get_team_years_db
from db.read.year import get_years as get_years_db
from db.write.main import (
    update_team_matches as update_team_matches_db,
    update_events as update_events_db,
    update_matches as update_matches_db,
    update_team_events as update_team_events_db,
    update_team_years as update_team_years_db,
    update_teams as update_teams_db,
    update_years as update_years_db,
)
from helper.utils import get_team_event_id
from models.elo import (
    existing_rating,
    mean_reversion,
    start_rating,
    update_rating as elo_update_rating,
    win_prob as elo_win_prob,
)


def process(start_year: int, end_year: int) -> None:
    teams = {}  # dict mapping team number to team obj
    for team in get_teams_db():
        teams[team.id] = team

    # constants from elo model
    global_start_elo = start_rating()
    reversion = mean_reversion()

    team_years_all: Dict[int, Dict[int, TeamYear]] = {}  # master dictionary

    if start_year > 2003:
        team_years_2 = {}
        for team_year in get_team_years_db(start_year - 2):
            team_years_2[team_year.team_id] = team_year
        team_years_all[start_year - 2] = team_years_2

    if start_year > 2002:
        team_years_1 = {}
        for team_year in get_team_years_db(start_year - 1):
            team_years_1[team_year.team_id] = team_year
        team_years_all[start_year - 1] = team_years_1

    for year in range(start_year, end_year + 1):
        start = datetime.now()

        team_years: Dict[int, TeamYear] = {}
        team_events: Dict[int, List[Tuple[float, bool]]] = {}
        team_matches: Dict[int, List[float]] = {}
        team_elos: Dict[int, float] = {}  # most recent elo
        team_match_ids: Dict[int, Dict[int, float]] = {}

        # win, loss, tie, count
        team_year_stats: Dict[int, List[int]] = defaultdict(lambda: [0, 0, 0, 0])
        team_event_stats: Dict[int, List[int]] = defaultdict(lambda: [0, 0, 0, 0])

        sd_score = get_years_db(year)[0].score_sd

        team_years_list = get_team_years_db(year)

        # INITIALIZE
        for team_year in team_years_list:
            num = team_year.team_id
            team_years[num] = team_year
            team_matches[num] = []

            elo_2yr = reversion
            if (
                year - 2 in team_years_all
                and num in team_years_all[year - 2]
                and team_years_all[year - 2][num].elo_max is not None
            ):
                elo_2yr = team_years_all[year - 2][num].elo_max

            elo_1yr = reversion
            if (
                year - 1 in team_years_all
                and num in team_years_all[year - 1]
                and team_years_all[year - 1][num].elo_max is not None
            ):
                elo_1yr = team_years_all[year - 1][num].elo_max

            start_elo = existing_rating(elo_1yr, elo_2yr)
            team_elos[num] = global_start_elo if year == 2002 else start_elo
            team_year.elo_start = team_elos[num]

        # MATCHES
        acc, mse, count = 0, 0, 0
        event_stats: Dict[int, List[Union[float, int]]] = defaultdict(lambda: [0, 0, 0])
        matches = get_matches_db(year)
        for match in sorted(matches):
            event_id = match.event_id
            red, blue = match.get_teams()
            red_elo_pre: Dict[int, float] = {}
            blue_elo_pre: Dict[int, float] = {}
            team_match_ids[match.id] = {}
            for team in red:
                red_elo_pre[team] = team_elos[team]
                team_match_ids[match.id][team] = team_elos[team]
            for team in blue:
                blue_elo_pre[team] = team_elos[team]
                team_match_ids[match.id][team] = team_elos[team]

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
                team_matches[t].append(red_elo_post[t])
                team_event_id = get_team_event_id(t, event_id)
                if team_event_id not in team_events:
                    team_events[team_event_id] = [(red_elo_pre[t], match.playoff == 1)]
                team_events[team_event_id].append((red_elo_post[t], match.playoff == 1))
                team_year_stats[t][3] += 1
                team_year_stats[t][red_mapping[winner]] += 1
                team_event_stats[team_event_id][3] += 1
                team_event_stats[t][red_mapping[winner]] += 1

            for t in blue:
                team_elos[t] = blue_elo_post[t]
                team_matches[t].append(blue_elo_post[t])
                team_event_id = get_team_event_id(t, event_id)
                if team_event_id not in team_events:
                    team_events[team_event_id] = [(blue_elo_pre[t], match.playoff == 1)]
                team_events[team_event_id].append(
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

        update_matches_db(matches, False)

        acc = round(acc / len(matches), 4)
        mse = round(mse / len(matches), 4)

        # TEAM MATCHES
        all_team_matches = get_team_matches_db(year=year)
        for team_match in all_team_matches:
            team_match.elo = team_match_ids[team_match.match_id][team_match.team_id]
        update_team_matches_db(all_team_matches, False)

        # TEAM EVENTS
        event_team_events: Dict[int, List[TeamEvent]] = defaultdict(list)
        team_team_events: Dict[int, List[TeamEvent]] = defaultdict(list)
        all_team_events = get_team_events_db(year=year)
        for team_event in all_team_events:
            id = team_event.id
            if id not in team_events:
                continue

            event_team_events[team_event.event_id].append(team_event)
            team_team_events[team_event.team_id].append(team_event)

            elos = [obj[0] for obj in team_events[id]]
            team_event.elo_start = elos[0]
            team_event.elo_end = elos[-1]
            team_event.elo_max = max(elos)
            team_event.elo_mean = sum(elos) / len(elos)
            team_event.elo_diff = elos[-1] - elos[0]
            qual_elos = [obj[0] for obj in team_events[id] if not obj[1]]
            team_event.elo_pre_playoffs = (
                elos[0] if len(qual_elos) == 0 else qual_elos[-1]
            )

            wins, losses, ties, count = team_event_stats[id]
            winrate = round((wins + ties / 2) / max(1, count), 4)
            team_event.wins = wins
            team_event.losses = losses
            team_event.ties = ties
            team_event.count = count
            team_event.winrate = winrate

        update_team_events_db(all_team_events, False)

        # EVENTS
        event_types: Dict[int, int] = defaultdict(int)
        all_events = get_events_db(year=year)
        for event in all_events:
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

        update_events_db(all_events, False)

        # TEAM YEARS
        year_elos: List[float] = []
        to_remove: List[int] = []
        for team in team_years:
            elos = team_matches[team]
            if elos == []:
                to_remove.append(team)
                continue

            elo_max = max(elos[min(len(elos) - 1, 8) :])
            year_elos.append(elo_max)

        for team in to_remove:
            team_years.pop(team)

        year_elos.sort(reverse=True)
        team_year_count = len(team_years)
        for team in team_years:
            obj = team_years[team]
            elos = team_matches[team]
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

        update_team_years_db(team_years_list, False)

        # YEARS
        year_elos.sort(reverse=True)
        year_obj = get_years_db(year)[0]
        year_obj.elo_max = year_elos[0]
        year_obj.elo_1p = year_elos[round(0.01 * len(year_elos))]
        year_obj.elo_5p = year_elos[round(0.05 * len(year_elos))]
        year_obj.elo_10p = year_elos[round(0.10 * len(year_elos))]
        year_obj.elo_25p = year_elos[round(0.25 * len(year_elos))]
        year_obj.elo_median = year_elos[round(0.50 * len(year_elos))]
        year_obj.elo_mean = round(sum(year_elos) / len(year_elos), 2)
        year_obj.elo_sd = round(statistics.pstdev(year_elos), 2)
        year_obj.elo_acc = acc
        year_obj.elo_mse = mse

        team_years_all[year] = team_years
        if year - 2 in team_years_all:
            team_years_all.pop(year - 2)

        update_years_db([year_obj], False)

        end = datetime.now()
        print(str(year) + ":", end - start)

    # TEAMS
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
        if team.active and max(keys) == 2019:
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


def main(start_year: int, end_year: int):
    process(start_year, end_year)
