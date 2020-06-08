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
end_year = 2020

M = Main.Main()

<<<<<<< HEAD
Main = Main.Main()
TBA = read_tba.ReadTBA()

print("Loading Teams")
for team in TBA.getTeams():
    Main.addTeam(team)

for year in range(start_year, end_year + 1):
    print("Year " + str(year))
    Main.addYear({"year": year})
    Y = Main.getYear(year)

    print("  TeamYears")
    teamYears = TBA.getTeamYears(year)
    for teamYear in teamYears:
        Y.addTeamYear(teamYear)

    print("  Events")
    events = TBA.getEvents(year)
=======
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
>>>>>>> parent of c7ccf6c... finished classes
    for event in events:
        Y.addEvent(event)
        E = Y.getEvent(event["key"])

        teamEvents = TBA.getTeamEvents(event["key"])
        for teamEvent in teamEvents:
            E.addTeamEvent(teamEvent)

        matches = TBA.getMatches(event["key"])
        for match in matches:
            E.addMatch(match)

<<<<<<< HEAD
    print("TBA Calls: " + str(TBA.getCount()))
    print()

    utils.saveMain(Main)

print("Total TBA Calls: " + str(TBA.getCount()))
print()

utils.saveMain(Main)
=======
utils.saveMain(M)

M = utils.loadMain()
print(M.getYears())
print(M.getYear(2002).getEvents())
print(M.getYear(2002).getEvent('2002va').getMatches())
>>>>>>> parent of c7ccf6c... finished classes
