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
        E = Y.getEvent(event["key"])

        teamEvents = read_tba.getTeamEvents(event["key"])
        for teamEvent in teamEvents:
            E.addTeamEvent(teamEvent)

        matches = read_tba.getMatches(event["key"])
        for match in matches:
            E.addMatch(match)

utils.saveMain(M)

M = utils.loadMain()
print(M.getYears())
print(M.getYear(2002).getEvents())
print(M.getYear(2002).getEvent('2002va').getMatches())
