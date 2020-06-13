from classes.classes import (
    Team,
    Year,
    TeamYear,
    Event,
    TeamEvent,
    Match,
    TeamMatch
)


class SQL_Write:
    def __init__(self, SQL, SQL_Read):
        self.session = SQL.getSession()
        self.read = SQL_Read

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

    def addEvent(self, dict, commit=False):
        event = Event(
            year_id=dict["year"],
            key=dict["key"],
            name=dict["name"],
            state=dict["state"],
            country=dict["country"],
            district=dict["district"],
        )

        self.session.add(event)
        if commit:
            self.commit()

    def addTeamEvent(self, dict, commit=False):
        teamEvent = TeamEvent(
            year_id=dict["year"],
            event=self.read.getEvent_byKey(dict["event"]),
            team_id=dict["team"],
        )

        self.session.add(teamEvent)
        if commit:
            self.commit()

    def addMatch(self, dict, commit=False):
        match = Match(
            year_id=dict["year"],
            event=self.read.getEvent_byKey(dict["event"]),
            key=dict["key"],
            comp_level=dict["comp_level"],
            set_number=dict["set_number"],
            match_number=dict["match_number"],
            red=dict["red"],
            blue=dict["blue"],
            winner=dict["winner"],
        )

        self.session.add(match)

        for (alliance, list) in [("red", match.red), ("blue", match.blue)]:
            for team in list:
                teamMatchDict = {
                    "match": match,
                    "team_event": self.read.getTeamEvent(team, dict["event"]),
                    "alliance": alliance
                }
                self.addTeamMatch(teamMatchDict, False)

        if commit:
            self.commit()

    def addTeamMatch(self, dict, commit=False):
        teamMatch = TeamMatch(
            match=dict["match"],
            team_event=dict["team_event"],
            alliance=dict["alliance"]
        )

        self.session.add(teamMatch)
        if commit:
            self.commit()

    def commit(self):
        self.session.commit()
