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

M.addYear(2019)

M.addTeam(5511)
M.addTeam(254)
M.addTeam(1323)

print(M.getTeams())

T = M.getTeam(5511)
T.addTeamYear(2019)
print(T.getTeamYears())

Y = M.getYear(2019)
print(Y.getTeamYears())
