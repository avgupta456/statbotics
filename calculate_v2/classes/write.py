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
            id=dict["number"],
            name=dict["name"],
            state=dict["state"],
            country=dict["country"],
        )

        self.session.add(team)
        if commit:
            self.commit()

        return team

    def addYear(self, dict, commit=False):
        year = Year(
            id=dict["year"],
        )

        self.session.add(year)
        if commit:
            self.commit()

        return year

    def addTeamYear(self, dict, commit=False):
        teamYear = TeamYear(
            year_id=dict["year"],
            team_id=dict["team"]
        )

        self.session.add(teamYear)
        if commit:
            self.commit()

        return teamYear

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

        return event

    def addTeamEvent(self, dict, commit=False):
        teamEvent = TeamEvent(
            team_id=dict["team"],
            team_year_id=self.read.getTeamYear_byParts(
                team=dict["team"], year=dict["year"]).getId(),
            year_id=dict["year"],
            event_id=dict["event"],
        )

        self.session.add(teamEvent)
        if commit:
            self.commit()

        return teamEvent

    def addMatch(self, dict, commit=False):
        year_id = dict["year"]
        event_id = dict["event"]

        match = Match(
            year_id=year_id,
            event_id=event_id,
            key=dict["key"],
            comp_level=dict["comp_level"],
            set_number=dict["set_number"],
            match_number=dict["match_number"],
            red=dict["red"],
            blue=dict["blue"],
            winner=dict["winner"],
        )

        self.session.add(match)

        for (alliance, list) in [("red", match.getRed()),
                                 ("blue", match.getBlue())]:
            for team in list:
                team_event = self.read. \
                    getTeamEvent_byParts(team, event_id).getId()
                team_year = self.read. \
                    getTeamYear_byParts(team, year_id).getId()

                teamMatchDict = {
                    "year": year_id,
                    "event": event_id,
                    "match": match.getId(),
                    "team": team,
                    "team_year": team_year,
                    "team_event": team_event,
                    "alliance": alliance
                }

                self.addTeamMatch(teamMatchDict, False)

        if commit:
            self.commit()

        return match

    def addTeamMatch(self, dict, commit=False):
        teamMatch = TeamMatch(
            year_id=dict["year"],
            event_id=dict["event"],
            match_id=dict["match"],
            team_id=dict["team"],
            team_year_id=dict["team_year"],
            team_event_id=dict["team_event"],
            alliance=dict["alliance"]
        )

        self.session.add(teamMatch)
        if commit:
            self.commit()

        return teamMatch

    def commit(self):
        self.session.commit()
