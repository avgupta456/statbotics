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
        self.flushes = 0
        self.commits = 0

        self.session = SQL.getSession()
        self.read = SQL_Read

    def add(self, obj, commit):
        if not type(obj) is list:
            obj = [obj]
        self.session.add_all(obj)
        self.writes += 1
        if(commit):
            self.commit()

    def remove(self, obj, commit=False):
        self.session.delete(obj)
        if commit:
            self.commit()

    def flush(self):
        self.flushes += 1
        self.session.flush()

    def commit(self):
        self.session.commit()
        self.commits += 1

    def getStats(self):
        return [self.writes, self.flushes, self.commits]

    '''Team'''

    def addTeam(self, dict, add=False, commit=False):
        if self.read.getTeam(dict["number"]) is None:
            team = Team(
                id=dict["number"],
                name=dict["name"],
                state=dict["state"],
                country=dict["country"],
            )
            if add:
                self.add(team, commit)
            return team
        return None

    '''Year'''

    def addYear(self, dict, add=False, commit=False):
        if self.read.getYear(dict["year"]) is None:
            year = Year(
                id=dict["year"],
            )
            if add:
                self.add(year, commit)
            return year
        return None

    '''TeamYear'''

    def addTeamYear(self, dict, add=False, commit=False):
        team, year = dict["team"], dict["year"]
        if self.read.getTeamYear_byParts(team, year) is None:
            teamYear = TeamYear(
                year_id=year,
                team_id=team
            )
            if add:
                self.add(teamYear, commit)
            return teamYear
        return None

    '''Event'''

    def addEvent(self, dict, add=False, commit=False):
        if self.read.getEvent_byKey(dict["key"]) is None:
            event = Event(
                year_id=dict["year"],
                key=dict["key"],
                name=dict["name"],
                state=dict["state"],
                country=dict["country"],
                district=dict["district"],
                time=dict["time"],
            )
            if add:
                self.add(event, commit)
            return event
        return None

    '''TeamEvent'''

    def addTeamEvent(self, dict, add=False, commit=False):
        team, event_id = dict["team"], dict["event_id"]
        if self.read.getTeamEvent_byParts(team, event_id) is None:
            team_year_id = self.read.getTeamYear_byParts(
                team=dict["team"], year=dict["year"]).getId()
            teamEvent = TeamEvent(
                team_id=team,
                team_year_id=team_year_id,
                year_id=dict["year"],
                event_id=event_id,
                time=dict["time"],
            )
            if add:
                self.add(teamEvent, commit)
            return teamEvent
        return None

    '''Match'''

    def addMatch(self, dict, add=False, commit=False):
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
                red_score=dict["red_score"],
                blue_score=dict["blue_score"],
                winner=dict["winner"],
                time=dict["time"]
            )
            if add:
                self.add(match, commit)

            teamMatches = []
            for (color, arr) in [
                ("red", match.getRed()),
                ("blue", match.getBlue())
            ]:
                for team in arr:
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
                        "alliance": color,
                        "time": dict["time"],
                    }
                    teamMatches.append(
                        self.addTeamMatch(teamMatchDict, add, False)
                    )

            return match, teamMatches
        return None

    '''TeamMatch'''

    def addTeamMatch(self, dict, add=False, commit=False):
        teamMatch = TeamMatch(
            year_id=dict["year"],
            event_id=dict["event"],
            match_id=dict["match"],
            team_id=dict["team"],
            team_year_id=dict["team_year"],
            team_event_id=dict["team_event"],
            alliance=dict["alliance"],
            time=dict["time"],
        )
        if add:
            self.add(teamMatch, commit)
        return teamMatch
