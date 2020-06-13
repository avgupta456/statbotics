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
        self.writes = 0
        self.commits = 0

        self.session = SQL.getSession()
        self.read = SQL_Read

    def add(self, obj, commit):
        self.session.add(obj)
        self.writes += 1
        if(commit):
            self.commit()
        return obj

    def commit(self):
        self.session.commit()
        self.commits += 1

    def getStats(self):
        return [self.writes, self.commits]

    def addTeam(self, dict, commit=False):
        team = Team(
            id=dict["number"],
            name=dict["name"],
            state=dict["state"],
            country=dict["country"],
        )

        return self.add(team, commit)

    def addYear(self, dict, commit=False):
        year = Year(
            id=dict["year"],
        )

        return self.add(year, commit)

    def addTeamYear(self, dict, commit=False):
        teamYear = TeamYear(
            year_id=dict["year"],
            team_id=dict["team"]
        )

        return self.add(teamYear, commit)

    def addEvent(self, dict, commit=False):
        event = Event(
            year_id=dict["year"],
            key=dict["key"],
            name=dict["name"],
            state=dict["state"],
            country=dict["country"],
            district=dict["district"],
        )

        return self.add(event, commit)

    def addTeamEvent(self, dict, commit=False):
        teamEvent = TeamEvent(
            team_id=dict["team"],
            team_year_id=self.read.getTeamYear_byParts(
                team=dict["team"], year=dict["year"]).getId(),
            year_id=dict["year"],
            event_id=dict["event"],
        )

        return self.add(teamEvent, commit)

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
        self.writes += 1

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

        return self.add(teamMatch, commit)
