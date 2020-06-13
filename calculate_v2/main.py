from tba import (
    read_tba,
)

from classes import (
    sql,
    write,
)

start_year = 2002
end_year = 2002

TBA = read_tba.ReadTBA()

SQL = sql.SQL(clean=True)
SQL_Write = write.SQL_Write(SQL)

print("Loading Teams")
for team in TBA.getTeams():
    SQL_Write.addTeam(team, False)
    print(team)
SQL_Write.commit()

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
