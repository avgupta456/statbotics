class TeamEvent:
    def __init__(self, TeamYear, Event, dict):
        self.TeamYear_p = TeamYear
        self.Event_p = Event
        self.TeamMatch_c = {}

        self.number = self.TeamYear_p.getNumber()
        self.key = self.Event_p.getKey()

    def __lt__(self, other):
        if self.getNumber() == other.getNumber():
            return self.getKey() < other.getKey()
        else:
            return self.getNumber() < other.getNumber()

    def __repr__(self):
        return "(TeamEvent " + \
                str(self.getNumber()) + " " + \
                str(self.getKey()) + ")"

    def __str__(self):
        return self.__repr__()

    def getNumber(self):
        return self.number

    def getKey(self):
        return self.key

    def getParentTeamYear(self):
        return self.TeamYear_p

    def getParentEvent(self):
        return self.Event_p

    def addTeamMatch(self, match):
        self.getParentEvent().addTeamMatch(self.getKey(), match)

    def setTeamMatch(self, match, TeamMatch):
        self.TeamMatch_c[match] = TeamMatch

    def getTeamMatch(self, match):
        return self.TeamMatch_c[match]

    def getTeamMatches(self):
        return self.TeamMatch_c
