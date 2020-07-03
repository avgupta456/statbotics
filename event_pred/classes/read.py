from sqlalchemy import desc

from event_pred.classes.classes import (
    Team,
    Year,
    TeamYear,
    Event,
    TeamEvent,
    Match,
    TeamMatch,
)


class SQL_Read:
    def __init__(self, SQL):
        self.reads = 0
        self.session = SQL.getSession()

    def getStats(self):
        return self.reads

    '''Team'''

    def getTeam(self, number):
        self.reads += 1
        return self.session.query(Team).filter_by(id=number).first()

    def getTeams(self):
        self.reads += 1
        return self.session.query(Team).order_by('id').all()

    def getTotalTeams(self):
        self.reads += 1
        return self.session.query(Team).count()

    '''Year'''

    def getYear(self, year):
        self.reads += 1
        return self.session.query(Year).filter_by(id=year).first()

    def getYears(self):
        self.reads += 1
        return self.session.query(Year).order_by('id').all()

    def getTotalYears(self):
        self.reads += 1
        return self.session.query(Year).count()

    '''Team Year'''

    def getTeamYear(self, teamYear):
        self.reads += 1
        return self.session.query(TeamYear).filter_by(id=teamYear).first()

    def getTeamYear_byParts(self, team, year):
        self.reads += 1
        return self.session.query(TeamYear) \
            .filter_by(team_id=team, year_id=year).first()

    def getTeamYearId_byParts(self, team, year):
        self.reads += 1
        return self.session.query(TeamYear.id) \
            .filter_by(team_id=team, year_id=year).first()[0]

    def getTeamYears(self, team=None, year=None, teamYear=None):
        self.reads += 1
        out = self.session.query(TeamYear)
        if team is not None:
            out = out.filter_by(team_id=team)
        if year is not None:
            out = out.filter_by(year_id=year)
        if teamYear is not None:
            out = out.filter_by(id=teamYear)
        return out.order_by('id').all()

    def getTotalTeamYears(self):
        self.reads += 1
        return self.session.query(TeamYear).count()

    def getLeaderboard(self, year):
        self.reads += 1
        return self.session.query(TeamYear) \
            .filter_by(year_id=year).order_by(desc(TeamYear.elo_max)).all()

    '''Event'''

    def getEvent(self, event):
        self.reads += 1
        return self.session.query(Event).filter_by(id=event).first()

    def getEvent_byKey(self, event_key):
        self.reads += 1
        return self.session.query(Event).filter_by(key=event_key).first()

    def getEvents_year(self, year):
        self.reads += 1
        return self.session.query(Event).filter_by(year_id=year) \
            .order_by('time').all()

    def getEventId_byKey(self, event_key):
        self.reads += 1
        return self.session.query(Event.id).filter_by(key=event_key).first()[0]

    def getEvents(self, year=None, week=None, event=None):
        self.reads += 1
        out = self.session.query(Event)
        if year is not None:
            out = out.filter_by(year_id=year)
        if week is not None:
            out = out.filter_by(week=week)
        if event is not None:
            out = out.filter_by(id=event)
        return out.order_by('id').all()

    def getTotalEvents(self):
        self.reads += 1
        return self.session.query(Event).count()

    '''Team Event'''

    def getTeamEvent(self, teamEvent):
        self.reads += 1
        return self.session.query(TeamEvent).filter_by(id=teamEvent).first()

    def getTeamEvent_byParts(self, team, event):
        self.reads += 1
        return self.session.query(TeamEvent) \
            .filter_by(team_id=team, event_id=event).first()

    def getTeamEventId_byParts(self, team, event):
        self.reads += 1
        return self.session.query(TeamEvent.id) \
            .filter_by(team_id=team, event_id=event).first()[0]

    def getTeamEvents(self, team=None, year=None,
                      teamYear=None, event=None, teamEvent=None):
        self.reads += 1
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

    def getTotalTeamEvents(self):
        self.reads += 1
        return self.session.query(TeamEvent).count()

    '''Match'''

    def getMatch(self, match):
        self.reads += 1
        return self.session.query(Match).filter_by(id=match).first()

    def getMatch_byKey(self, match_key):
        self.reads += 1
        return self.session.query(Match).filter_by(key=match_key).first()

    def getMatches_year(self, year):
        self.reads += 1
        return self.session.query(Match).filter_by(year_id=year) \
            .order_by('time').all()

    def getMatches(self, year=None, event=None, match=None, playoff=None):
        self.reads += 1
        out = self.session.query(Match)
        if year is not None:
            out = out.filter_by(year_id=year)
        if event is not None:
            out = out.filter_by(event_id=event)
        if match is not None:
            out = out.filter_by(id=match)
        if playoff is not None:
            out = out.filter_by(playoff=playoff)
        return out.order_by('id').all()

    def getTotalMatches(self):
        self.reads += 1
        return self.session.query(Match).count()

    '''Team Matches'''

    def getTeamMatch(self, team_match):
        self.reads += 1
        return self.session.query(TeamMatch).filter_by(id=team_match).first()

    def getTeamMatches(self, year=None, event=None,
                       match=None, playoff=None, team=None):
        self.reads += 1
        out = self.session.query(TeamMatch)
        if year is not None:
            out = out.filter_by(year_id=year)
        if event is not None:
            out = out.filter_by(event_id=event)
        if match is not None:
            out = out.filter_by(id=match)
        if playoff is not None:
            out = out.filter_by(playoff=playoff)
        if team is not None:
            out = out.filter_by(team_id=team)
        return out.order_by('id').all()

    def getTotalTeamMatches(self):
        self.reads += 1
        return self.session.query(TeamMatch).count()
