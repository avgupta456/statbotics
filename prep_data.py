from helper import utils
import pandas as pd

team_matches = []
for year in range(2002, 2021):
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

team_matches = pd.DataFrame(team_matches, columns = ["year", "event", "match", "team", "start_elo", "end_elo", "elo_diff"])

print(team_matches)

team_events = []
for year in range(2002, 2021):
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
            elo_mean = team_data['end_elo'].mean()
            elo_max = team_data['end_elo'].max()
            elo_diff = elo_end - elo_start

            team_events.append([year, event, team, elo_start,
                elo_pre_playoffs, elo_end, elo_mean, elo_max, elo_diff])

team_events = pd.DataFrame(team_events, columns = ["year", "event", "team", "elo_start", "elo_pre_playoffs", "elo_end", "elo_mean", "elo_max", "elo_diff"])
print(team_events)
