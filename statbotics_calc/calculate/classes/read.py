from classes.classes import Event, Match, Team, TeamEvent, TeamMatch, TeamYear, Year
from sqlalchemy import desc


class SQL_Read:
    def __init__(self, SQL):
        self.reads = 0
        self.session = SQL.getLocalSession()

    def getStats(self):
        return self.reads

    """Team"""

    def getTeam(self, number):
        self.reads += 1
        return self.session.query(Team).filter_by(id=number).first()

    def getTeams(self):
        self.reads += 1
        return self.session.query(Team).order_by("id").all()

    def getTotalTeams(self):
        self.reads += 1
        return self.session.query(Team).count()

    """Year"""

    def getYear(self, year):
        self.reads += 1
        return self.session.query(Year).filter_by(id=year).first()

    def getYears(self):
        self.reads += 1
        return self.session.query(Year).order_by("id").all()

    def getTotalYears(self):
        self.reads += 1
        return self.session.query(Year).count()

    """Team Year"""

    def getTeamYear(self, teamYear):
        self.reads += 1
        return self.session.query(TeamYear).filter_by(id=teamYear).first()

    def getTeamYear_byParts(self, team, year):
        self.reads += 1
        return (
            self.session.query(TeamYear).filter_by(team_id=team, year_id=year).first()
        )

    def getTeamYearId_byParts(self, team, year):
        self.reads += 1
        return (
            self.session.query(TeamYear.id)
            .filter_by(team_id=team, year_id=year)
            .first()[0]
        )

    def getTeamYears(self, team=None, year=None, teamYear=None):
        self.reads += 1
        out = self.session.query(TeamYear)
        if team is not None:
            out = out.filter_by(team_id=team)
        if year is not None:
            out = out.filter_by(year_id=year)
        if teamYear is not None:
            out = out.filter_by(id=teamYear)
        return out.order_by("id").all()

    def getTotalTeamYears(self):
        self.reads += 1
        return self.session.query(TeamYear).count()

    def getLeaderboard(self, year):
        self.reads += 1
        return (
            self.session.query(TeamYear)
            .filter_by(year_id=year)
            .order_by(desc(TeamYear.elo_max))
            .all()
        )

    """Event"""

    def getEvent(self, event):
        self.reads += 1
        return self.session.query(Event).filter_by(id=event).first()

    def getEvent_byKey(self, event_key):
        self.reads += 1
        return self.session.query(Event).filter_by(key=event_key).first()

    def getEvents_year(self, year):
        self.reads += 1
        return self.session.query(Event).filter_by(year_id=year).order_by("time").all()

    def getEventId_byKey(self, event_key):
        self.reads += 1
        return self.session.query(Event.id).filter_by(key=event_key).first()[0]

    def getEvents(self, year=None, week=None, event=None):
        self.reads += 1
        out = self.session.query(Event)
        if year is not None:
            out = out.filter_by(year_id=year)
        if week is not None:
            out = out.filter_by(week=week)
        if event is not None:
            out = out.filter_by(id=event)
        return out.order_by("id").all()

    def getTotalEvents(self):
        self.reads += 1
        return self.session.query(Event).count()

    """Team Event"""

    def getTeamEvent(self, teamEvent):
        self.reads += 1
        return self.session.query(TeamEvent).filter_by(id=teamEvent).first()

    def getTeamEvent_byParts(self, team, event):
        self.reads += 1
        return (
            self.session.query(TeamEvent)
            .filter_by(team_id=team, event_id=event)
            .first()
        )

    def getTeamEventId_byParts(self, team, event):
        self.reads += 1
        return (
            self.session.query(TeamEvent.id)
            .filter_by(team_id=team, event_id=event)
            .first()[0]
        )

    def getTeamEvents(
        self, team=None, year=None, teamYear=None, event=None, teamEvent=None
    ):
        self.reads += 1
        out = self.session.query(TeamEvent)
        if team is not None:
            out = out.filter_by(team_id=team)
        if year is not None:
            out = out.filter_by(year_id=year)
        if teamYear is not None:
            out = out.filter_by(team_year_id=teamYear)
        if event is not None:
            out = out.filter_by(event_id=event)
        if teamEvent is not None:
            out = out.filter_by(id=teamEvent)
        return out.order_by("id").all()

    def getTotalTeamEvents(self):
        self.reads += 1
        return self.session.query(TeamEvent).count()

    """Match"""

    def getMatch(self, match):
        self.reads += 1
        return self.session.query(Match).filter_by(id=match).first()

    def getMatch_byKey(self, match_key):
        self.reads += 1
        return self.session.query(Match).filter_by(key=match_key).first()

    def getMatches_year(self, year):
        self.reads += 1
        return self.session.query(Match).filter_by(year_id=year).order_by("time").all()

    def getMatches(self, year=None, event=None, match=None, playoff=None):
        self.reads += 1
        out = self.session.query(Match)
        if year is not None:
            out = out.filter_by(year_id=year)
        if event is not None:
            out = out.filter_by(event_id=event)
        if match is not None:
            out = out.filter_by(id=match)
        if playoff is not None:
            out = out.filter_by(playoff=playoff)
        return out.order_by("id").all()

    def getTotalMatches(self):
        self.reads += 1
        return self.session.query(Match).count()

    """Team Matches"""

    def getTeamMatch(self, team_match):
        self.reads += 1
        return self.session.query(TeamMatch).filter_by(id=team_match).first()

    def getTeamMatches(
        self, year=None, event=None, match=None, playoff=None, team=None
    ):
        self.reads += 1
        out = self.session.query(TeamMatch)
        if year is not None:
            out = out.filter_by(year_id=year)
        if event is not None:
            out = out.filter_by(event_id=event)
        if match is not None:
            out = out.filter_by(id=match)
        if playoff is not None:
            out = out.filter_by(playoff=playoff)
        if team is not None:
            out = out.filter_by(team_id=team)
        return out.order_by("id").all()

    def getTotalTeamMatches(self):
        self.reads += 1
        return self.session.query(TeamMatch).count()

    """EVENT PRED"""

    def getYearDict(self, year):
        self.reads += 1
        data = (
            self.session.query(Year.score_sd, Year.score_mean)
            .filter_by(id=year)
            .first()
        )
        return [data[0], data[1]]

    def getEventDict(self, event_key):
        self.reads += 1
        data = self.session.query(Event, Event.id).filter_by(key=event_key).first()
        return [data[0], data[1]]

    def getTeamsDict(self, event_id):
        self.reads += 1
        data = (
            self.session.query(
                TeamEvent.team_id,
                TeamEvent.elo_start,
                TeamEvent.opr_start,
                TeamEvent.opr_auto,
                TeamEvent.opr_teleop,
                TeamEvent.opr_1,
                TeamEvent.opr_2,
                TeamEvent.opr_endgame,
                TeamEvent.opr_fouls,
                TeamEvent.opr_no_fouls,
                TeamEvent.ils_1_start,
                TeamEvent.ils_2_start,
            )
            .filter_by(event_id=event_id)
            .all()
        )

        out, stats = [], {}
        for entry in data:
            out.append(entry[0])
            stats[entry[0]] = {
                "elo_start": entry[1],
                "opr_start": entry[2],
                "opr_auto": entry[3],
                "opr_teleop": entry[4],
                "opr_1": entry[5],
                "opr_2": entry[6],
                "opr_endgame": entry[7],
                "opr_fouls": entry[8],
                "opr_no_fouls": entry[9],
                "ils_1_start": entry[10],
                "ils_2_start": entry[11],
            }

        return out, stats

    def getMatchesDict(self, event_id):
        self.reads += 1
        data = (
            self.session.query(
                Match.id,
                Match.winner,
                Match.elo_win_prob,
                Match.opr_win_prob,
                Match.mix_win_prob,
                Match.red_rp_1_prob,
                Match.red_rp_2_prob,
                Match.blue_rp_1_prob,
                Match.blue_rp_2_prob,
                Match.red_score,
                Match.blue_score,
                Match.red_rp_1,
                Match.red_rp_2,
                Match.blue_rp_1,
                Match.blue_rp_2,
                Match.red_1,
                Match.blue_1,
                Match.red_2,
                Match.blue_2,
                Match.red_auto,
                Match.blue_auto,
                Match.red_teleop,
                Match.blue_teleop,
                Match.red_endgame,
                Match.blue_endgame,
                Match.red_fouls,
                Match.blue_fouls,
                Match.red_no_fouls,
                Match.blue_no_fouls,
                Match.red,
                Match.blue,
            )
            .filter_by(event_id=event_id, playoff=0)
            .all()
        )

        out = []
        for entry in data:
            out.append(
                {
                    "match_id": entry[0],
                    "winner": entry[1],
                    "elo_win_prob": entry[2],
                    "opr_win_prob": entry[3],
                    "mix_win_prob": entry[4],
                    "red_rp_1_prob": entry[5],
                    "red_rp_2_prob": entry[6],
                    "blue_rp_1_prob": entry[7],
                    "blue_rp_2_prob": entry[8],
                    "red_score": entry[9],
                    "blue_score": entry[10],
                    "red_rp_1": entry[11],
                    "red_rp_2": entry[12],
                    "blue_rp_1": entry[13],
                    "blue_rp_2": entry[14],
                    "red_1": entry[15],
                    "blue_1": entry[16],
                    "red_2": entry[17],
                    "blue_2": entry[18],
                    "red_auto": entry[19],
                    "blue_auto": entry[20],
                    "red_teleop": entry[21],
                    "blue_teleop": entry[22],
                    "red_endgame": entry[23],
                    "blue_endgame": entry[24],
                    "red_fouls": entry[25],
                    "blue_fouls": entry[26],
                    "red_no_fouls": entry[27],
                    "blue_no_fouls": entry[28],
                    "red": [int(x) for x in entry[29].split(",")],
                    "blue": [int(x) for x in entry[30].split(",")],
                }
            )

        return out

    def getTeamMatchesDict(self, event_id):
        self.reads += 1
        data = (
            self.session.query(TeamMatch.team_id, TeamMatch.match_id, TeamMatch.elo)
            .filter_by(event_id=event_id)
            .all()
        )

        out = {}
        for entry in data:
            if entry[1] not in out:
                out[entry[1]] = {}
            if entry[0] not in out[entry[1]]:
                out[entry[1]][entry[0]] = entry[2]
        return out
