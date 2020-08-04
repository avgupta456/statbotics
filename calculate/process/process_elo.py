from collections import defaultdict
import statistics

from helper import utils
from models import elo
from process.logging import printStats


def process(start_year, end_year, SQL_Write, SQL_Read):
    teams = {}  # dict of team nums to team objs
    for team in SQL_Read.getTeams():
        teams[team.id] = team

    # constants from elo model
    start, mean_reversion = elo.start_rating(), elo.mean_reversion()

    team_years_all = {}  # master dictionary

    if start_year > 2003:
        team_years_2 = {}
        teamYears2 = SQL_Read.getTeamYears(year=start_year - 2)
        for teamYear in teamYears2:
            team_years_2[teamYear.team_id] = teamYear
        team_years_all[start_year - 2] = team_years_2

    if start_year > 2002:
        team_years_1 = {}
        teamYears1 = SQL_Read.getTeamYears(year=start_year - 1)
        for teamYear in teamYears1:
            team_years_1[teamYear.team_id] = teamYear
        team_years_all[start_year - 1] = team_years_1

    for year in range(start_year, end_year + 1):
        print(year)  # dicts for num to TeamYear, TeamMatch, most recent elo
        team_years, team_events, team_matches, team_elos = {}, {}, {}, {}
        team_match_ids = {}

        # win, loss, tie, count
        team_year_stats = defaultdict(lambda: [0, 0, 0, 0])

        sd_score = SQL_Read.getYear(year=year).score_sd
        teamYears = SQL_Read.getTeamYears(year=year)

        print("Team Year Setup")
        count = 0
        for teamYear in teamYears:
            # eventually will need 2021 logic here (continuation season)
            num = teamYear.team_id
            team_years[num] = teamYear
            team_matches[num] = []

            # gets elo using mean reversion
            elo_2yr = mean_reversion
            if (
                year - 2 in team_years_all
                and num in team_years_all[year - 2]
                and team_years_all[year - 2][num].elo_max is not None
            ):
                elo_2yr = team_years_all[year - 2][num].elo_max
            elo_1yr = mean_reversion
            if (
                year - 1 in team_years_all
                and num in team_years_all[year - 1]
                and team_years_all[year - 1][num].elo_max is not None
            ):
                elo_1yr = team_years_all[year - 1][num].elo_max
            start_rating = elo.existing_rating(elo_1yr, elo_2yr)
            team_elos[num] = start if year == 2002 else start_rating
            teamYear.elo_start = team_elos[num]  # saves new elo

            count += 1
            if count % 1000 == 0:
                SQL_Write.add()

        print("Matches")
        acc, mse, count = 0, 0, 0  # for statistics
        event_stats = defaultdict(lambda: [0, 0, 0])  # acc, mse, count
        matches = SQL_Read.getMatches_year(year=year)
        for match in sorted(matches):
            event_id = match.event_id
            red, blue = match.getTeams()
            red_elo_pre, blue_elo_pre = {}, {}
            team_match_ids[match.id] = {}
            for t in red:
                red_elo_pre[t] = team_elos[t]
                team_match_ids[match.id][t] = team_elos[t]
            for t in blue:
                blue_elo_pre[t] = team_elos[t]
                team_match_ids[match.id][t] = team_elos[t]

            # update object
            match.red_elo_sum = sum(red_elo_pre.values())
            match.blue_elo_sum = sum(blue_elo_pre.values())

            # updates win probability fields
            win_prob = elo.win_prob(red_elo_pre, blue_elo_pre)
            match.elo_win_prob = win_prob
            match.elo_winner = "red" if win_prob > 0.5 else "blue"

            # compute elo changes
            red_elo_post, blue_elo_post = elo.update_rating(
                sd_score,
                red_elo_pre,
                blue_elo_pre,
                match.red_score,
                match.blue_score,
                match.playoff,
            )

            winner = match.winner
            red_mapping = {"red": 0, "blue": 1, "draw": 2}
            blue_mapping = {"blue": 0, "red": 1, "draw": 2}

            # update dictionaries
            for t in red:
                team_elos[t] = red_elo_post[t]
                team_matches[t].append(red_elo_post[t])
                team_event_id = utils.getTeamEventId(t, match.event_id)
                if team_event_id not in team_events:
                    team_events[team_event_id] = [[red_elo_pre[t], match.playoff]]
                team_events[team_event_id].append([red_elo_post[t], match.playoff])
                team_year_stats[t][3] += 1
                team_year_stats[t][red_mapping[winner]] += 1
            for t in blue:
                team_elos[t] = blue_elo_post[t]
                team_matches[t].append(blue_elo_post[t])
                team_event_id = utils.getTeamEventId(t, match.event_id)
                if team_event_id not in team_events:
                    team_events[team_event_id] = [[blue_elo_pre[t], match.playoff]]
                team_events[team_event_id].append([blue_elo_post[t], match.playoff])
                team_year_stats[t][3] += 1
                team_year_stats[t][blue_mapping[winner]] += 1

            # update stats
            win_probs = {"red": 1, "blue": 0, "draw": 0.5}
            error = (win_probs[winner] - match.elo_win_prob) ** 2
            event_stats[event_id][1] += error  # mse
            mse += error

            if winner == match.elo_winner:
                event_stats[event_id][0] += 1  # acc
                acc += 1

            count += 1
            event_stats[event_id][2] += 1  # count
            if count % 1000 == 0:
                SQL_Write.add()

        # aggregate stats
        acc = round(acc / len(matches), 4)
        mse = round(mse / len(matches), 4)

        print("Team Matches")
        for team_match in SQL_Read.getTeamMatches(year=year):
            team_match.elo = team_match_ids[team_match.match_id][team_match.team_id]
        SQL_Write.commit()  # optional, reduces memory overhead

        print("Team Events")
        count = 0
        for team in teamYears:
            for team_event in team.team_events:
                if team_event.id not in team_events:
                    SQL_Write.remove(team_event)
                    continue

                data = team_events[team_event.id]
                elos = [obj[0] for obj in team_events[team_event.id]]
                team_event.elo_start = elos[0]
                team_event.elo_end = elos[-1]
                team_event.elo_max = max(elos)
                team_event.elo_mean = sum(elos) / len(elos)
                team_event.elo_diff = elos[-1] - elos[0]
                team_event.elo_pre_playoffs = elos[0]

                cont = True
                for i in range(len(data) - 1, -1, -1):
                    if cont and data[i][1] == 0:
                        ind = min(i + 1, len(data) - 1)
                        team_event.elo_pre_playoffs = data[ind][0]
                        cont = False

            count += 1
            if count % 1000 == 0:
                SQL_Write.add()

        SQL_Write.commit()

        print("Events")
        # all event elo stats based on pre-playoff elos
        for event in SQL_Read.getEvents_year(year=year):
            event_id = event.id
            elos = []
            for team_event in event.team_events:
                elos.append(team_event.elo_pre_playoffs)
            elos.sort(reverse=True)
            event.elo_max = elos[0]
            event.elo_top8 = -1 if len(elos) < 8 else elos[7]
            event.elo_top24 = -1 if len(elos) < 24 else elos[23]
            event.elo_mean = round(sum(elos) / len(elos), 2)
            event.elo_sd = round(statistics.pstdev(elos), 2)
            acc, mse, count = event_stats[event_id]
            event.elo_acc = round(acc / count, 4)
            event.elo_mse = round(mse / count, 4)

        print("Team Years")
        year_elos, count = [], 0
        for team in team_years:
            elos = team_matches[team]
            if elos == []:
                SQL_Write.remove(team_years[team])
                team_years.pop(team)
            else:
                elo_max = max(elos[min(len(elos) - 1, 8) :])
                year_elos.append(elo_max)

        year_elos.sort(reverse=True)
        team_year_count = len(team_years)
        for team in team_years:
            obj = team_years[team]
            elos = team_matches[team]
            elo_max = max(elos[min(len(elos) - 1, 8) :])
            obj.elo_max = elo_max
            obj.elo_mean = round(sum(elos) / len(elos), 2)
            obj.elo_end = team_elos[team]
            obj.elo_diff = obj.elo_end - obj.elo_start

            pre_champs = obj.elo_start
            for team_event in sorted(obj.team_events):
                # goes from team_event to event
                if team_event.event.type < 3:
                    pre_champs = team_event.elo_end
            obj.elo_pre_champs = pre_champs

            wins, losses, ties, count = team_year_stats[team]
            winrate = round((wins + 0.5 * ties) / count, 4)
            obj.wins = wins
            obj.losses = losses
            obj.ties = ties
            obj.count = count
            obj.winrate = winrate

            obj.elo_rank = rank = year_elos.index(elo_max) + 1
            obj.elo_percentile = round(rank / team_year_count, 4)

            count += 1
            if count % 1000 == 0:
                SQL_Write.add()

        print("Years")
        year_elos.sort(reverse=True)
        year_obj = SQL_Read.getYear(year=year)
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
        # keeps memory down
        if year - 2 in team_years_all:
            team_years_all.pop(year - 2)

        SQL_Write.commit()
        printStats(SQL_Write=SQL_Write, SQL_Read=SQL_Read)

    print("Teams")
    for team in SQL_Read.getTeams():
        years = {}
        wins, losses, ties, count = 0, 0, 0, 0
        for year in team.team_years:
            years[year.year_id] = year.elo_max
            wins += year.wins
            losses += year.losses
            ties += year.ties
            count += year.count
        keys = years.keys()
        vals = years.values()
        recent = []
        for year in range(2017, end_year + 1):
            if year in years:
                recent.append(years[year])
        r_y, y = len(recent), len(vals)
        team.elo = -1 if not team.active else years[max(keys)]

        """
        temporary solution applying mean reversion if no 2020 matches
        """
        if team.active and max(keys) == 2019:
            yr_1 = 1450 if 2019 not in years else years[2019]
            yr_2 = 1450 if 2018 not in years else years[2018]
            team.elo = 0.56 * yr_1 + 0.24 * yr_2 + 0.20 * 1450
        """
        End temporary block
        """

        team.elo_recent = -1 if r_y == 0 else round(sum(recent) / r_y, 2)
        team.elo_mean = -1 if y == 0 else round(sum(vals) / y, 2)
        team.elo_max = -1 if y == 0 else max(vals)

        winrate = round((wins + ties / 2) / count, 4)
        team.wins = wins
        team.losses = losses
        team.ties = ties
        team.count = count
        team.winrate = winrate

    SQL_Write.commit()
    printStats(SQL_Write=SQL_Write, SQL_Read=SQL_Read)


def test(start_year, end_year, SQL_Write, SQL_Read):
    return


def main(start_year, end_year, TBA, SQL_Write, SQL_Read, clean):
    process(start_year, end_year, SQL_Write, SQL_Read)
    test(start_year, end_year, SQL_Write, SQL_Read)
    printStats(SQL_Write=SQL_Write, SQL_Read=SQL_Read)
