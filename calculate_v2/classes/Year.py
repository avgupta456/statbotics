import classes.Event as Event
import classes.TeamEvent as TeamEvent


class Year:
    year = -1  # numeric year, ex: 2019

    Main_p = None  # points to Main parent
    TeamYear_c = {}  # maps from team to TeamYear object children
    Event_c = {}  # maps from event key to Event object children

    def __init__(self, Main, year):
        self.Main_p = Main
        self.year = year

    def __lt__(self, other):
        return self.getYear() < other.getYear()

    def __repr__(self):
        return "Year " + str(self.getYear())

    def __str__(self):
        return self.__repr__()

    def getYear(self):
        return self.year

    def getParentMain(self):
        return self.Main_p

    def addTeamYear(self, team):
        self.getParentMain().addTeamYear_fromYear(self, team)

    def setTeamYear(self, team, TeamYear):
        self.TeamYear_c[team] = TeamYear

    def getTeamYear(self, team):
        return self.TeamYear_c[team]

    def addEvent(self, event):
        self.Event_c[event] = Event.Event(self, event)

    def getEvent(self, event):
        return self.Event_c[event]

    def addTeamEvent_fromTeamYear(self, TeamYear, event):
        Event = self.getEvent(event)
        TeamEvent_temp = TeamEvent.TeamEvent(TeamYear, Event)
        TeamYear.setTeamEvent(event, TeamEvent_temp)

    def addTeamEvent_fromEvent(self, Event, team):
        Team = self.getTeam(team)
        TeamEvent_temp = TeamEvent.TeamEvent(Team, Event)
        Year.setTeamEvent(team, TeamEvent_temp)
