from helper import utils
import pandas as pd
import stats

import statistics
import json

blacklist = [
    [2005, 'ga', 'f1m1'],
]

def get_data(start_year, end_year):
    team_matches = []
    for year in range(start_year, end_year+1):
        for m in utils.loadProcessedMatches(year):
            event = m.key.split("_")[0][4:]
            match = m.key.split("_")[1]

            for i in range(len(m.red)):
                start_elo, end_elo = round(m.red_ratings[i]), round(m.red_ratings_end[i])
                elo_diff, append = round(end_elo - start_elo), True

                for item in blacklist:
                    if(year==item[0] and event==item[1] and match==item[2]): append = False
                if(append): team_matches.append([year, event, match, m.red[i], start_elo, end_elo, elo_diff])

            for i in range(len(m.blue)):
                start_elo, end_elo = round(m.blue_ratings[i]), round(m.blue_ratings_end[i])
                elo_diff, append = round(end_elo - start_elo), True

                for item in blacklist:
                    if(year==item[0] and event==item[1] and match==item[2]): append = False
                if(append): team_matches.append([year, event, match, m.blue[i], start_elo, end_elo, elo_diff])

    team_matches = pd.DataFrame(team_matches, columns = ["year", "event", "match", "team", "elo_start", "elo_end", "elo_diff"])
    team_matches = team_matches.sort_values(by=['year', 'event', 'match', 'team'])
    team_matches.columns.names = ['id']

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
                    elo_pre_playoffs = round(temp.iloc[temp.shape[0]-1,5])

                elo_end = team_data.iloc[team_data.shape[0]-1, 5]
                elo_mean = round(team_data['elo_end'].mean())
                elo_max = team_data['elo_end'].max()
                elo_diff = round(elo_end - elo_start)

                team_events.append([year, event, team, elo_start,
                    elo_pre_playoffs, elo_end, elo_mean, elo_max, elo_diff])

    team_events = pd.DataFrame(team_events, columns = ["year", "event", "team", "elo_start", "elo_pre_playoffs", "elo_end", "elo_mean", "elo_max", "elo_diff"])
    yeam_events = team_events.sort_values(by=['year', 'event', 'team'])
    team_events.columns.names = ['id']

    champ_keys = ['arc', 'cars', 'carv', 'cur', 'dal', 'dar', 'gal', 'hop', 'new', 'roe', 'tes', 'tur']

    team_years = []
    for year in range(start_year, end_year+1):
        year_data_events = team_events[team_events.year == year]
        year_data_matches = team_matches[team_matches.year == year]

        teams_temp = utils.loadTeams(year)
        num_teams = len(teams_temp)

        ratings = []
        for t in teams_temp.values():
            ratings.append(t.get_rating_max())
        ratings.sort()

        for team in year_data_events['team'].unique():
            team_data_events = year_data_events[year_data_events.team == team]
            team_data_matches = year_data_matches[year_data_matches.team == team]
            elo_start = team_data_events.iloc[0, 3]
            elo_end = team_data_events.iloc[team_data_events.shape[0]-1, 5]
            elo_diff = round(elo_end - elo_start)

            if(len(set(champ_keys).intersection(set(team_data_events["event"])))==0): elo_pre_champs = elo_end
            else: elo_pre_champs = round(team_data_events[team_data_events.event.isin(champ_keys)].iloc[0, 3])

            elo_mean = round(team_data_matches['elo_end'].mean())
            elo_max = teams_temp[team].get_rating_max()

            rank = num_teams-ratings.index(elo_max)
            percentile = round((rank/num_teams), 4)
            elo_max = round(elo_max) #after so doesn't mess with index

            team_years.append([year, team, elo_start, elo_pre_champs, elo_end, elo_mean, elo_max, elo_diff, rank, percentile])

    team_years = pd.DataFrame(team_years, columns = ["year", "team", "elo_start", "elo_pre_champs", "elo_end", "elo_mean", "elo_max", "elo_diff", "rank", "percentile"])
    team_years = team_years.sort_values(by=['year', 'team'])
    team_years.columns.names = ['id']

    teams = []
    for team in team_years['team'].unique():
        team_data = team_years[team_years.team==team]
        elos, elo_sum, count = [-1]*(end_year-start_year+1), 0, 0
        for i in range(team_data.shape[0]):
            elos[team_data["year"].iloc[i]-start_year]=round(team_data["elo_max"].iloc[i])
            elo_sum, count = elo_sum + team_data["elo_max"].iloc[i], count + 1
        elo, elo_mean, elo_max = elos[-1], round(elo_sum/count), max(elos)
        if(elo==-1): elo=elos[-2] #accounts for 2020 season suspension
        elo_max_year = start_year+elos.index(elo_max)
        elos = ", ".join(str(x) for x in elos)
        teams.append([team, elo, elos, elo_mean, elo_max, elo_max_year])

    teams = pd.DataFrame(teams, columns=["team", "elo", "elos", "elo_mean", "elo_max", "elo_max_year"])
    teams = teams.sort_values(by=['team'])
    teams.columns.names = ['id']

    events = []
    for year in range(start_year, end_year+1):
        year_data = team_events[team_events.year == year]
        for event in year_data["event"].unique():
            elos = []
            event_data = year_data[year_data.event == event]
            for i in range(event_data.shape[0]):
                elos.append(round(event_data["elo_max"].iloc[i]))
            elos.sort(reverse=True)

            try: elo_max = elos[0]
            except Exception as e: elo_max= -1

            try: elo_top8 = elos[7]
            except Exception as e: elo_top8= -1

            try: elo_top24 = elos[23]
            except Exception as e: elo_top24= -1

            elo_mean, elo_sd = round(sum(elos)/len(elos)), round(statistics.pstdev(elos))
            events.append([year, event, elo_max, elo_top8, elo_top24, elo_mean, elo_sd])

    events = pd.DataFrame(events, columns=["year", "event", "elo_max", "elo_top8", "elo_top24", "elo_mean", "elo_sd"])
    events = events.sort_values(by=['year', 'event'])
    events.columns.names = ['id']

    years = []
    for year in range(start_year, end_year+1):
        teams_temp = utils.loadTeams(year)
        board, elos = sorted(teams_temp.values()), []
        for team in board: elos.append(round(team.get_rating_max()))
        elo_max = elos[0]
        elo_1p = round(elos[round(0.01*len(elos))])
        elo_5p = round(elos[round(0.05*len(elos))])
        elo_10p = round(elos[round(0.10*len(elos))])
        elo_25p = round(elos[round(0.25*len(elos))])
        elo_median = round(elos[round(0.50*len(elos))])
        elo_mean = round(sum(elos)/len(elos))
        elo_sd = round(statistics.pstdev(elos))
        mse, acc = stats.getStats(year)
        mse, acc = round(mse, 4), round(acc, 4)
        years.append([year, elo_max, elo_1p, elo_5p, elo_10p, elo_25p, elo_median, elo_mean, elo_sd, acc, mse])

    years = pd.DataFrame(years, columns=["year", "elo_max", "elo_1p", "elo_5p", "elo_10p", "elo_25p", "elo_median", "elo_mean", "elo_sd", "acc", "mse"])
    years = years.sort_values(by=['year'])
    years.columns.names = ['id']

    return team_matches, team_events, team_years, teams, events, years
