from classes.classes import (
    Team,
    Year,
    TeamYear,
    Event,
    TeamEvent,
    # Match,
    # TeamMatch
)


class SQL_Read:
    def __init__(self, SQL):
        self.session = SQL.getSession()

    '''Team'''

    def getTeam(self, number):
        return self.session.query(Team).filter_by(number=number).first()

    def getTeams(self):
        return self.session.query(Team).order_by('number').all()

    '''Year'''

    def getYear(self, year):
        return self.session.query(Year).filter_by(year=year).first()

    def getYears(self):
        return self.session.query(Year).order_by('year').all()

    '''Team Year'''

    def getTeamYear(self, team, year):
        return self.session.query(TeamYear) \
               .filter_by(team_id=team) \
               .filter_by(year_id=year) \
               .first()

    def getTeamYears(self):
        return self.session.query(TeamYear) \
               .order_by('year_id') \
               .order_by('number_id') \
               .all()

    def getTeamYears_byTeam(self, team):
        return self.session.query(TeamYear) \
               .filter_by(team_id=team) \
               .order_by('year_id') \
               .all()

    def getTeamYears_byYear(self, year):
        return self.session.query(TeamYear) \
               .filter_by(year_id=year) \
               .order_by('team_id') \
               .all()

    '''Event'''

    def getEvent(self, event):
        '''Todo'''

    def getEvent_byKey(self, event):
        return self.session.query(Event) \
               .filter_by(key=event) \
               .first()

    def getEvents(self):
        '''Todo'''

    def getEvents_byYear(self, year):
        '''Todo'''

    '''Team Event'''

    def getTeamEvent(self, team, event):
        return self.session.query(TeamEvent) \
               .filter_by(team_id=team) \
               .filter_by(event_id=event) \
               .first()

    def getTeamEvents(self):
        '''Todo'''

    def getTeamEvents_byTeam(self, team):
        '''Todo'''

    '''Match'''

    def getMatch(self, match):
        '''Todo'''

    def getMatches(self):
        '''Todo'''

    def getMatches_byEvent(self, event):
        '''Todo'''

    '''Team Match'''

    def getTeamMatch(self, team, match):
        '''Todo'''

    def getTeamMatches(self):
        '''Todo'''

    def getTeamMatches_byMatch(self, match):
        '''Todo'''
