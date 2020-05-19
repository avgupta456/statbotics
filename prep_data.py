from helper import utils
import pandas as pd
import stats

import statistics

def get_data(start_year, end_year):
    team_matches = []
    for year in range(start_year, end_year+1):
        for m in utils.loadProcessedMatches(year):
            event = m.key.split("_")[0][4:]
            match = m.key.split("_")[1]

            for i in range(len(m.red)):
                start_elo, end_elo = m.red_ratings[i], m.red_ratings_end[i]
                elo_diff = end_elo - start_elo
                team_matches.append([year, event, match, m.red[i], start_elo, end_elo, elo_diff])

            for i in range(len(m.blue)):
                start_elo, end_elo = m.blue_ratings[i], m.blue_ratings_end[i]
                elo_diff = end_elo - start_elo
                team_matches.append([year, event, match, m.blue[i], start_elo, end_elo, elo_diff])

    team_matches = pd.DataFrame(team_matches, columns = ["year", "event", "match", "team", "elo_start", "elo_end", "elo_diff"])

    team_events = []
    for year in range(start_year, end_year+1):
        year_data = team_matches[team_matches.year == year]
        for event in year_data['event'].unique():
            event_data = year_data[year_data.event == event]
            for team in event_data['team'].unique():
                team_data = event_data[event_data.team == team]

                elo_start = team_data.iloc[0, 4]
                if team_data["match"].iloc[0][:2]!="qm":
                    elo_pre_playoffs = elo_start
                else:
                    temp = team_data[team_data.match.str.startswith("qm")]
                    elo_pre_playoffs = temp.iloc[temp.shape[0]-1,5]

                elo_end = team_data.iloc[team_data.shape[0]-1, 5]
                elo_mean = team_data['elo_end'].mean()
                elo_max = team_data['elo_end'].max()
                elo_diff = elo_end - elo_start

                team_events.append([year, event, team, elo_start,
                    elo_pre_playoffs, elo_end, elo_mean, elo_max, elo_diff])

    team_events = pd.DataFrame(team_events, columns = ["year", "event", "team", "elo_start", "elo_pre_playoffs", "elo_end", "elo_mean", "elo_max", "elo_diff"])

    champ_keys = ['arc', 'cars', 'carv', 'cur', 'dal', 'dar', 'gal', 'hop', 'new', 'roe', 'tes', 'tur']

    team_years = []
    for year in range(start_year, end_year+1):
        year_data_events = team_events[team_events.year == year]
        year_data_matches = team_matches[team_matches.year == year]

        teams = utils.loadTeams(year)
        num_teams = len(teams)

        ratings = []
        for t in teams.values():
            ratings.append(t.get_rating_max())
        ratings.sort()

        for team in year_data_events['team'].unique():
            team_data_events = year_data_events[year_data_events.team == team]
            team_data_matches = year_data_matches[year_data_matches.team == team]
            elo_start = team_data_events.iloc[0, 3]
            elo_end = team_data_events.iloc[team_data_events.shape[0]-1, 5]
            elo_diff = elo_end - elo_start

            if(len(set(champ_keys).intersection(set(team_data_events["event"])))==0): elo_pre_champs = elo_end
            else: elo_pre_champs = team_data_events[team_data_events.event.isin(champ_keys)].iloc[0, 3]

            elo_mean = team_data_matches['elo_end'].mean()
            elo_max = teams[team].get_rating_max()

            rank = num_teams-ratings.index(elo_max)
            percent = int(1e4*rank/num_teams)/1e2

            team_years.append([year, team, elo_start, elo_pre_champs, elo_end, elo_mean, elo_max, elo_diff, rank, percent])

    team_years = pd.DataFrame(team_years, columns = ["year", "team", "elo_start", "elo_pre_champs", "elo_end", "elo_mean", "elo_max", "elo_diff", "rank", "percentile"])

    teams = []
    for team in team_years['team'].unique():
        team_data = team_years[team_years.team==team]
        elos, elo_sum, count = [-1]*(end_year-start_year+1), 0, 0
        for i in range(team_data.shape[0]):
            elos[team_data["year"].iloc[i]-start_year]=team_data["elo_max"].iloc[i]
            elo_sum, count = elo_sum + team_data["elo_max"].iloc[i], count + 1
        elo, elo_mean, elo_max = elos[-1], elo_sum/count, max(elos)
        elo_max_year = start_year+elos.index(elo_max)
        elos = ", ".join(str(x) for x in elos)
        teams.append([team, elo, elos, elo_mean, elo_max, elo_max_year])

    teams = pd.DataFrame(teams, columns=["team", "elo", "elos", "elo_mean", "elo_max", "elo_max_year"])

    events = []
    for year in range(start_year, end_year+1):
        year_data = team_events[team_events.year == year]
        for event in year_data["event"].unique():
            elos = []
            event_data = year_data[year_data.event == event]
            for i in range(event_data.shape[0]):
                elos.append(event_data["elo_max"].iloc[i])

            try: elo_max = elos[0]
            except Exception as e: elo_max= -1

            try: elo_top8 = elos[7]
            except Exception as e: elo_top8= -1

            try: elo_top24 = elos[23]
            except Exception as e: elo_top24= -1

            elo_mean, elo_sd = sum(elos)/len(elos), statistics.pstdev(elos)
            events.append([year, event, elo_max, elo_top8, elo_top24, elo_mean, elo_sd])

    events = pd.DataFrame(events, columns=["year", "event", "elo_max", "elo_top8", "elo_top24", "elo_mean", "elo_sd"])

    years = []
    for year in range(start_year, end_year+1):
        teams = utils.loadTeams(year)
        board, elos = sorted(teams.values()), []
        for team in board: elos.append(team.get_rating_max())
        elo_max = elos[0]
        elo_1p = elos[int(0.01*len(elos))]
        elo_5p = elos[int(0.05*len(elos))]
        elo_10p = elos[int(0.10*len(elos))]
        elo_25p = elos[int(0.25*len(elos))]
        elo_median = elos[int(0.50*len(elos))]
        elo_mean = sum(elos)/len(elos)
        elo_sd = statistics.pstdev(elos)
        mse, acc = stats.getStats(year)
        years.append([year, elo_max, elo_1p, elo_5p, elo_10p, elo_25p, elo_median, elo_mean, elo_sd, acc, mse])

    years = pd.DataFrame(years, columns=["year", "elo_max", "elo_1p", "elo_5p", "elo_10p", "elo_25p", "elo_median", "elo_mean", "elo_sd", "acc", "mse"])
    return team_matches, team_events, team_years, teams, events, years

team_matches, team_events, team_years, teams, events, years = get_data(2002, 2020)

print("TEAM_MATCHES")
print(team_matches)
print()

print("TEAM EVENTS")
print(team_events)
print()

print("TEAM_YEARS")
print(team_years)
print()

print("TEAMS")
print(teams)
print()

print("EVENTS")
print(events)
print()

print("YEARS")
print(years)
print()
