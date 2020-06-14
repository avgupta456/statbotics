from classes.classes import (
    Team,
    Year,
    TeamYear,
    Event,
    TeamEvent,
    Match,
    team_match_table,
    teamYear_match_table,
    teamEvent_match_table,
)


class SQL_Write:
    def __init__(self, SQL, SQL_Read):
        self.writes = 0
        self.commits = 0
        self.objects = []
        self.match_objects = []

        self.match_id = 0

        self.session = SQL.getSession()
        self.read = SQL_Read

    def add(self):
        if self.objects != []:
            self.session.add_all(self.objects)
            self.objects = []
            self.writes += 1
            self.commit()

        if self.match_objects != []:
            self.session.execute(team_match_table.insert().
                                 values(self.match_objects))
            self.session.execute(teamYear_match_table.insert().
                                 values(self.match_objects))
            self.session.execute(teamEvent_match_table.insert().
                                 values(self.match_objects))
            self.match_objects = []
            self.writes += 3
            self.commit()

    def flush(self):
        self.session.flush()
        self.commits += 1

    def commit(self):
        if len(self.objects) > 0 or len(self.match_objects) > 0:
            self.add()
        self.session.commit()
        self.commits += 1

    def remove(self, obj, commit=False):
        self.session.delete(obj)
        if commit:
            self.commit()

    def getStats(self):
        return [self.writes, self.commits]

    '''Team'''

    def addTeam(self, dict, check=True, add=False, commit=False):
        if not check or self.read.getTeam(dict["number"]) is None:
            team = Team(
                id=dict["number"],
                name=dict["name"],
                state=dict["state"],
                country=dict["country"],
            )
            self.objects.append(team)
            if add:
                self.add()
            if commit:
                self.commit()
            return True
        return False

    '''Year'''

    def addYear(self, dict, check=True, add=False, commit=False):
        if not check or self.read.getYear(dict["year"]) is None:
            year = Year(
                id=dict["year"],
            )
            self.objects.append(year)
            if add:
                self.add()
            if commit:
                self.commit()
            return True
        return False

    '''TeamYear'''

    def addTeamYear(self, dict, check=True, add=False, commit=False):
        team, year = dict["team"], dict["year"]
        if not check or self.read.getTeamYear_byParts(team, year) is None:
            teamYear = TeamYear(
                year_id=year,
                team_id=team
            )
            self.objects.append(teamYear)
            if add:
                self.add()
            if commit:
                self.commit()
            return True
        return False

    '''Event'''

    def addEvent(self, dict, check=True, add=False, commit=False):
        if not check or self.read.getEvent_byKey(dict["key"]) is None:
            event = Event(
                year_id=dict["year"],
                key=dict["key"],
                name=dict["name"],
                state=dict["state"],
                country=dict["country"],
                district=dict["district"],
                time=dict["time"],
            )
            self.objects.append(event)
            if add:
                self.add()
            if commit:
                self.commit()
            return True
        return False

    '''TeamEvent'''

    def addTeamEvent(self, dict, check=True, add=False, commit=False):
        team, event_id = dict["team"], dict["event_id"]
        if not check or self.read.getTeamEvent_byParts(team, event_id) is None:
            team_year_id = self.read.getTeamYear_byParts(
                team=dict["team"], year=dict["year"]
            ).getId()
            teamEvent = TeamEvent(
                team_id=team,
                team_year_id=team_year_id,
                year_id=dict["year"],
                event_id=event_id,
                time=dict["time"],
            )
            self.objects.append(teamEvent)
            if add:
                self.add()
            if commit:
                self.commit()
            return True
        return False

    '''Match'''

    def addMatch(self, dict, check=True, add=False, commit=False):
        year_id = dict["year"]
        event_id = dict["event"]
        if not check or self.read.getMatch_byKey(dict["key"]) is None:
            self.match_id += 1
            match = Match(
                id=self.match_id,
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
            self.objects.append(match)
            arr = []
            for team in dict["red"].split(","):
                arr.append((int(team), self.match_id))
            for team in dict["blue"].split(","):
                arr.append((int(team), self.match_id))
            self.match_objects.extend(arr)
            if add:
                self.add()
            if commit:
                self.commit()
            return True
        return False
