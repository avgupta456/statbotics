import time

from scripts.logging import printStats


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
            curr_time = int(time.time())
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
                matches = TBA.getMatches(year,
                                         event_key,
                                         event_time,
                                         cache=cache)
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


def main(start_year, end_year, TBA, SQL_Write, SQL_Read,
         clean=False, cache=True):
    process(start_year, end_year, TBA, SQL_Write, SQL_Read, clean, cache)
    post_process(TBA, SQL_Write, SQL_Read, clean)
    printStats()
