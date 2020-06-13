from classes.classes import (
    Team,
    Year,
    TeamYear,
    Event,
    TeamEvent,
    Match,
    TeamMatch
)

import classes.sql as sql
session = sql.getSession()

'''Team'''


def getTeam(number):
    return session.query(Team).filter_by(number=number).first()


def getTeams():
    return session.query(Team).order_by('number').all()


'''Year'''


def getYear(year):
    return session.query(Year).filter_by(year=year).first()


def getYears():
    return session.query(Year).order_by('year').all()


'''Team Year'''


def getTeamYear(team, year):
    return session.query(TeamYear) \
           .filter(team_id=team) \
           .filter(year_id=year) \
           .first()


def getTeamYears():
    return session.query(TeamYear) \
           .order_by('year_id') \
           .order_by('number_id') \
           .all()


def getTeamYears_byTeam(team):
    return session.query(TeamYear) \
           .filter(team_id=team) \
           .order_by('year_id') \
           .all()


def getTeamYears_byYear(year):
    return session.query(TeamYear) \
           .filter(year_id=year) \
           .order_by('team_id') \
           .all()


team = Team(name="Cortechs Robotics",
            number=5511,
            state="NC",
            country="USA")

year = Year(year=2015)
team_year = TeamYear(team=team, year=year)
event = Event(year=year, key='2019abc', name='test2', state='test3', country='test4', district='test5')
team_event = TeamEvent(event=event, team_year=team_year)
match = Match(event=event, key="a", comp_level="b", set_number=1, match_number=2, red1=3, red2=4, red3=5, blue1=6, blue2=7, blue3=8, winner="Red")
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
