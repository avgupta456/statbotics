import sys

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

# for pickling
sys.setrecursionlimit(int(1e6))
print("Recursion Limit: " + str(sys.getrecursionlimit()))
print()

Main = Main.Main()

print("Loading Teams")
for team in read_tba.getTeams():
    Main.addTeam(team)

for year in range(start_year, end_year + 1):
    print("Year " + str(year))
    Main.addYear({"year": year})
    Y = Main.getYear(year)

    print("  TeamYears")
    teamYears = read_tba.getTeamYears(year)
    for teamYear in teamYears:
        Y.addTeamYear(teamYear)

    print("  Events")
    events = read_tba.getEvents(year)
    for event in events:
        print("\tEvent " + str(event["key"]))
        Y.addEvent(event)
        E = Y.getEvent(event["key"])

        teamEvents = read_tba.getTeamEvents(event["key"])
        for teamEvent in teamEvents:
            E.addTeamEvent(teamEvent)

        matches = read_tba.getMatches(event["key"])
        for match in matches:
            E.addMatch(match)
            M = E.getMatch(match["key"])

            M.addTeamMatches()
print()
utils.saveMain(M)
