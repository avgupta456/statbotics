from classes.classes import (
    Team,
    Year,
    TeamYear,
    Event,
    TeamEvent,
    Match,
    TeamMatch,
)

from helper import utils


class SQL_Write:
    def __init__(self, SQL, SQL_Read):
        self.writes = 0
        self.commits = 0
        self.objects = []

        self.match_id = SQL_Read.getTotalMatches()
        self.event_id = SQL_Read.getTotalEvents()

        self.session = SQL.getSession()
        self.read = SQL_Read

    def add(self):
        if self.objects != []:
            self.session.add_all(self.objects)
            self.objects = []
            self.writes += 1
            self.commit()

    def flush(self):
        self.session.flush()
        self.commits += 1

    def commit(self):
        self.session.commit()
        self.commits += 1

    def remove(self, obj, commit=False):
        self.session.delete(obj)
        self.writes += 1
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
                id=int(str(year)+str(team)),
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
            district = dict["district"]
            if district is None:
                district = "None"
            self.event_id += 1
            event = Event(
                id=self.event_id,
                year_id=dict["year"],
                key=dict["key"],
                name=dict["name"],
                state=dict["state"],
                country=dict["country"],
                district=district,
                time=dict["time"],
                type=dict["type"],
                week=dict["week"],
            )
            self.objects.append(event)
            if add:
                self.add()
            if commit:
                self.commit()
            return True, self.event_id
        return False, self.event_id

    '''TeamEvent'''

    def addTeamEvent(self, dict, check=True, add=False, commit=False):
        team, event_id = dict["team"], dict["event_id"]
        if not check or self.read.getTeamEvent_byParts(team, event_id) is None:
            team_year_id = int(str(dict["year"])+str(dict["team"]))
            teamEvent = TeamEvent(
                id=int("1"+str(event_id).zfill(4)+str(team)),
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
                playoff=(dict["comp_level"] != "qm"),
                time=dict["time"],

                red_auto=dict["red_score_breakdown"]["auto"],
                red_auto_movement=dict["red_score_breakdown"]["auto_movement"],
                red_auto_1=dict["red_score_breakdown"]["auto_1"],
                red_auto_2=dict["red_score_breakdown"]["auto_2"],
                red_auto_2_1=dict["red_score_breakdown"]["auto_2_1"],
                red_auto_2_2=dict["red_score_breakdown"]["auto_2_2"],
                red_auto_2_3=dict["red_score_breakdown"]["auto_2_3"],
                red_teleop_1=dict["red_score_breakdown"]["teleop_1"],
                red_teleop_2=dict["red_score_breakdown"]["teleop_2"],
                red_teleop_2_1=dict["red_score_breakdown"]["teleop_2_1"],
                red_teleop_2_2=dict["red_score_breakdown"]["teleop_2_2"],
                red_teleop_2_3=dict["red_score_breakdown"]["teleop_2_3"],
                red_1=dict["red_score_breakdown"]["1"],
                red_2=dict["red_score_breakdown"]["2"],
                red_teleop=dict["red_score_breakdown"]["teleop"],
                red_endgame=dict["red_score_breakdown"]["endgame"],
                red_no_fouls=dict["red_score_breakdown"]["no_fouls"],
                red_fouls=dict["red_score_breakdown"]["fouls"],
                red_rp_1=dict["red_score_breakdown"]["rp1"],
                red_rp_2=dict["red_score_breakdown"]["rp2"],

                blue_auto=dict["blue_score_breakdown"]["auto"],
                blue_auto_movement=dict["blue_score_breakdown"]["auto_movement"],  # noqa: E501
                blue_auto_1=dict["blue_score_breakdown"]["auto_1"],
                blue_auto_2=dict["blue_score_breakdown"]["auto_2"],
                blue_auto_2_1=dict["blue_score_breakdown"]["auto_2_1"],
                blue_auto_2_2=dict["blue_score_breakdown"]["auto_2_2"],
                blue_auto_2_3=dict["blue_score_breakdown"]["auto_2_3"],
                blue_teleop_1=dict["blue_score_breakdown"]["teleop_1"],
                blue_teleop_2=dict["blue_score_breakdown"]["teleop_2"],
                blue_teleop_2_1=dict["blue_score_breakdown"]["teleop_2_1"],
                blue_teleop_2_2=dict["blue_score_breakdown"]["teleop_2_2"],
                blue_teleop_2_3=dict["blue_score_breakdown"]["teleop_2_3"],
                blue_1=dict["blue_score_breakdown"]["1"],
                blue_2=dict["blue_score_breakdown"]["2"],
                blue_teleop=dict["blue_score_breakdown"]["teleop"],
                blue_endgame=dict["blue_score_breakdown"]["endgame"],
                blue_no_fouls=dict["blue_score_breakdown"]["no_fouls"],
                blue_fouls=dict["blue_score_breakdown"]["fouls"],
                blue_rp_1=dict["blue_score_breakdown"]["rp1"],
                blue_rp_2=dict["blue_score_breakdown"]["rp2"],
            )
            self.objects.append(match)
            new_dict = {
                "year_id": year_id,
                "event_id": event_id,
                "match_id": self.match_id,
                "time": dict["time"]
            }
            for alliance in ["red", "blue"]:
                new_dict["alliance"] = alliance
                for team in dict[alliance].split(","):
                    team_year_id = utils.getTeamYearId(team, year_id)
                    team_event_id = utils.getTeamEventId(team, event_id)
                    new_dict["team_id"] = team
                    new_dict["team_year_id"] = team_year_id
                    new_dict["team_event_id"] = team_event_id
                    self.addTeamMatch(new_dict,
                                      check=check,
                                      add=add,
                                      commit=commit)
            if add:
                self.add()
            if commit:
                self.commit()
            return True
        return False

    '''Team Match'''

    def addTeamMatch(self, dict, check=True, add=False, commit=False):
        if not check or self.read.getTeamMatch(dict["id"]) is None:
            team_match = TeamMatch(
                team_id=dict["team_id"],
                team_year_id=dict["team_year_id"],
                team_event_id=dict["team_event_id"],
                year_id=dict["year_id"],
                event_id=dict["event_id"],
                match_id=dict["match_id"],
                time=dict["time"],
                alliance=dict["alliance"]
            )
            self.objects.append(team_match)
            if add:
                self.add()
            if commit:
                self.commit()
            return True
        return False
