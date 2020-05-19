from helper import utils
import pandas as pd

start_year = 2002
end_year = 2020

team_matches = []
for year in range(start_year, end_year+1):
    print(year)
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

print(team_matches)

team_events = []
for year in range(start_year, end_year+1):
    print(year)
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
print(team_events)

champ_keys = ['arc', 'cars', 'carv', 'cur', 'dal', 'dar', 'gal', 'hop', 'new', 'roe', 'tes', 'tur']

team_years = []
for year in range(start_year, end_year+1):
    print(year)
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
print(team_years)

teams = []
for team in team_years['team'].unique():
    team_data = team_years[team_years.team==team]
    elos, sum, count = [-1]*(end_year-start_year+1), 0, 0
    for i in range(team_data.shape[0]):
        elos[team_data["year"].iloc[i]-start_year]=team_data["elo_max"].iloc[i]
        sum, count = sum + team_data["elo_max"].iloc[i], count + 1
    elo, elo_mean, elo_max = elos[-1], sum/count, max(elos)
    elo_max_year = start_year+elos.index(elo_max)
    elos = ", ".join(str(x) for x in elos)
    teams.append([team, elo, elos, elo_mean, elo_max, elo_max_year])

teams = pd.DataFrame(teams, columns=["team", "elo", "elos", "elo_mean", "elo_max", "elo_max_year"])
print(teams)
