class Team:
    number = -1

    Main_p = None  # points to Main object
    TeamYear_c = {}  # maps from year to TeamYear children

    def __init__(self, Main, num):
        self.Main_p = Main
        self.number = num

    def __lt__(self, other):
        return self.get_number() > other.getNumber()

    def __repr__(self):
        return "Team " + str(self.getNumber())

    def __str__(self):
        return self.__repr__()

    def getNumber(self):
        return self.number

    def getMain(self):
        return self.Main_p

    def addTeamYear(self, year):
        self.getMain().addTeamYear_fromTeam(self, year)

    def setTeamYear(self, year, TeamYear):
        self.TeamYear_c[year] = TeamYear

    def getTeamYear(self, year):
        return self.TeamYear_c[year]
