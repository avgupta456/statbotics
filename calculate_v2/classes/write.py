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

    def remove(self, obj, commit=False):
        self.session.delete(obj)
        if commit:
            self.commit()

    def commit(self):
        self.session.commit()
        self.commits += 1

    def getStats(self):
        return [self.writes, self.commits]

    '''Team'''

    def addTeam(self, dict, commit=False):
        if self.read.getTeam(dict["number"]) is None:
            team = Team(
                id=dict["number"],
                name=dict["name"],
                state=dict["state"],
                country=dict["country"],
            )
            self.add(team, commit)
            return False
        return True

    '''Year'''

    def addYear(self, dict, commit=False):
        if self.read.getYear(dict["year"]) is None:
            year = Year(
                id=dict["year"],
            )
            self.add(year, commit)
            return False
        return True

    '''TeamYear'''

    def addTeamYear(self, dict, commit=False):
        team, year = dict["team"], dict["year"]
        if self.read.getTeamYear_byParts(team, year) is None:
            teamYear = TeamYear(
                year_id=year,
                team_id=team
            )
            self.add(teamYear, commit)
            return False
        return True

    '''Event'''

    def addEvent(self, dict, commit=False):
        if self.read.getEvent_byKey(dict["key"]) is None:
            event = Event(
                year_id=dict["year"],
                key=dict["key"],
                name=dict["name"],
                state=dict["state"],
                country=dict["country"],
                district=dict["district"],
            )
            self.add(event, commit)
            return False
        return True

    '''TeamEvent'''

    def addTeamEvent(self, dict, commit=False):
        team, event_id = dict["team"], dict["event"]
        if self.read.getTeamEvent_byParts(team, event_id) is None:
            team_year_id = self.read.getTeamYear_byParts(
                team=dict["team"], year=dict["year"]).getId()
            teamEvent = TeamEvent(
                team_id=team,
                team_year_id=team_year_id,
                year_id=dict["year"],
                event_id=event_id,
            )
            self.add(teamEvent, commit)
            return False
        return True

    '''Match'''

    def addMatch(self, dict, commit=False):
        year_id = dict["year"]
        event_id = dict["event"]
        if self.read.getMatch_byKey(dict["key"]) is None:
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
            self.add(match, commit)
            for (color, list) in [
                ("red", match.getRed()),
                ("blue", match.getBlue())
            ]:
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
                        "alliance": color
                    }
                    self.addTeamMatch(teamMatchDict, False)
            return False
        return True

    '''TeamMatch'''

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
        self.add(teamMatch, commit)
