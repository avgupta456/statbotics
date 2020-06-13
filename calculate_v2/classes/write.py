from classes.classes import (
    Team,
    Year,
    TeamYear,
    # Event,
    # TeamEvent,
    # Match,
    # TeamMatch
)


class SQL_Write:
    def __init__(self, SQL):
        self.session = SQL.getSession()

    def addTeam(self, dict, commit=False):
        team = Team(
            name=dict["name"],
            number=dict["number"],
            state=dict["state"],
            country=dict["country"],
        )

        self.session.add(team)
        if commit:
            self.commit()

    def addYear(self, dict, commit=False):
        year = Year(
            year=dict["year"],
        )

        self.session.add(year)
        if commit:
            self.commit()

    def addTeamYear(self, dict, commit=False):
        teamYear = TeamYear(
            year_id=dict["year"],
            team_id=dict["team"]
        )

        self.session.add(teamYear)
        if commit:
            self.commit()

    def commit(self):
        self.session.commit()
