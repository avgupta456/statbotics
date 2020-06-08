from tba import (
    read_tba
)

from classes import (
    Main,
)

from helper import (
    utils
)

import sys

start_year = 2002
end_year = 2002

sys.setrecursionlimit(int(1e6))
print("Recursion Limit: " + str(sys.getrecursionlimit()))
print()

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

    for event in events:
        print("\tEvent: " + str(event["key"]))
        Y.addEvent(event)
        E = Y.getEvent(event["key"])

        teamEvents = TBA.getTeamEvents(event["key"])
        for teamEvent in teamEvents:
            E.addTeamEvent(teamEvent)

        matches = TBA.getMatches(event["key"])
        for match in matches:
            E.addMatch(match)

            M = E.getMatch(match["key"])
            M.addTeamMatches()

    print("TBA Calls: " + str(TBA.getCount()))
    print()

    utils.saveMain(Main)

print("Total TBA Calls: " + str(TBA.getCount()))
print()

utils.saveMain(Main)

Main2 = utils.loadMain()
print(Main2.getYears())
print(Main2.getYear(2002).getEvents())
print(Main2.getYear(2002)
      .getEvent('2002va')
      .getMatch('2002va_qm1')
      .getTeamMatches())
