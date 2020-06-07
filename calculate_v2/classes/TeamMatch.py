class TeamMatch:
    number = -1
    key = ""

    TeamEvent_p = None  # points to Team Event parent
    Match_p = None  # points to Match parent

    def __init__(self, TeamEvent, Match):
        self.TeamEvent = TeamEvent
        self.Match = Match

        self.number = self.TeamEvent.getNumber()
        self.key = self.Match.getKey()

    def __lt__(self, other):
        if self.getNumber() == other.getNumber():
            return self.getKey() < other.getKey()
        else:
            return self.getNumber() < other.getNumber()

    def __repr__(self):
        return "(TeamMatch " + \
                str(self.getNumber()) + " " + \
                str(self.getKey()) + ")"

    def __str__(self):
        return self.__repr__()

    def getNumber(self):
        return self.number

    def getKey(self):
        return self.key

    def getParentTeamEvent(self):
        return self.TeamEvent_p

    def getParentMatch(self):
        return self.Match_p
