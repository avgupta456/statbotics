import classes.Team as Team
import classes.Year as Year
import classes.TeamYear as TeamYear


class Main:
    Team_c = {}  # dict from team num to Team object children
    Year_c = {}  # dict from year to Year object children

    def __init__(self):
        return

    def addTeam(self, num):
        self.Team_c[num] = Team.Team(self, num)

    def getTeam(self, num):
        return self.Team_c[num]

    def getTeams(self):
        return self.Team_c

    def addYear(self, year):
        self.Year_c[year] = Year.Year(self, year)

    def getYear(self, year):
        return self.Year_c[year]

    def getYears(self):
        return self.Year_c

    def addTeamYear_fromTeam(self, Team, year):
        Year = self.getYear(year)
        TeamYear_temp = TeamYear.TeamYear(Team, Year)
        Team.setTeamYear(year, TeamYear_temp)
        team = Team.getNumber()
        Year.setTeamYear(team, TeamYear_temp)

    def addTeamYear_fromYear(self, Year, team):
        Team = self.getTeam(team)
        TeamYear_temp = TeamYear.TeamYear(Team, Year)
        Year.setTeamYear(team, TeamYear_temp)
        year = Year.getYear()
        Team.setTeamYear(year, TeamYear_temp)
