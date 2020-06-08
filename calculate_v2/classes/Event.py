import classes.TeamMatch as TeamMatch
import classes.Match as Match


class Event:
    def __init__(self, Year, dict):
        self.Year_p = Year
        self.TeamEvent_c = {}
        self.Match_c = {}

        self.key = dict["key"]
        self.name = dict["name"]
        self.state = dict["state"]
        self.country = dict["country"]
        self.district = dict["district"]
        self.start_date = dict["start_date"]
        self.end_date = dict["end_date"]

    def __lt__(self, other):
        return self.getKey() < other.getKey()

    def __repr__(self):
        return "(Event " + str(self.getKey()) + ")"

    def __str__(self):
        return self.__repr__()

    def getKey(self):
        return self.key

    def getParentYear(self):
        return self.Year_p

    def addTeamEvent(self, dict):
        self.getParentYear().addTeamEvent(dict["num"], self.getKey(), dict)

    def setTeamEvent(self, team, teamEvent):
        self.TeamEvent_c[team] = teamEvent

    def getTeamEvent(self, team):
        return self.TeamEvent_c[team]

    def getTeamEvents(self):
        return self.TeamEvent_c

    def addMatch(self, dict):
        self.Match_c[dict["key"]] = Match.Match(self, dict)

    def getMatch(self, match):
        return self.Match_c[match]

    def getMatches(self):
        return self.Match_c

    def addTeamMatch(self, team, match, dict):
        Match = self.getMatch(match)
        TeamEvent = self.getTeamEvent(team)
        TeamMatch_temp = TeamMatch.TeamMatch(TeamEvent, Match, dict)
        TeamEvent.setTeamMatch(match, TeamMatch_temp)
        Match.setTeamMatch(team, TeamMatch_temp)

    def getName(self):
        return self.name

    def getState(self):
        return self.state

    def getCountry(self):
        return self.country

    def getDistrict(self):
        return self.district

    def getStartDate(self):
        return self.start_date

    def getEndDate(self):
        return self.end_date
