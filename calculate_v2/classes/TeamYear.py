class TeamYear:
    number = -1
    year = -1

    Team_p = None  # points to Team parent
    Year_p = None  # poitns to Year parent
    TeamEvent_c = {}  # maps from event key to TeamEvent children

    def __init__(self, Team, Year):
        self.Team_p = Team
        self.Year_p = Year

        self.number = self.Team_p.getNumber()
        self.year = self.Year_p.getYear()

    def __lt__(self, other):
        if self.getNumber() == other.getNumber():
            return self.getYear() < other.getYear()
        else:
            return self.getNumber() < other.getNumber()

    def __repr__(self):
        return "TeamYear " + str(self.getNumber()) + "\t" + str(self.getYear())

    def __str__(self):
        return self.__repr__()

    def getParentTeam(self):
        return self.Team_p

    def getParentYear(self):
        return self.Year_p

    def getNumber(self):
        return self.number

    def getYear(self):
        return self.year
