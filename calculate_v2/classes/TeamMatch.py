class TeamMatch:
    def __init__(self, TeamEvent, Match, dict):
        self.TeamEvent_p = TeamEvent
        self.Match_p = Match

        self.number = dict["num"]
        self.key = dict["key"]
        self.alliance = dict["alliance"]

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
