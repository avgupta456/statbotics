import load_team_info
import load_matches

start_year = 2002
end_year = 2020

def load_data():
    load_matches.saveMatches(start_year, end_year)
    load_team_info.saveAllTeamsInfo()

import process
import stats

def calculate_elos():
    process.processYears(start_year, end_year)
    stats.metrics()
    stats.mean()

import push_data

def push():
    push_data.main(start_year, end_year)
