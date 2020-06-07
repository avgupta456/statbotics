class Match:
    def __init__(self, Event, key):
        self.Event_p = Event
        self.TeamMatch_c = {}
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
        self.getParentEvent().addTeamMatch(team, self.getKey())

    def setTeamMatch(self, team, TeamMatch):
        self.TeamMatch_c[team] = TeamMatch

    def getTeamMatch(self, team):
        return self.TeamMatch_c[team]

    def getTeamMatches(self):
        return self.TeamMatch_c
