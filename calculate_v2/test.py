from tba import (
    read_tba
)

from classes import (
    Main,
)

from helper import (
    utils
)

start_year = 2002
end_year = 2002

'''
M = Main.Main()

for year in range(start_year, end_year + 1):
    M.addYear(year)

for team in read_tba.getTeams():
    M.addTeam(team)

for year in range(start_year, end_year + 1):
    Y = M.getYear(year)
    data = read_tba.getTeamYears(year)
    for teamYear in data:
        Y.addTeamYear(teamYear)

utils.saveMain(M)
'''
M = utils.loadMain()
print(M.getTeams())
print(M.getYears())
