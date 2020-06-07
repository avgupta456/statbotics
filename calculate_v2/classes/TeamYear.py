class TeamYear:
    def __init__(self, Team, Year, dict):
        self.Team_p = Team
        self.Year_p = Year
        self.TeamEvent_c = {}

        self.number = self.Team_p.getNumber()
        self.year = self.Year_p.getYear()

    def __lt__(self, other):
        if self.getNumber() == other.getNumber():
            return self.getYear() < other.getYear()
        else:
            return self.getNumber() < other.getNumber()

    def __repr__(self):
        return "(TeamYear " + \
                str(self.getNumber()) + " " + \
                str(self.getYear()) + ")"

    def __str__(self):
        return self.__repr__()

    def getNumber(self):
        return self.number

    def getYear(self):
        return self.year

    def getParentTeam(self):
        return self.Team_p

    def getParentYear(self):
        return self.Year_p

    def addTeamEvent(self, dict):
        self.getParentYear().addTeamEvent(self.getNumber(), dict["key"], dict)

    def setTeamEvent(self, event, TeamEvent):
        self.TeamEvent_c[event] = TeamEvent

    def getTeamEvent(self, event):
        return self.TeamEvent_c[event]

    def getTeamEvents(self):
        return self.TeamEvent_c
