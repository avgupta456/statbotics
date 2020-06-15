import time
import datetime

start = datetime.datetime.now()
curr_time = int(time.time())


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


def process(start_year, end_year, TBA, SQL_Write, SQL_Read,
            clean=False, cache=True):

    if clean:
        print("Loading Teams")
        for team in TBA.getTeams(cache=cache):
            SQL_Write.addTeam(team, check=False, add=False, commit=False)
        SQL_Write.add()

    all_teams = [t.getNumber() for t in SQL_Read.getTeams()]
    for year in range(start_year, end_year + 1):
        print("Year " + str(year))
        SQL_Write.addYear({"year": year},
                          check=(not clean),
                          add=False,
                          commit=False)

        team_years = [t.getTeam() for t in SQL_Read.getTeamYears(year=year)]
        for teamYear in TBA.getTeamYears(year, cache=cache):
            # handles teams with no matches removed in postprocessing
            team_year = teamYear["team"]
            if team_year not in team_years and team_year in all_teams:
                SQL_Write.addTeamYear(teamYear,
                                      check=False,
                                      add=False,
                                      commit=False)
        SQL_Write.add()

        events = TBA.getEvents(year, cache=cache)
        for event in events:
            event_key = event["key"]
            event_written = SQL_Write.addEvent(event,
                                               check=(not clean),
                                               add=True,
                                               commit=False)

            # if the match is within five days
            if event_written or abs(curr_time - event["time"]) < 432000:
                event_id = SQL_Read.getEventId_byKey(event_key)
                event_time = event["time"]

                teamEvents = TBA.getTeamEvents(event_key, cache=cache)
                for teamEvent in teamEvents:
                    teamEvent["year"] = year
                    teamEvent["event_id"] = event_id
                    teamEvent["time"] = event_time
                    SQL_Write.addTeamEvent(teamEvent,
                                           check=(not clean),
                                           add=False,
                                           commit=False)
                SQL_Write.add()
                matches = TBA.getMatches(event_key, event_time, cache=cache)
                for match in matches:
                    match["year"] = year
                    match["event"] = event_id
                    SQL_Write.addMatch(match,
                                       check=(not clean),
                                       add=False,
                                       commit=False)

        SQL_Write.add(match_objects=True)
        printStats(TBA, SQL_Write, SQL_Read)

    SQL_Write.add(match_objects=True)  # match objects
    post_process(TBA, SQL_Write, SQL_Read, clean)
    printStats(TBA, SQL_Write, SQL_Read)


# removes REALLY old teams and adds district labels
def post_process(TBA, SQL_Write, SQL_Read, clean=False):
    if clean:
        print("Removing Old Teams")
        for team in SQL_Read.getTeams():
            '''Removes Teams With No Matches'''
            matches = team.matches
            if len(matches) == 0:
                events = team.team_events
                years = team.team_years
                for event in events:
                    SQL_Write.remove(event)
                for year in years:
                    SQL_Write.remove(year)
                SQL_Write.remove(team)
        SQL_Write.commit()

    print("Updating Team Entries")
    active_teams = [t.getTeam() for t in SQL_Read.getTeamYears(year=2020)]
    for team in SQL_Read.getTeams():
        '''Checks if active in 2020'''
        team.active = 1 if team.getNumber() in active_teams else 0

        '''Retrieves district'''
        if team.district is None:
            team.district = TBA.getTeamDistrict(team.getNumber())
    SQL_Write.commit()
