from classes import Team
import utils

import elo
import ts

def processYear(year):
    matches = utils.loadMatches(year)
    teams = {} #number to

    try: old_teams = utils.loadTeams(year-1)
    except Exception as e: old_teams = None

    for match in matches:
        for alliance in [match.red, match.blue]:
            for team in alliance:
                if team not in teams:
                    if old_teams!=None and team in old_teams:
                        teams[team] = Team(team, ts.existing_rating(old_teams[team]), elo.existing_rating(old_teams[team]))
                    else:
                        teams[team] = Team(team, ts.new_rating(), elo.new_rating())

    #print(sorted(teams.values()))

    for match in matches:
        ts.update_rating(year, teams, match)
        elo.update_rating(year, teams, match)

    #print(sorted(teams.values()))

    utils.saveTeams(year, teams)
    utils.saveProcessedMatches(year, matches)

def main():
    for year in range(2005,2021):
        print(year)
        processYear(year)

if __name__ == "__main__":
    main()
