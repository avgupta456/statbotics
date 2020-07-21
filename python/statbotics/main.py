import datetime

import requests
from cachecontrol import CacheControl

import validate


class Statbotics:
    def __init__(self):
        self.BASE_URL = "https://backend.statbotics.io"
        self.session = CacheControl(requests.Session())
        self.login(self.getToken())
        self.token = self.getToken()

    def getToken(self, retries=0):
        if retries > 2:
            raise UserWarning("Could not connect to Statbotics.io")
        self.session.get(self.BASE_URL + "/admin/")
        if "csrftoken" not in self.session.cookies:
            return self.getToken(retries + 1)
        return self.session.cookies["csrftoken"]

    def login(self, token):
        login_data = {"csrfmiddlewaretoken": token, "next": self.BASE_URL + "/admin/"}
        self.session.post(
            self.BASE_URL + "/admin/login/",
            data=login_data,
            headers=dict(Referer=self.BASE_URL),
        )

    def _get(self, url, retry=0):
        resp = self.session.get(self.BASE_URL + url)
        if resp.status_code == 200:
            return resp.json()
        if retry < 2:
            self._get(url, retry=retry + 1)
        raise UserWarning("Invalid query, or traffic too high (try later)")

    def _negate(self, string):
        if len(string) == 0:
            return string
        if string[0] == "-":
            return string[1:]
        return "-" + string

    def getTeam(self, team):
        validate.checkType(team, "int", "team")
        return self._get("/api/team/" + str(team))

    def getTeams(
        self,
        country=None,
        state=None,
        district=None,
        active=True,
        metric=None,
        count=1000,
        offset=0,
        fields=["all"],
    ):
        url = "/api/_teams?"

        validate.checkType(metric, "str", "metric")
        validate.checkType(count, "int", "count")
        validate.checkType(offset, "int", "offset")
        validate.checkType(fields, "list", "fields")

        url += "limit=" + str(count) + "&offset=" + str(offset)
        url += validate.getLocations(country, state, district)

        if active:
            url += "&active=1"

        if metric:
            if metric not in validate.getTeamMetrics():
                raise ValueError("Invalid metric")
            url += "&o=" + self._negate(metric)

        data = self._get(url)["results"]
        if fields == ["all"]:
            return data

        out = []
        for entry in data:
            new_entry = {}
            for field in fields:
                new_entry[field] = entry[field]
            out.append(new_entry)
        return out

    def getYear(self, year):
        validate.checkType(year, "int", "year")
        out = self._get("/api/year/" + str(year))
        if len(out) == 0:
            raise ValueError("Invalid year")
        return out[0]

    def getYears(self, metric=None):
        validate.checkType(metric, "str", "metric")
        return self._get("/api/years")

    def getTeamYear(self, team, year):
        validate.checkType(team, "int", "team")
        validate.checkType(year, "int", "year")
        out = self._get("/api/team_year/team/" + str(team) + "/year/" + str(year))
        if len(out) == 0:
            raise ValueError("Invalid (team, year) pair")
        return out[0]

    def getTeamYears(
        self,
        team=None,
        year=None,
        country=None,
        state=None,
        district=None,
        metric=None,
        page=None,
    ):

        url = "/api/team_years"

        validate.checkType(team, "int", "team")
        validate.checkType(year, "int", "year")
        validate.checkType(metric, "str", "metric")

        if (
            not team
            and not year
            and (country == "USA" or not country)
            and not state
            and not district
        ):
            raise UserWarning("Query too large, be more specific")

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
        out = self._get("/api/event/" + event)
        if len(out) == 0:
            raise ValueError("Invalid event key")
        return out[0]

    def getEvents(
        self,
        year=None,
        country=None,
        state=None,
        district=None,
        type=None,
        week=None,
        metric=None,
    ):

        url = "/api/events"

        validate.checkType(year, "int", "year")
        validate.checkType(metric, "str", "metric")
        validate.checkType(week, "int", "week")
        type = validate.getType(type)

        if year:
            url += "/year/" + str(year)

        if type:
            url += "/type/" + str(type)

        if week:
            url += "/week/" + str(week)

        url += validate.getLocations(country, state, district)

        if metric:
            if metric not in validate.getEventMetrics():
                raise ValueError("Invalid metric")
            url += "/by/" + self._negate(metric)

        return self._get(url)

    def getTeamEvent(self, team, event):
        validate.checkType(team, "int", "team")
        validate.checkType(event, "str", "event")
        out = self._get("/api/team_event/team/" + str(team) + "/event/" + event)
        if len(out) == 0:
            raise ValueError("Invalid (team, event) pair)")
        return out[0]

    def getTeamEvents(
        self,
        team=None,
        year=None,
        event=None,
        country=None,
        state=None,
        district=None,
        type=None,
        week=None,
        metric=None,
        page=1,
    ):

        url = "/api/team_events"

        validate.checkType(team, "int", "team")
        validate.checkType(event, "str", "event")
        validate.checkType(metric, "str", "metric")
        validate.checkType(page, "int", "page")
        validate.checkType(week, "int", "week")
        type = validate.getType(type)

        if (
            not team
            and not event
            and (country == "USA" or not country)
            and not state
            and not district
            and not (year and type)
            and not (year and week)
        ):
            raise UserWarning("Query too large, be more specific")

        if team and event:
            raise UserWarning("Use getTeamEvent() instead")
        if event and (year or type or week):
            raise UserWarning("Overconstrained query")
        if (team or event) and (country or state or district):
            raise UserWarning("Conflicting location input")

        if team:
            url += "/team/" + str(team)

        if year:
            url += "/year/" + str(year)

        if event:
            url += "/event/" + event

        if type:
            url += "/type/" + str(type)

        if week:
            url += "/week/" + str(week)

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
        out = self._get("/api/match/" + match)
        if len(out) == 0:
            raise ValueError("Invalid match key")
        return out[0]

    def getMatches(self, year=None, event=None, elims=None, page=None):

        url = "/api/matches"

        validate.checkType(year, "int", "year")
        validate.checkType(event, "str", "event")
        validate.checkType(page, "int", "page")
        validate.checkType(elims, "bool", "elims")

        if not event:
            raise UserWarning("Query too large, be more specific (event)")

        if year and event:
            raise UserWarning("Year input will be ignored")

        if year:
            url += "/year/" + str(year)

        if event:
            url += "/event/" + event

        if elims:
            url += "/elims"

        if page and page != 1:
            url += "/page/" + page

        return self._get(url)

    def getTeamMatch(self, team, match):
        validate.checkType(team, "int", "team")
        validate.checkType(match, "str", "match")
        out = self._get("/api/team_match/team/" + str(team) + "/match/" + match)
        if len(out) == 0:
            raise ValueError("Invalid (team, match) pair)")
        return out[0]

    def getTeamMatches(
        self, team=None, year=None, event=None, match=None, elims=None, page=None
    ):
        start = datetime.datetime.now()
        url = "/api/team_matches"

        validate.checkType(team, "int", "team")
        validate.checkType(year, "int", "year")
        validate.checkType(event, "str", "event")
        validate.checkType(match, "str", "match")
        validate.checkType(page, "int", "page")
        validate.checkType(elims, "bool", "elims")

        if not team and not event and not match:
            raise UserWarning(
                "Query too large, be more specific (team, event, or match)"
            )

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

        if elims:
            url += "/elims"

        if page and page != 1:
            url += "/page/" + str(page)

        out = self._get(url)
        end = datetime.datetime.now()
        print(end - start)
        return out

    """
    def getEventSim(self, event, index=None, full=False, iterations=None):
        validate.checkType(event, "str", "event")
        validate.checkType(index, "int", "index")
        validate.checkType(full, "bool", "full")
        validate.checkType(iterations, "int", "iterations")

        url = "/api/event_sim/event/" + event

        if index:
            url += "/index/" + str(index)

        if full:
            url += "/full"
            if iterations:
                url += "/iterations/" + str(iterations)
        else:
            url += "/simple"

        return self._get(url)
    """


sb = Statbotics()
for i in range(100):
    teams = sb.getTeams(country="USA", count=100, metric="elo", fields=["team", "elo"],)
    print(teams)
    print(i, len(teams))
