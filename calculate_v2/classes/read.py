from classes.classes import (
    Team,
    Year,
    TeamYear,
    Event,
    TeamEvent,
    Match,
    TeamMatch
)


class SQL_Read:
    def __init__(self, SQL):
        self.session = SQL.getSession()

    '''Team'''

    def getTeam(self, number):
        return self.session.query(Team).filter_by(id=number).first()

    def getTeams(self):
        return self.session.query(Team).order_by('id').all()

    '''Year'''

    def getYear(self, year):
        return self.session.query(Year).filter_by(id=year).first()

    def getYears(self):
        return self.session.query(Year).order_by('id').all()

    '''Team Year'''

    def getTeamYear(self, teamYear):
        return self.session.query(TeamYear).filter_by(id=teamYear).first()

    def getTeamYear_byParts(self, team, year):
        return self.session.query(TeamYear) \
            .filter_by(team_id=team, year_id=year).first()

    def getTeamYears(self, team=None, year=None, teamYear=None):
        out = self.session.query(TeamYear)
        if team is not None:
            out = out.filter_by(team_id=team)
        if year is not None:
            out = out.filter_by(year_id=year)
        if teamYear is not None:
            out = out.filter_by(id=teamYear)
        return out.order_by('id').all()

    '''Event'''

    def getEvent(self, event):
        return self.session.query(Event).filter_by(id=event).first()

    def getEvent_byKey(self, event_key):
        return self.session.query(Event).filter_by(key=event_key).first()

    def getEvents(self, year=None, event=None):
        out = self.session.query(Event)
        if year is not None:
            out = out.filter_by(year_id=year)
        if event is not None:
            out = out.filter_by(id=event)
        return out.order_by('id').all()

    '''Team Event'''

    def getTeamEvent(self, teamEvent):
        return self.session.query(TeamEvent).filter_by(id=teamEvent).first()

    def getTeamEvent_byParts(self, team, event):
        return self.session.query(TeamEvent) \
            .filter_by(team_id=team, event_id=event).first()

    def getTeamEvents(self, team=None, year=None,
                      teamYear=None, event=None, teamEvent=None):
        out = self.session.query(TeamEvent)
        if team is not None:
            out = out.filter_by(team_id=team)
        if year is not None:
            out = out.filter_by(year_id=year)
        if teamYear is not None:
            out = out.filter_by(team_year_id=teamYear)
        if event is not None:
            out = out.filter_by(event_id=event)
        if teamEvent is not None:
            out = out.filter_by(id=teamEvent)
        return out.order_by('id').all()

    '''Match'''

    def getMatch(self, match):
        return self.session.query(Match).filter_by(id=match).first()

    def getMatches(self, year=None, event=None, match=None):
        out = self.session.query(Event)
        if year is not None:
            out = out.filter_by(year_id=year)
        if event is not None:
            out = out.filter_by(event_id=event)
        if match is not None:
            out = out.filter_by(id=match)
        return out.order_by('id').all()

    '''Team Match'''

    def getTeamMatch(self, teamMatch):
        return self.session.query(TeamMatch).filter_by(id=teamMatch).first()

    def getTeamMatches(self, team=None, year=None, teamYear=None, event=None,
                       teamEvent=None, match=None, teamMatch=None):
        out = self.session.query(TeamEvent)
        if team is not None:
            out = out.filter_by(team_id=team)
        if year is not None:
            out = out.filter_by(year_id=year)
        if teamYear is not None:
            out = out.filter_by(team_year_id=teamYear)
        if event is not None:
            out = out.filter_by(event_id=event)
        if teamEvent is not None:
            out = out.filter_by(team_event_id=teamEvent)
        if match is not None:
            out = out.filter_by(match_id=match)
        if teamMatch is not None:
            out = out.filter_by(id=teamMatch)
        return out.order_by('id').all()
