from scripts.logging import printStats

from elo import elo


def process_elo(start_year, end_year, SQL_Write, SQL_Read):
    teams = {}
    for team in SQL_Read.getTeams():
        teams[team.getNumber()] = team

    start, mean_reversion = elo.start_rating(), elo.mean_reversion()

    team_years_all = {}
    for year in range(start_year, end_year + 1):
        team_years = {}
        for teamYear in SQL_Read.getTeamYears(year=year):
            num = teamYear.getTeam()
            team_years[num] = teamYear
            elo_2yr = mean_reversion
            if year-2 in team_years_all and \
                    num in team_years_all[year-2] and \
                    team_years_all[year-2][num].elo_max is not None:
                elo_2yr = team_years_all[year-2][num].elo_max
            elo_1yr = mean_reversion
            if year-1 in team_years_all and \
                    num in team_years_all[year-1] and \
                    team_years_all[year-1][num].elo_max is not None:
                elo_1yr = team_years_all[year-1][num].elo_max
            start_rating = elo.existing_rating(elo_1yr, elo_2yr)
            teamYear.start_rating = start if year == 2002 else start_rating
            print(teamYear, teamYear.start_rating)
            '''TODO ELO UPDATES HERE'''
        team_years_all[year] = team_years


def main(start_year, end_year, SQL_Write, SQL_Read):
    process_elo(start_year, end_year, SQL_Write, SQL_Read)
    printStats(SQL_Write=SQL_Write, SQL_Read=SQL_Read)
