import load_team_info
import load_matches

import process
import stats

import push_data

start_year = 2002
end_year = 2020


def load_data():
    load_matches.saveMatches(start_year, end_year)
    load_team_info.saveAllTeamsInfo()


def calculate_elos():
    process.processYears(start_year, end_year)
    stats.metrics()
    stats.mean()


def push():
    push_data.main(start_year, end_year)
