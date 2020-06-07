class Team:
    number = -1
    name = ""
    state = ""
    country = ""

    Main_p = None  # points to Main object
    TeamYear_c = {}  # maps from year to TeamYear children

    def __init__(self, Main, dict):
        self.Main_p = Main

        self.number = int(dict["num"])
        self.name = dict["name"]
        self.state = dict["state"]
        self.country = dict["country"]

    def __lt__(self, other):
        return self.getNumber() < other.getNumber()

    def __repr__(self):
        return "(Team " + str(self.getNumber()) + ": " + str(self.name) + ")"

    def __str__(self):
        return self.__repr__()

    def getNumber(self):
        return self.number

    def getParentMain(self):
        return self.Main_p

    def addTeamYear(self, dict):
        self.getParentMain().addTeamYear(self.getNumber(), dict["year"], dict)

    def setTeamYear(self, year, TeamYear):
        self.TeamYear_c[year] = TeamYear

    def getTeamYear(self, year):
        return self.TeamYear_c[year]

    def getTeamYears(self):
        return self.TeamYear_c

    def getName(self):
        return self.name

    def getState(self):
        return self.state

    def getCountry(self):
        return self.country
