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


'''
year = Year(year=2015)
team_year = TeamYear(team=team, year=year)
event = Event(year=year, key='2019abc', name='test2',
    state='test3', country='test4', district='test5')
team_event = TeamEvent(event=event, team_year=team_year)
match = Match(event=event, key="a", comp_level="b", set_number=1,
    match_number=2, red1=3, red2=4, red3=5, blue1=6,
    blue2=7, blue3=8, winner="Red")
team_match = TeamMatch(team_event=team_event, match=match)
session.add_all([team, year, team_year, event, team_event, match, team_match])
session.commit()

query = session.query(Team).filter_by(name='Cortechs Robotics').first()
print(query)

query = session.query(Year).filter_by(year=2015).first()
print(query)

query = session.query(TeamYear).filter_by(id=1).first()
print(query)

query = session.query(Event).filter_by(id=1).first()
print(query)

query = session.query(TeamEvent).filter_by(id=1).first()
print(query)

query = session.query(Match).filter_by(id=1).first()
print(query)

query = session.query(TeamMatch).filter_by(id=1).first()
print(query)

print(getTeam(5511))
print(getTeams())
print(getYears())
'''
