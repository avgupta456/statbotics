def search(SQL_Read):
    matches = SQL_Read.getTeam(5511).matches
    matches.sort()
    print(matches)
