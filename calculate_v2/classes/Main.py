import classes.Team as Team
import classes.Year as Year
import classes.TeamYear as TeamYear


class Main:
    def __init__(self):
        self.Team_c = {}
        self.Year_c = {}

    def addTeam(self, dict):
        self.Team_c[dict["num"]] = Team.Team(self, dict)

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

    def addTeamYear(self, team, year, dict):
        Year = self.getYear(year)
        Team = self.getTeam(team)
        TeamYear_temp = TeamYear.TeamYear(Team, Year, dict)
        Team.setTeamYear(year, TeamYear_temp)
        Year.setTeamYear(team, TeamYear_temp)
