class Match:
    key = ""

    Event_p = None  # points to Event parent
    TeamMatch_c = {}  # maps from position to TeamMatch children

    def __init__(self, Event, key):
        self.Event_p = Event
        self.key = key

    def __lt__(self, other):
        return self.getKey() < other.getKey()

    def __repr__(self):
        return "(Match " + str(self.getKey()) + ")"

    def __str__(self):
        return self.__repr__()

    def getKey(self):
        return self.key

    def getParentEvent(self):
        return self.Event_p

    def addTeamMatch(self, team):
        self.getParentEvent().addTeamMatch_fromMatch(self, team)

    def setTeamMatch(self, team, TeamMatch):
        self.TeamMatch_c[team] = TeamMatch

    def getTeamMatch(self, team):
        return self.TeamMatch_c[team]

    def getTeamMatches(self):
        return self.TeamMatch_c
