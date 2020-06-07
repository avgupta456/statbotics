import classes.Event as Event
import classes.TeamEvent as TeamEvent


class Year:
    def __init__(self, Main, dict):
        self.Main_p = Main
        self.TeamYear_c = {}
        self.Event_c = {}

        self.year = dict["year"]

    def __lt__(self, other):
        return self.getYear() < other.getYear()

    def __repr__(self):
        return "(Year " + str(self.getYear()) + ")"

    def __str__(self):
        return self.__repr__()

    def getYear(self):
        return self.year

    def getParentMain(self):
        return self.Main_p

    def addTeamYear(self, dict):
        self.getParentMain().addTeamYear(dict["num"], self.getYear(), dict)

    def setTeamYear(self, team, TeamYear):
        self.TeamYear_c[team] = TeamYear

    def getTeamYear(self, team):
        return self.TeamYear_c[team]

    def getTeamYears(self):
        return self.TeamYear_c

    def addEvent(self, dict):
        self.Event_c[dict["key"]] = Event.Event(self, dict)

    def getEvent(self, event):
        return self.Event_c[event]

    def getEvents(self):
        return self.Event_c

    def addTeamEvent(self, team, event, dict):
        TeamYear = self.getTeamYear(team)
        Event = self.getEvent(event)
        TeamEvent_temp = TeamEvent.TeamEvent(TeamYear, Event, dict)
        TeamYear.setTeamEvent(event, TeamEvent_temp)
        Event.setTeamEvent(team, TeamEvent_temp)
