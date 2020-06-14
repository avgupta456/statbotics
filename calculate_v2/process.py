import datetime
start = datetime.datetime.now()


def printStats(TBA, SQL_Write, SQL_Read, print_sql=False):
    print()

    if TBA is not None:
        print("TBA Calls: " + str(TBA.getStats()[0]))
        print("TBA Cache: " + str(TBA.getStats()[1]))
        print()

    if SQL_Write is not None:
        print("SQL Writes: " + str(SQL_Write.getStats()[0]))
        print("SQL Commits: " + str(SQL_Write.getStats()[1]))

    if SQL_Read is not None:
        print("SQL Reads: " + str(SQL_Read.getStats()))

    if SQL_Write is not None or SQL_Read is not None:
        print()

    if print_sql:
        print("Total Teams: " + str(SQL_Read.getTotalTeams()))
        print("Total Years: " + str(SQL_Read.getTotalYears()))
        print("Total TeamYears: " + str(SQL_Read.getTotalTeamYears()))
        print("Total Events: " + str(SQL_Read.getTotalEvents()))
        print("Total TeamEvents: " + str(SQL_Read.getTotalTeamEvents()))
        print("Total Matches: " + str(SQL_Read.getTotalMatches()))
        print("Total TeamMatches: " + str(SQL_Read.getTotalTeamMatches()))
        print()

    print("Time Elapsed: " + str(datetime.datetime.now()-start))
    print()


def process(start_year, end_year, TBA, SQL_Write, SQL_Read, clean=True):
    print("Loading Teams")
    for team in TBA.getTeams():
        SQL_Write.addTeam(team, check=not clean, add=False, commit=False)
    SQL_Write.add()

    for year in range(start_year, end_year + 1):
        print("Year " + str(year))
        SQL_Write.addYear({"year": year},
                          check=not clean,
                          add=False,
                          commit=False)

        teamYears = TBA.getTeamYears(year)
        for teamYear in teamYears:
            SQL_Write.addTeamYear(teamYear,
                                  check=not clean,
                                  add=False,
                                  commit=False)
        SQL_Write.add()

        print("    Events")
        events = TBA.getEvents(year)
        for event in events:
            event_key = event["key"]
            print("\tEvent: " + str(event_key))
            SQL_Write.addEvent(event, check=not clean, add=True, commit=False)

            event_id = SQL_Read.getEvent_byKey(event_key).getId()
            event_time = event["time"]

            teamEvents = TBA.getTeamEvents(event_key)
            for teamEvent in teamEvents:
                teamEvent["year"] = year
                teamEvent["event_id"] = event_id
                teamEvent["time"] = event_time
                SQL_Write.addTeamEvent(teamEvent,
                                       check=not clean,
                                       add=False,
                                       commit=False)
            SQL_Write.add()
            matches = TBA.getMatches(event_key, event_time)
            for match in matches:
                match["year"] = year
                match["event"] = event_id
                SQL_Write.addMatch(match,
                                   check=not clean,
                                   add=False,
                                   commit=False)
        SQL_Write.add()
        printStats(TBA, SQL_Write, SQL_Read)

    SQL_Write.add(match_objects=True)  # match objects
    post_process(TBA, SQL_Write, SQL_Read)
    printStats(TBA, SQL_Write, SQL_Read)


# removes REALLY old teams and adds district labels
def post_process(TBA, SQL_Write, SQL_Read):
    teams = SQL_Read.getTeams()

    for team in teams:
        '''Removes Teams With No Matches'''
        matches = SQL_Read.getTeamMatches(team=team.getNumber())
        events = SQL_Read.getTeamEvents(team=team.getNumber())
        years = SQL_Read.getTeamYears(team=team.getNumber())
        if len(matches) == 0:
            print("Remove " + team.getName())
            for event in events:
                SQL_Write.remove(event)
            for year in years:
                SQL_Write.remove(year)
            SQL_Write.remove(team)
        else:
            '''Checks if active in 2020'''
            team.active = 0
            for year in years:
                if year.getYear() == 2020:
                    team.active = 1

            '''Retrieves district'''
            district = TBA.getTeamDistrict(team.getNumber())
            team.district = district

    events = SQL_Read.getEvents()
    for event in events:
        matches = SQL_Read.getMatches(event=event.getId())
        if len(matches) == 0:
            team_events = SQL_Read.getTeamEvents(event=event.getId())
            for team_event in team_events:
                SQL_Write.remove(team_event)
            SQL_Write.remove(event)

    SQL_Write.commit()
    printStats(None, SQL_Write, SQL_Read)
