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

M = Main.Main()

for year in range(start_year, end_year + 1):
    M.addYear({"year": year})

for team in read_tba.getTeams():
    M.addTeam(team)

for year in range(start_year, end_year + 1):
    Y = M.getYear(year)
    teamYears = read_tba.getTeamYears(year)
    for teamYear in teamYears:
        Y.addTeamYear(teamYear)

    events = read_tba.getEvents(year)
    for event in events:
        Y.addEvent(event)

utils.saveMain(M)

M = utils.loadMain()
print(M.getYears())
print(M.getYear(2002).getEvents())
