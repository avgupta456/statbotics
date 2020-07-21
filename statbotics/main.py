import datetime

import requests
from cachecontrol import CacheControl

from . import validate


class Statbotics:
    """
    Main Object for interfacing with the Statbotics API
    """

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

    def _filter(self, data, fields):
        if fields == ["all"]:
            return data

        for field in fields:
            if field not in data[0]:
                raise ValueError("Invalid field: " + str(field))

        out = []
        for entry in data:
            new_entry = {}
            for field in fields:
                new_entry[field] = entry[field]
            out.append(new_entry)
        return out

    def _get(self, url, fields, retry=0):
        resp = self.session.get(self.BASE_URL + url)
        if resp.status_code != 200:
            if retry < 2:
                return self._get(url, fields, retry=retry + 1)
            raise UserWarning("Invalid query: " + url)
        data = resp.json()["results"]

        if len(data) == 0:
            raise UserWarning("Invalid inputs, no data recieved for " + url)

        return self._filter(data, fields)

    def _negate(self, string):
        if len(string) == 0:
            return string
        if string[0] == "-":
            return string[1:]
        return "-" + string

    def getTeam(self, team, fields=["all"]):
        """
        Function to retrieve information on an individual team\n
        :param team: Team Number, integer\n
        :param fields: List of fields to return. The default is ["all"]\n
        :return: a dictionary with the team's number, location (country, state, district), and Elo statistics (Current Elo, Recent Elo, Mean Elo, Max Elo)\n
        """
        validate.checkType(team, "int", "team")
        validate.checkType(fields, "list", "fields")
        return self._get("/api/_teams?team=" + str(team), fields)[0]

    def getTeams(
        self,
        country=None,
        state=None,
        district=None,
        active=True,
        metric=None,
        limit=1000,
        offset=0,
        fields=["all"],
    ):
        """
        Function to retrieve information on multiple teams\n
        :param country: Restrict based on country (select countries included)\n
        :param state: US States and Canada provinces only. Can infer country.\n
        :param district: Use 2 or 3-letter key (ex: FIM, NE, etc)\n
        :param active: Restrict to active teams (played most recent season)\n
        :param metric: Order output. Default descending, add '-' for ascending. (Ex: "-elo", "team", etc)\n
        :param limit: Limits the output length to speed up queries. Max 10,000\n
        :param offset: Skips the first (offset) items when returning\n
        :param fields: List of fields to return. Default is ["all"]\n
        :return: A list of dictionaries, with each dictionary including the team, location, and Elo statistics\n
        """

        url = "/api/_teams?"

        validate.checkType(metric, "str", "metric")
        validate.checkType(limit, "int", "limit")
        validate.checkType(offset, "int", "offset")
        validate.checkType(fields, "list", "fields")

        if limit > 10000:
            raise ValueError(
                "Please reduce 'limit', consider breaking into multiple smaller queries"
            )

        url += "limit=" + str(limit) + "&offset=" + str(offset)
        url += validate.getLocations(country, state, district)

        if active:
            url += "&active=1"

        if metric:
            if metric not in validate.getTeamMetrics():
                raise ValueError("Invalid metric")
            url += "&o=" + self._negate(metric)

        return self._get(url, fields)

    def getYear(self, year, fields=["all"]):
        validate.checkType(year, "int", "year")
        validate.checkType(fields, "list", "fields")
        return self._get("/api/_years?year=" + str(year), fields)[0]

    def getYears(self, metric=None, limit=1000, offset=0, fields=["all"]):
        validate.checkType(metric, "str", "metric")
        validate.checkType(limit, "int", "limit")
        validate.checkType(offset, "int", "offset")
        validate.checkType(fields, "list", "fields")
        url = "/api/_years?limit=" + str(limit) + "&offset=" + str(offset)
        if metric:
            url += "&o=" + self._negate(metric)
        return self._get(url, fields)

    def getTeamYear(self, team, year, fields=["all"]):
        validate.checkType(team, "int", "team")
        validate.checkType(year, "int", "year")
        validate.checkType(fields, "list", "fields")
        url = "/api/_team_years?team=" + str(team) + "&year=" + str(year)
        return self._get(url, fields)[0]

    def getTeamYears(
        self,
        team=None,
        year=None,
        country=None,
        state=None,
        district=None,
        metric=None,
        limit=1000,
        offset=0,
        fields=["all"],
    ):

        url = "/api/_team_years"

        validate.checkType(team, "int", "team")
        validate.checkType(year, "int", "year")
        validate.checkType(metric, "str", "metric")
        validate.checkType(limit, "int", "limit")
        validate.checkType(offset, "int", "offset")
        validate.checkType(fields, "list", "fields")

        if limit > 10000:
            raise ValueError(
                "Please reduce 'limit', consider breaking into multiple smaller queries"
            )

        url += "?limit=" + str(limit) + "&offset=" + str(offset)

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
            url += "&team=" + str(team)

        if year:
            url += "&year=" + str(year)

        url += validate.getLocations(country, state, district)

        if metric:
            if metric not in validate.getTeamYearMetrics():
                raise ValueError("Invalid metric")
            url += "&o=" + self._negate(metric)

        return self._get(url, fields)

    def getEvent(self, event, fields=["all"]):
        validate.checkType(event, "str", "event")
        validate.checkType(fields, "list", "fields")
        url = "/api/_events?key=" + event
        return self._get(url, fields)[0]

    def getEvents(
        self,
        year=None,
        country=None,
        state=None,
        district=None,
        type=None,
        week=None,
        metric=None,
        limit=1000,
        offset=0,
        fields=["all"],
    ):

        url = "/api/_events"

        validate.checkType(year, "int", "year")
        validate.checkType(metric, "str", "metric")
        type = validate.getType(type)
        validate.checkType(week, "int", "week")
        validate.checkType(limit, "int", "limit")
        validate.checkType(offset, "int", "offset")
        validate.checkType(fields, "list", "fields")

        if limit > 10000:
            raise ValueError(
                "Please reduce 'limit', consider breaking into multiple smaller queries"
            )

        url += "?limit=" + str(limit) + "&offset=" + str(offset)

        if year:
            url += "&year=" + str(year)

        url += validate.getLocations(country, state, district)

        if metric:
            if metric not in validate.getEventMetrics():
                raise ValueError("Invalid metric")
            url += "&o=" + self._negate(metric)

        data = self._get(url, ["all"])
        if type is not None:
            new_data = []
            for entry in data:
                if entry["type"] == type:
                    new_data.append(entry)
            data = new_data
        if week is not None:
            new_data = []
            for entry in data:
                if entry["week"] == week:
                    new_data.append(entry)
            data = new_data
        return self._filter(data, fields)

    def getTeamEvent(self, team, event, fields=["all"]):
        validate.checkType(team, "int", "team")
        validate.checkType(event, "str", "event")
        validate.checkType(fields, "list", "fields")
        url = "/api/_team_events?team=" + str(team) + "&event=" + event
        return self._get(url, fields)[0]

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
        limit=1000,
        offset=0,
        fields=["all"],
    ):

        url = "/api/_team_events"

        validate.checkType(team, "int", "team")
        validate.checkType(event, "str", "event")
        type = validate.getType(type)
        validate.checkType(week, "int", "week")
        validate.checkType(metric, "str", "metric")
        validate.checkType(limit, "int", "limit")
        validate.checkType(offset, "int", "offset")
        validate.checkType(fields, "list", "fields")

        if limit > 10000:
            raise ValueError(
                "Please reduce 'limit', consider breaking into multiple smaller queries"
            )

        url += "?limit=" + str(limit) + "&offset=" + str(offset)

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
            url += "&team=" + str(team)

        if year:
            url += "&year=" + str(year)

        if event:
            url += "&event=" + event

        url += validate.getLocations(country, state, district)

        if metric:
            if metric not in validate.getTeamEventMetrics():
                raise ValueError("Invalid metric")
            url += "&o=" + self._negate(metric)

        data = self._get(url, ["all"])
        if type is not None:
            new_data = []
            for entry in data:
                if entry["type"] == type:
                    new_data.append(entry)
            data = new_data
        if week is not None:
            new_data = []
            for entry in data:
                if entry["week"] == week:
                    new_data.append(entry)
            data = new_data
        return self._filter(data, fields)

    def getMatch(self, match, fields=["all"]):
        validate.checkType(match, "str", "match")
        validate.checkType(fields, "list", "fields")
        return self._get("/api/_matches?key=" + match, fields)[0]

    def getMatches(
        self, year=None, event=None, elims=None, limit=1000, offset=0, fields=["all"]
    ):

        url = "/api/_matches"

        validate.checkType(year, "int", "year")
        validate.checkType(event, "str", "event")
        validate.checkType(elims, "bool", "elims")
        validate.checkType(limit, "int", "limit")
        validate.checkType(offset, "int", "offset")
        validate.checkType(fields, "list", "fields")

        if limit > 10000:
            raise ValueError(
                "Please reduce 'limit', consider breaking into multiple smaller queries"
            )

        url += "?limit=" + str(limit) + "&offset=" + str(offset)

        if not event:
            raise UserWarning("Query too large, be more specific (event)")

        if year and event:
            raise UserWarning("Year input will be ignored")

        if year:
            url += "&year=" + str(year)

        if event:
            url += "&event=" + event

        if elims:
            url += "&playoff=1"

        url += "&o=time"
        return self._get(url, fields)

    def getTeamMatch(self, team, match, fields=["all"]):
        validate.checkType(team, "int", "team")
        validate.checkType(match, "str", "match")
        validate.checkType(fields, "list", "fields")
        url = "/api/_team_matches?team=" + str(team) + "&match=" + str(match)
        return self._get(url, fields)[0]

    def getTeamMatches(
        self,
        team=None,
        year=None,
        event=None,
        match=None,
        elims=None,
        limit=1000,
        offset=0,
        fields=["all"],
    ):
        url = "/api/_team_matches"

        validate.checkType(team, "int", "team")
        validate.checkType(year, "int", "year")
        validate.checkType(event, "str", "event")
        validate.checkType(match, "str", "match")
        validate.checkType(elims, "bool", "elims")
        validate.checkType(limit, "int", "limit")
        validate.checkType(offset, "int", "offset")
        validate.checkType(fields, "list", "fields")

        if limit > 10000:
            raise ValueError(
                "Please reduce 'limit', consider breaking into multiple smaller queries"
            )

        url += "?limit=" + str(limit) + "&offset=" + str(offset)

        if not team and not event and not match:
            raise UserWarning(
                "Query too large, be more specific (team, event, or match)"
            )

        if (year and event) or (year and match) or (event and match):
            raise UserWarning("Only specify one of (year, event, match)")

        if team:
            url += "&team=" + str(team)

        if year:
            url += "&year=" + str(year)

        if event:
            url += "&event=" + event

        if match:
            url += "&match=" + match

        if elims:
            url += "&playoff=1"

        url += "&o=time"
        print(url)
        return self._get(url, fields)

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
