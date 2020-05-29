import constants
import utils
import stats

from sqlalchemy import create_engine
import pandas as pd
import pymysql

import statistics
import datetime
import json

blacklist = [
    [2005, 'ga', 'f1m1'],
]

def get_data(start_year, end_year):
    team_matches = []
    id = 1

    for year in range(start_year, end_year+1):
        for m in utils.loadProcessedMatches(year):
            event = m.key.split("_")[0][4:]
            match = m.key.split("_")[1]
            time = m.time

            for i in range(len(m.red)):
                start_elo, end_elo = round(m.red_ratings[i]), round(m.red_ratings_end[i])
                elo_diff, append = round(end_elo - start_elo), True

                for item in blacklist:
                    if(year==item[0] and event==item[1] and match==item[2]): append = False

                if(append):
                    team_matches.append([id, year, event, match, time, m.red[i], start_elo, end_elo, elo_diff])
                    id += 1

            for i in range(len(m.blue)):
                start_elo, end_elo = round(m.blue_ratings[i]), round(m.blue_ratings_end[i])
                elo_diff, append = round(end_elo - start_elo), True

                for item in blacklist:
                    if(year==item[0] and event==item[1] and match==item[2]): append = False

                if(append):
                    team_matches.append([id, year, event, match, time, m.blue[i], start_elo, end_elo, elo_diff])
                    id += 1

    team_matches = pd.DataFrame(team_matches, columns = ["id", "year", "event", "match", "time", "team", "elo_start", "elo_end", "elo_diff"])
    team_matches = team_matches.sort_values(by=['year', 'event', 'team'])

    team_events = []
    id = 1

    for year in range(start_year, end_year+1):
        year_data = team_matches[team_matches.year == year]
        for event in year_data['event'].unique():
            event_data = year_data[year_data.event == event]
            time = event_data["time"].iloc[0]
            for team in event_data['team'].unique():
                team_data = event_data[event_data.team == team]
                tea_data = team_data.sort_values(by=['time'], ascending=True)

                elo_start = team_data["elo_start"].iloc[0]
                if (team_data["match"].iloc[0])[:2]!="qm":
                    elo_pre_playoffs = elo_start #handles only elim events
                else:
                    temp = team_data[team_data.match.str.startswith("qm")] #handles no playoffs
                    elo_pre_playoffs = temp["elo_end"].iloc[temp.shape[0]-1]

                elo_end = team_data["elo_end"].iloc[team_data.shape[0]-1]
                elo_mean = round(team_data['elo_end'].mean())
                elo_max = max(elo_start, team_data['elo_end'].max())
                elo_diff = round(elo_end - elo_start)

                team_events.append([id, year, event, time, team, elo_start,
                    elo_pre_playoffs, elo_end, elo_mean, elo_max, elo_diff])
                id += 1

    team_events = pd.DataFrame(team_events, columns = ["id", "year", "event", "time", "team",
        "elo_start", "elo_pre_playoffs", "elo_end", "elo_mean", "elo_max", "elo_diff"])
    yeam_events = team_events.sort_values(by=['year', 'event', 'team'])

    champ_keys = ['arc', 'cars', 'carv', 'cur', 'dal', 'dar', 'gal', 'hop', 'new', 'roe', 'tes', 'tur']

    team_years = []
    all_teams_info = utils.loadAllTeamsInfo()
    id = 1

    for year in range(start_year, end_year+1):
        year_data_events = team_events[team_events.year == year]
        year_data_matches = team_matches[team_matches.year == year]

        teams_temp = utils.loadTeams(year)
        for team in year_data_events['team'].unique():
            team_data_events = year_data_events[year_data_events.team == team]
            team_data_matches = year_data_matches[year_data_matches.team == team]
            team_data_events = team_data_events.sort_values(by=['time'], ascending=True)
            team_data_matches = team_data_matches.sort_values(by=['time'], ascending=True)
            elo_start = team_data_events["elo_start"].iloc[0]
            elo_end = team_data_events["elo_end"].iloc[team_data_events.shape[0]-1]
            elo_diff = round(elo_end - elo_start)

            if(len(set(champ_keys).intersection(set(team_data_events["event"])))==0): elo_pre_champs = elo_end
            else: elo_pre_champs = round(team_data_events[team_data_events.event.isin(champ_keys)]["elo_start"].iloc[0])

            elo_mean = round(team_data_matches['elo_end'].mean())
            elo_max = teams_temp[team].get_rating_max()

            elo_max = round(elo_max) #after so doesn't mess with index

            [name, country, state, district, _] = all_teams_info[team]

            team_years.append([id, year, team, name, region, district, elo_start,
                elo_pre_champs, elo_end, elo_mean, elo_max, elo_diff])
            id += 1

    team_years = pd.DataFrame(team_years, columns = ["id", "year", "team", "name", "country", "state",
    "district", "elo_start", "elo_pre_champs", "elo_end", "elo_mean", "elo_max", "elo_diff"])
    team_years = team_years.sort_values(by=['year', 'team'])

    teams = []

    utils.saveAllTeams(team_years['team'].unique())
    for team in team_years['team'].unique():

        team_data = team_years[team_years.team==team]
        elos, elo_sum, count = [-1]*(end_year-start_year+1), 0, 0
        for i in range(team_data.shape[0]):
            elos[team_data["year"].iloc[i]-start_year]=round(team_data["elo_max"].iloc[i])
            elo_sum, count = elo_sum + team_data["elo_max"].iloc[i], count + 1
        elo, elo_mean, elo_max = elos[-1], round(elo_sum/count), max(elos)

        #takes whatever years exist 2016-Present
        total, years = sum(elos[-5:]), 5
        for i in range(5):
            if(elos[-i-1]==-1):
                total, years = total + 1, years - 1
        if(years==0): elo_recent = -1
        else: elo_recent = round(total/years)

        '''accounts for 2020 season suspension (with mean revision)'''
        if(elo==-1):
            try: elo_1yr = elo[-2]
            except Exception as e: elo_1yr = -1

            try: elo_2yr = elo[-3]
            except Exception as e: elo_2yr = -1

            if(elo_1yr==-1):
                elo = -1 #team has not played last two years, inactive
            elif(elo_2yr==-1):
                elo = elo_1yr * 0.56 + 1450 * 0.44 #rookie team
            else:
                elo = elo_1yr * 0.56 + elo_2yr * 0.24 + 1450 * 0.20

        elo_max_year = start_year+elos.index(elo_max)
        [name, country, state, district, years] = all_teams_info[team]
        active = (elo!=-1) #have a current elo

        teams.append([team, name, country, state, district, years, active,
            elo, elo_recent, elo_mean, elo_max, elo_max_year])

    teams = pd.DataFrame(teams, columns=["team", "name", "country", "state", "district",
    "years_active", "active", "elo", "elo_recent", "elo_mean", "elo_max", "elo_max_year"])
    teams = teams.sort_values(by=['team'])

    events = []
    id = 1

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
            events.append([id, year, event, elo_max, elo_top8, elo_top24, elo_mean, elo_sd])
            id += 1

    events = pd.DataFrame(events, columns=["id", "year", "event", "elo_max", "elo_top8", "elo_top24", "elo_mean", "elo_sd"])
    events = events.sort_values(by=['year', 'event'])

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

def push_data(data):
    team_matches, team_events, team_years, teams, events, years = data
    engine = create_engine('mysql+pymysql://'+constants.CLOUDSQL_USER+':'+constants.CLOUDSQL_PASSWORD
        +'@'+constants.CLOUDSQL_HOST+':'+constants.CLOUDSQL_PORT+'/'+constants.CLOUDSQL_DATABASE)

    team_matches.to_sql('rankings_teammatch', engine, if_exists='replace', index=False)
    team_events.to_sql('rankings_teamevent', engine, if_exists='replace', index=False)
    team_years.to_sql('rankings_teamyear', engine, if_exists='replace', index=False)
    teams.to_sql('rankings_team', engine, if_exists='replace', index=False)
    events.to_sql('rankings_event', engine, if_exists='replace', index=False)
    years.to_sql('rankings_year', engine, if_exists='replace', index=False)

def main(startYear, endYear):
    data = get_data(startYear, endYear)
    push_data(data)

if __name__ == "__main__":
    start = datetime.datetime.now()
    main()

    end = datetime.datetime.now()
    print("Total Time: " + str(end-start))
