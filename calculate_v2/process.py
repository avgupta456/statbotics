def process(start_year, end_year, TBA, SQL_Write, SQL_Read):
    print("Loading Teams")
    for team in TBA.getTeams():
        SQL_Write.addTeam(team, False)
    SQL_Write.commit()

    for year in range(start_year, end_year + 1):
        print("Year " + str(year))
        SQL_Write.addYear({"year": year}, False)

        teamYears = TBA.getTeamYears(year)
        for teamYear in teamYears:
            SQL_Write.addTeamYear(teamYear, False)
        SQL_Write.commit()

        print("  Events")
        events = TBA.getEvents(year)
        for event in events:
            event_key = event["key"]
            print("\tEvent: " + str(event_key))
            SQL_Write.addEvent(event, False)
            event_id = SQL_Read.getEvent_byKey(event_key).getId()

            teamEvents = TBA.getTeamEvents(event_key)
            for teamEvent in teamEvents:
                teamEvent["year"] = year
                teamEvent["event"] = event_id
                SQL_Write.addTeamEvent(teamEvent, False)

            matches = TBA.getMatches(event_key)
            for match in matches:
                match["year"] = year
                match["event"] = event_id
                SQL_Write.addMatch(match, False)

        SQL_Write.commit()

        print("TBA Calls: " + str(TBA.getCount()))
        print()

    print("Total TBA Calls: " + str(TBA.getCount()))
    print()
