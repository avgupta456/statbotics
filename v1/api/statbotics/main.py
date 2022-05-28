import datetime

import requests
from cachecontrol import CacheControl

from . import validate


class Statbotics:
    """
    Main Object for interfacing with the Statbotics API
    """

    def __init__(self):
        self.BASE_URL = "https://api.statbotics.io"
        self.session = CacheControl(requests.Session())
        self.login(self.get_token())
        self.token = self.get_token()

    def get_token(self, retries=0):
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

        data = resp.json()
        if "results" in data:
            data = data["results"]

        if len(data) == 0:
            raise UserWarning("Invalid inputs, no data recieved for " + url)

        return self._filter(data, fields)

    def _negate(self, string):
        if len(string) == 0:
            return string
        if string[0] == "-":
            return string[1:]
        return "-" + string

    def get_team(self, team, fields=["all"]):
        """
        Function to retrieve information on an individual team\n
        :param team: Team Number, integer\n
        :param fields: List of fields to return. The default is ["all"]\n
        :return: a dictionary with the team's number, location (country, state, district), and Elo statistics (Current Elo, Recent Elo, Mean Elo, Max Elo)\n
        """

        validate.check_type(team, "int", "team")
        validate.check_type(fields, "list", "fields")
        return self._get("/v1/_teams?team=" + str(team), fields)[0]

    def get_teams(
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
        :return: A list of dictionaries, each dictionary including the team, location, and Elo statistics\n
        """

        url = "/v1/_teams?"

        validate.check_type(metric, "str", "metric")
        validate.check_type(limit, "int", "limit")
        validate.check_type(offset, "int", "offset")
        validate.check_type(fields, "list", "fields")

        if limit > 10000:
            raise ValueError(
                "Please reduce 'limit', consider breaking into multiple smaller queries"
            )

        url += "limit=" + str(limit) + "&offset=" + str(offset)
        url += validate.get_locations(country, state, district)

        if active:
            url += "&active=1"

        if metric:
            if metric not in validate.get_team_metrics():
                raise ValueError("Invalid metric")
            url += "&o=" + self._negate(metric)

        return self._get(url, fields)

    def get_year(self, year, fields=["all"]):
        """
        Function to retrieve information for a specific year\n
        :param year: Year, integer\n
        :param fields: List of fields to return. The default is ["all"]\n
        :return: a dictionary with the year, match prediction statistics, and RP prediction statistics\n
        """

        validate.check_type(year, "int", "year")
        validate.check_type(fields, "list", "fields")
        return self._get("/v1/_years?year=" + str(year), fields)[0]

    def get_years(self, metric=None, limit=1000, offset=0, fields=["all"]):
        """
        Function to retrieve information on multiple years\n
        :param metric: Order output. Default descending, add '-' for ascending. (Ex: "elo_acc", "-opr_mse", etc)\n
        :param limit: Limits the output length to speed up queries. Max 10,000\n
        :param offset: Skips the first (offset) items when returning\n
        :param fields: List of fields to return. Default is ["all"]\n
        :return: A list of dictionaries, each dictionary including the year and match/RP prediction statistics\n
        """

        validate.check_type(metric, "str", "metric")
        validate.check_type(limit, "int", "limit")
        validate.check_type(offset, "int", "offset")
        validate.check_type(fields, "list", "fields")
        url = "/v1/_years?limit=" + str(limit) + "&offset=" + str(offset)
        if metric:
            url += "&o=" + self._negate(metric)
        return self._get(url, fields)

    def get_team_year(self, team, year, fields=["all"]):
        """
        Function to retrieve information for a specific team's performance in a specific year\n
        :param team: Team number, integer\n
        :param year: Year, integer\n
        :param fields: List of fields to return. The default is ["all"]\n
        :return: a dictionary with the team, year, and Elo/OPR statistics\n
        """

        validate.check_type(team, "int", "team")
        validate.check_type(year, "int", "year")
        validate.check_type(fields, "list", "fields")
        url = "/v1/_team_years?team=" + str(team) + "&year=" + str(year)
        return self._get(url, fields)[0]

    def get_team_years(
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
        """
        Function to retrieve information on multiple (team, year) pairs\n
        :param team: Restrict based on a specific team number\n
        :param country: Restrict based on country (select countries included)\n
        :param state: US States and Canada provinces only. Can infer country.\n
        :param district: Use 2 or 3-letter key (ex: FIM, NE, etc)\n
        :param metric: Order output. Default descending, add '-' for ascending. (Ex: "elo_pre_champs", "-opr_auto", etc)\n
        :param limit: Limits the output length to speed up queries. Max 10,000\n
        :param offset: Skips the first (offset) items when returning\n
        :param fields: List of fields to return. Default is ["all"]\n
        :return: A list of dictionaries, each dictionary including the team, year, and OPR/Elo statistics\n
        """

        url = "/v1/_team_years"

        validate.check_type(team, "int", "team")
        validate.check_type(year, "int", "year")
        validate.check_type(metric, "str", "metric")
        validate.check_type(limit, "int", "limit")
        validate.check_type(offset, "int", "offset")
        validate.check_type(fields, "list", "fields")

        if limit > 10000:
            raise ValueError(
                "Please reduce 'limit', consider breaking into multiple smaller queries"
            )

        url += "?limit=" + str(limit) + "&offset=" + str(offset)

        if team and year:
            raise UserWarning("Use get_team_year() instead")
        if team and (country or state or district):
            raise UserWarning("Conflicting location input")

        if team:
            url += "&team=" + str(team)

        if year:
            url += "&year=" + str(year)

        url += validate.get_locations(country, state, district)

        if metric:
            if metric not in validate.get_team_year_metrics():
                raise ValueError("Invalid metric")
            url += "&o=" + self._negate(metric)

        return self._get(url, fields)

    def get_event(self, event, fields=["all"]):
        """
        Function to retrieve information for a specific event\n
        :param event: Event key, string (ex: "2019cur")\n
        :param fields: List of fields to return. The default is ["all"]\n
        :return: a dictionary with the event and Elo/OPR statistics\n
        """

        validate.check_type(event, "str", "event")
        validate.check_type(fields, "list", "fields")
        url = "/v1/_events?key=" + event
        return self._get(url, fields)[0]

    def get_events(
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
        """
        Function to retrieve information on multiple events\n
        :param year: Restrict by specific year, integer\n
        :param country: Restrict based on country (select countries included)\n
        :param state: US States and Canada provinces only. Can infer country.\n
        :param district: Use 2 or 3-letter key (ex: FIM, NE, etc)\n
        :param type: 0=regional, 1=district, 2=district champ, 3=champs, 4=einstein\n
        :param week: Week of play, generally between 0 and 8\n
        :param metric: Order output. Default descending, add '-' for ascending. (Ex: "elo_pre_playoffs", "-opr_end", etc)\n
        :param limit: Limits the output length to speed up queries. Max 10,000\n
        :param offset: Skips the first (offset) items when returning\n
        :param fields: List of fields to return. Default is ["all"]\n
        :return: A list of dictionaries, each dictionary including the team, event and Elo/OPR statistics\n
        """

        url = "/v1/_events"

        validate.check_type(year, "int", "year")
        validate.check_type(metric, "str", "metric")
        type = validate.get_type(type)
        validate.check_type(week, "int", "week")
        validate.check_type(limit, "int", "limit")
        validate.check_type(offset, "int", "offset")
        validate.check_type(fields, "list", "fields")

        if limit > 10000:
            raise ValueError(
                "Please reduce 'limit', consider breaking into multiple smaller queries"
            )

        url += "?limit=" + str(limit) + "&offset=" + str(offset)

        if year:
            url += "&year=" + str(year)

        url += validate.get_locations(country, state, district)

        if type is not None:
            url += "&type=" + str(type)

        if week is not None:
            url += "&week=" + str(week)

        if metric:
            if metric not in validate.get_event_metrics():
                raise ValueError("Invalid metric")
            url += "&o=" + self._negate(metric)

        return self._get(url, fields)

    def get_team_event(self, team, event, fields=["all"]):
        """
        Function to retrieve information for a specific (team, event) pair\n
        :param team: Team number, integer\n
        :param event: Event key, string (ex: "2019cur")\n
        :param fields: List of fields to return. The default is ["all"]\n
        :return: a dictionary with the event and Elo/OPR statistics\n
        """

        validate.check_type(team, "int", "team")
        validate.check_type(event, "str", "event")
        validate.check_type(fields, "list", "fields")
        url = "/v1/_team_events?team=" + str(team) + "&event=" + event
        return self._get(url, fields)[0]

    def get_team_events(
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
        """
        Function to retrieve information on multiple (team, event) pairs\n
        :param team: Restrict by team number, integer\n
        :param year: Restrict by specific year, integer\n
        :param country: Restrict based on country (select countries included)\n
        :param state: US States and Canada provinces only. Can infer country.\n
        :param district: Use 2 or 3-letter key (ex: FIM, NE, etc)\n
        :param type: 0=regional, 1=district, 2=district champ, 3=champs, 4=einstein\n
        :param week: Week of play, generally between 0 and 8\n
        :param metric: Order output. Default descending, add '-' for ascending. (Ex: "elo_pre_playoffs", "-opr_end", etc)\n
        :param limit: Limits the output length to speed up queries. Max 10,000\n
        :param offset: Skips the first (offset) items when returning\n
        :param fields: List of fields to return. Default is ["all"]\n
        :return: A list of dictionaries, each dictionary including the team, event and Elo/OPR statistics\n
        """

        url = "/v1/_team_events"

        validate.check_type(team, "int", "team")
        validate.check_type(event, "str", "event")
        type = validate.get_type(type)
        validate.check_type(week, "int", "week")
        validate.check_type(metric, "str", "metric")
        validate.check_type(limit, "int", "limit")
        validate.check_type(offset, "int", "offset")
        validate.check_type(fields, "list", "fields")

        if limit > 10000:
            raise ValueError(
                "Please reduce 'limit', consider breaking into multiple smaller queries"
            )

        url += "?limit=" + str(limit) + "&offset=" + str(offset)

        if team and event:
            raise UserWarning("Use get_team_event() instead")
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

        url += validate.get_locations(country, state, district)

        if type is not None:
            url += "&type=" + str(type)

        if week is not None:
            url += "&week=" + str(week)

        if metric:
            if metric not in validate.get_team_event_metrics():
                raise ValueError("Invalid metric")
            url += "&o=" + self._negate(metric)

        return self._get(url, fields)

    def get_match(self, match, fields=["all"]):
        """
        Function to retrieve information for a specific match\n
        :param match: Match key, string (ex: "2019cur_qm1", "2019cmptx_f1m3")\n
        :param fields: List of fields to return. The default is ["all"]\n
        :return: a dictionary with the match, score breakdowns, and predictions\n
        """

        validate.check_type(match, "str", "match")
        validate.check_type(fields, "list", "fields")
        return self._get("/v1/_matches?key=" + match, fields)[0]

    def get_matches(
        self, year=None, event=None, elims=None, limit=1000, offset=0, fields=["all"]
    ):
        """
        Function to retrieve information on multiple matches\n
        :param year: Restrict by specific year, integer\n
        :param event: Restrict by specific event key, string\n
        :param elims: Restrict to only elimination matches, default False\n
        :param limit: Limits the output length to speed up queries. Max 10,000\n
        :param offset: Skips the first (offset) items when returning\n
        :param fields: List of fields to return. Default is ["all"]\n
        :return: A list of dictionaries, each dictionary including the match, score breakdowns, and predictions\n
        """

        url = "/v1/_matches"

        validate.check_type(year, "int", "year")
        validate.check_type(event, "str", "event")
        validate.check_type(elims, "bool", "elims")
        validate.check_type(limit, "int", "limit")
        validate.check_type(offset, "int", "offset")
        validate.check_type(fields, "list", "fields")

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

    def get_team_match(self, team, match, fields=["all"]):
        """
        Function to retrieve information for a specific (team, match) pair\n
        :param team: Team number, integer\n
        :param match: Match key, string (ex: "2019cur_qm1", "2019cmptx_f1m3")\n
        :param fields: List of fields to return. The default is ["all"]\n
        :return: a dictionary with the team, match, alliance, and then elo\n
        """

        validate.check_type(team, "int", "team")
        validate.check_type(match, "str", "match")
        validate.check_type(fields, "list", "fields")
        url = "/v1/_team_matches?team=" + str(team) + "&match=" + str(match)
        return self._get(url, fields)[0]

    def get_team_matches(
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
        """
        Function to retrieve information on multiple (team, match) pairs\n
        :param team: Restrict by team number, integer\n
        :param year: Restrict by specific year, integer\n
        :param event: Restrict by specific event key, string\n
        :param elims: Restrict to only elimination matches, default False\n
        :param limit: Limits the output length to speed up queries. Max 10,000\n
        :param offset: Skips the first (offset) items when returning\n
        :param fields: List of fields to return. Default is ["all"]\n
        :return: A list of dictionaries, each dictionary including the team, match, alliance, and then elo\n
        """

        url = "/v1/_team_matches"

        validate.check_type(team, "int", "team")
        validate.check_type(year, "int", "year")
        validate.check_type(event, "str", "event")
        validate.check_type(match, "str", "match")
        validate.check_type(elims, "bool", "elims")
        validate.check_type(limit, "int", "limit")
        validate.check_type(offset, "int", "offset")
        validate.check_type(fields, "list", "fields")

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
        return self._get(url, fields)

    def get_event_sim(self, event, index=None, full=False, iterations=None):
        validate.check_type(event, "str", "event")
        validate.check_type(index, "int", "index")
        validate.check_type(full, "bool", "full")
        validate.check_type(iterations, "int", "iterations")

        url = "/v1/event_sim/event/" + event

        if index:
            url += "/index/" + str(index)

        if full:
            url += "/full"
            if iterations:
                if iterations > 100:
                    raise ValueError("Iterations must be <= 100")
                url += "/iterations/" + str(iterations)
        else:
            url += "/simple"

        return self._get(url, fields=["all"])
