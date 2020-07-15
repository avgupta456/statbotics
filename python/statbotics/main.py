import requests
from cachecontrol import CacheControl

from . import validate


class Statbotics():
    def __init__(self):
        self.BASE_URL = "https://backend.statbotics.io"
        self.session = CacheControl(requests.Session())
        self.login(self.getToken())
        self.token = self.getToken()

    def getToken(self, retries=0):
        if retries > 2:
            raise UserWarning("Could not connect to Statbotics.io")
        self.session.get(self.BASE_URL+"/admin/")
        if 'csrftoken' not in self.session.cookies:
            return self.getToken(retries + 1)
        return self.session.cookies['csrftoken']

    def login(self, token):
        login_data = {
            "csrfmiddlewaretoken": token,
            "next": self.BASE_URL + "/admin/"
        }
        self.session.post(
            self.BASE_URL + "/admin/login/",
            data=login_data,
            headers=dict(Referer=self.BASE_URL)
        )

    def _get(self, url):
        resp = self.session.get(self.BASE_URL+url)
        if resp.status_code == 200:
            return resp.json()
        raise UserWarning("Invalid Query " +
                          "(some large queries do not support metric)")

    def _negate(self, string):
        if len(string) == 0:
            return string
        if string[0] == "-":
            return string[1:]
        return "-" + string

    def getTeam(self, team):
        validate.checkType(team, "int", "team")
        return self._get("/api/team/"+str(team))

    def getTeams(self, country=None, state=None, district=None,
                 active=True, metric=None):

        url = "/api/teams"

        validate.checkType(metric, "str", "metric")

        url += validate.getLocations(country, state, district)

        if active:
            url += "/active"

        if metric:
            if metric not in validate.getTeamMetrics():
                raise ValueError("Invalid metric")
            url += "/by/" + self._negate(metric)

        return self._get(url)

    def getYear(self, year):
        validate.checkType(year, "int", "year")
        out = self._get("/api/year/"+str(year))
        if len(out) == 0:
            raise ValueError("Invalid year")
        return out[0]

    def getYears(self, metric=None):
        validate.checkType(metric, "str", "metric")
        return self._get("/api/years")

    def getTeamYear(self, team, year):
        validate.checkType(team, "int", "team")
        validate.checkType(year, "int", "year")
        out = self._get("/api/team_year/team/"+str(team)+"/year/"+str(year))
        if len(out) == 0:
            raise ValueError("Invalid (team, year) pair")
        return out[0]

    def getTeamYears(self, team=None, year=None, country=None, state=None,
                     district=None, metric=None, page=None):

        url = "/api/team_years"

        validate.checkType(team, "int", "team")
        validate.checkType(year, "int", "year")
        validate.checkType(metric, "str", "metric")

        if team and year:
            raise UserWarning("Use getTeamYear() instead")
        if team and (country or state or district):
            raise UserWarning("Conflicting location input")

        if team:
            url += "/team/" + str(team)

        if year:
            url += "/year/" + str(year)

        url += validate.getLocations(country, state, district)

        if metric:
            if metric not in validate.getTeamYearMetrics():
                raise ValueError("Invalid metric")
            url += "/by/" + self._negate(metric)

        if page and page != 1:
            url += "/page/" + str(page)

        return self._get(url)

    def getEvent(self, event):
        validate.checkType(event, "str", "event")
        out = self._get("/api/event/"+event)
        if len(out) == 0:
            raise ValueError("Invalid event key")
        return out[0]

    def getEvents(self, year=None, country=None, state=None, district=None,
                  metric=None):

        url = "/api/events"

        validate.checkType(year, "int", "year")
        validate.checkType(metric, "str", "metric")

        if year:
            url += "/year/" + str(year)
        url += validate.getLocations(country, state, district)

        if metric:
            if metric not in validate.getEventMetrics():
                raise ValueError("Invalid metric")
            url += "/by/" + self._negate(metric)

        return self._get(url)

    def getTeamEvent(self, team, event):
        validate.checkType(team, "int", "team")
        validate.checkType(event, "str", "event")
        out = self._get("/api/team_event/team/"+str(team)+"/event/"+event)
        if len(out) == 0:
            raise ValueError("Invalid (team, event) pair)")
        return out[0]

    def getTeamEvents(self, team=None, year=None, event=None, country=None,
                      state=None, district=None, metric=None, page=None):

        url = "/api/team_events"

        validate.checkType(team, "int", "team")
        validate.checkType(event, "str", "event")
        validate.checkType(metric, "str", "metric")
        validate.checkType(page, "int", "page")

        if team and event:
            raise UserWarning("Use getTeamEvent() instead")
        if year and event:
            raise UserWarning("Year input will be ignored")
        if (team or event) and (country or state or district):
            raise UserWarning("Conflicting location input")

        if team:
            url += "/team/" + str(team)

        if year:
            url += "/year/" + str(year)

        if event:
            url += "/event/" + event

        url += validate.getLocations(country, state, district)

        if metric:
            if metric not in validate.getTeamEventMetrics():
                raise ValueError("Invalid metric")
            url += "/by/" + self._negate(metric)

        if page and page != 1:
            url += "/page/" + page

        return self._get(url)

    def getMatch(self, match):
        validate.checkType(match, "str", "match")
        out = self._get("/api/match/"+match)
        if len(out) == 0:
            raise ValueError("Invalid match key")
        return out[0]

    def getMatches(self, year=None, event=None, page=None):

        url = "/api/matches"

        validate.checkType(year, "int", "year")
        validate.checkType(event, "str", "event")
        validate.checkType(page, "int", "page")

        if year and event:
            raise UserWarning("Year input will be ignored")

        if year:
            url += "/year/" + str(year)

        if event:
            url += "/event/" + event

        if page and page != 1:
            url += "/page/" + page

        return self._get(url)

    def getTeamMatch(self, team, match):
        validate.checkType(team, "int", "team")
        validate.checkType(match, "str", "match")
        out = self._get("/api/team_match/team/"+str(team)+"/match/"+match)
        if len(out) == 0:
            raise ValueError("Invalid (team, match) pair)")
        return out[0]

    def getTeamMatches(self, team=None, year=None, event=None, match=None,
                       page=None):

        url = "/api/team_matches"

        validate.checkType(team, "int", "team")
        validate.checkType(year, "int", "year")
        validate.checkType(event, "str", "event")
        validate.checkType(match, "str", "match")
        validate.checkType(page, "int", "page")

        if (year and event) or (year and match) or (event and match):
            raise UserWarning("Only specify one of (year, event, match)")

        if team:
            url += "/team/" + str(team)

        if year:
            url += "/year/" + str(year)

        if event:
            url += "/event/" + event

        if match:
            url += "/match/" + match

        if page and page != 1:
            url += "/page/" + str(page)

        return self._get(url)
