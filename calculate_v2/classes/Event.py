import classes.Match as Match
import classes.TeamMatch as TeamMatch


class Event:
    key = ""

    Year_p = None  # points to year parent
    TeamEvent_c = {}  # maps from team to TeamEvent children
    Match_c = {}  # maps from match key to Match children

    def __init__(self, Year, key):
        self.Year = Year
        self.key = key

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

    def addTeamEvent(self, team):
        self.getParentYear().addTeamEvent(self.getKey(), team)

    def setTeamEvent(self, team, teamEvent):
        self.TeamEvent_c[team] = teamEvent

    def getTeamEvent(self, team):
        return self.TeamEvent_c[team]

    def getTeamEvents(self):
        return self.TeamEvent_c

    def addMatch(self, match):
        self.Match_c[match] = Match.Match(self, match)

    def getMatch(self, match):
        return self.Match_c[match]

    def getMatches(self):
        return self.Match_c

    def addTeamMatch(self, team, match):
        Match = self.getMatch(match)
        TeamEvent = self.getTeamEvent(team)
        TeamMatch_temp = TeamMatch.TeamMatch(TeamEvent, Match)
        TeamEvent.setTeamMatch(match, TeamMatch_temp)
        Match.setTeamMatch(team, TeamMatch_temp)
