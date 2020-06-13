from classes.classes import (
    Team,
    # Year,
    # TeamYear,
    # Event,
    # TeamEvent,
    # Match,
    # TeamMatch
)


class SQL_Write:
    def __init__(self, SQL):
        self.session = SQL.getSession()

    def addTeam(self, dict, commit=True):
        team = Team(
            name=dict["name"],
            number=dict["number"],
            state=dict["state"],
            country=dict["country"],
        )

        self.session.add(team)
        if commit:
            self.session.commit()

    def commit(self):
        self.session.commit()
