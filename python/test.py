import statbotics

sb = statbotics.Statbotics()

print("Get Team")
print(sb.getTeam(5511))
print()

print("Get Teams")
print(sb.getTeams(district="fnc"))
print()

print("Get Year")
print(sb.getYear(2019))
print()

print("Get Years")
print(sb.getYears())
print()

print("Get Team Year")
print(sb.getTeamYear(team=5511, year=2019))
print()

print("Get Team Years")
print(sb.getTeamYears(team=5511))
print()

print("Get Event")
print(sb.getEvent("2019ncwak"))
print()

print("Get Events")
print(sb.getEvents(district="fnc"))
print()

print("Get Team Event")
print(sb.getTeamEvent(team=5511, event="2019ncwak"))
print()

print("Get Team Events")
print(sb.getTeamEvents(team=5511, year=2019))
print()

print("Get Match")
print(sb.getMatch("2019ncwak_qm6"))
print()

print("Get Matches")
print(sb.getMatches(event="2019ncwak"))
print()

print("Get Team Match")
print(sb.getTeamMatch(team=5511, match="2019ncwak_qm6"))
print()

print("Get Team Matches")
print(sb.getTeamMatches(team=5511, event="2019ncwak"))
print()
