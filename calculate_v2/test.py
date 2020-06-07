from classes import (
    Main,
    Team,
    Year,
    TeamYear,
    Event,
    TeamEvent,
    Match,
    TeamMatch
)

M = Main.Main()
print(M)

M.addTeam(5511)
M.addTeam(254)
M.addTeam(1323)

print(M.getTeams())
