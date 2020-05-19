from helper import utils

team_matches = []
for year in range(2002, 2021):
    print(year)
    for m in utils.loadProcessedMatches(year):
        event = m.key.split("_")[0]
        match = m.key.split("_")[1]

        for i in range(len(m.red)):
            start_elo, end_elo = m.red_ratings[i], m.red_ratings_end[i]
            elo_diff = end_elo - start_elo
            data = [year, event, match, m.red[i], start_elo, end_elo, elo_diff]
            team_matches.append(data)

        for i in range(len(m.blue)):
            start_elo, end_elo = m.blue_ratings[i], m.blue_ratings_end[i]
            elo_diff = end_elo - start_elo
            data = [year, event, match, m.blue[i], start_elo, end_elo, elo_diff]
            team_matches.append(data)

print(len(team_matches))
