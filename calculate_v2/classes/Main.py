import Team
import Year
import TeamYear


class Main:
    Team_c = {}  # dict from team num to Team object children
    Year_c = {}  # dict from year to Year object children

    def __init__(self):
        return

    def addTeam(self, num):
        self.Team_c[num] = Team(self, num)

    def getTeam(self, num):
        return self.Team_c[num]

    def addYear(self, year):
        self.Year_c[year] = Year(self, year)

    def getYear(self, year):
        return self.Year_C[year]

    def addTeamYear_fromTeam(self, Team, year):
        Year = self.getYear(year)
        TeamYear_temp = TeamYear(Team, Year)
        Team.setTeamYear(year, TeamYear_temp)

    def addTeamYear_fromYear(self, Year, team):
        Team = self.getTeam(team)
        TeamYear_temp = TeamYear(Team, Year)
        Year.setTeamYear(team, TeamYear_temp)
