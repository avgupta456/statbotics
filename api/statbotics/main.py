from typing import Any, Dict, List, Optional, Union

import requests
from cachecontrol import CacheControl  # type: ignore

from .validate import check_type, get_locations, get_type
from .constants import (
    event_metrics,
    match_metrics,
    team_event_metrics,
    team_match_metrics,
    team_metrics,
    team_year_metrics,
    year_metrics,
)


class Statbotics:
    """
    Main Object for interfacing with the Statbotics API
    """

    def __init__(self):
        self.BASE_URL = "https://api.statbotics.io/v3"
        # self.BASE_URL = "http://localhost:8000/v3"
        self.session = CacheControl(requests.Session())

    def _filter_singular(
        self, data: Dict[str, Any], fields: List[str]
    ) -> Dict[str, Any]:
        if fields == ["all"]:
            return data

        for field in fields:
            if field not in data:
                raise ValueError(
                    f"Invalid field: {field}. Available fields: {data.keys()}"
                )

        return {field: data[field] for field in fields}

    def _filter_plural(
        self, data: List[Dict[str, Any]], fields: List[str]
    ) -> List[Dict[str, Any]]:
        if fields == ["all"]:
            return data

        for field in fields:
            if field not in data[0]:
                raise ValueError(
                    f"Invalid field: {field}. Available fields: {data[0].keys()}"
                )

        return [{field: entry[field] for field in fields} for entry in data]

    def _get_singular(
        self, url: str, fields: List[str], retry: int = 0
    ) -> Dict[str, Any]:
        resp = self.session.get(self.BASE_URL + url)
        if resp.status_code != 200:
            if retry < 2:
                return self._get_singular(url, fields, retry=retry + 1)
            raise UserWarning("Invalid query: " + url)

        data: Dict[str, Any] = resp.json()

        if data == {}:
            raise UserWarning("Invalid inputs, no data recieved for " + url)

        return self._filter_singular(data, fields)

    def _get_plural(
        self, url: str, fields: List[str], retry: int = 0
    ) -> List[Dict[str, Any]]:
        resp = self.session.get(self.BASE_URL + url)
        if resp.status_code != 200:
            if retry < 2:
                return self._get_plural(url, fields, retry=retry + 1)
            raise UserWarning("Invalid query: " + url)

        data: List[Dict[str, Any]] = resp.json()

        if data == []:
            raise UserWarning("Invalid inputs, no data recieved for " + url)

        return self._filter_plural(data, fields)

    def get_team(self, team: int, fields: List[str] = ["all"]) -> Dict[str, Any]:
        """
        Function to retrieve information on an individual team\n
        :param team: Team Number, integer\n
        :param fields: List of fields to return. The default is ["all"]\n
        :return: a dictionary with team metadata and EPA statistics\n
        """

        check_type(team, "int", "team")
        check_type(fields, "list", "fields")
        return self._get_singular("/team/" + str(team), fields)

    def get_teams(
        self,
        country: Optional[str] = None,
        state: Optional[str] = None,
        district: Optional[str] = None,
        active: Optional[bool] = True,
        metric: str = "team",
        ascending: Optional[bool] = None,
        limit: int = 100,
        offset: int = 0,
        fields: List[str] = ["all"],
    ) -> List[Dict[str, Any]]:
        """
        Function to retrieve information on multiple teams\n
        :param country: Restrict based on country (select country to include)\n
        :param state: US States and Canada provinces only. Can infer country.\n
        :param district: Use 2 or 3-letter key (ex: FIM, NE, etc)\n
        :param active: Restrict to active teams (played most recent season)\n
        :param metric: Order output by field (Ex: "-norm_epa", "team", etc). Default is "team".\n
        :param ascending: Order output ascending or descending. Default varies by metric.\n
        :param limit: Limits the output length to speed up queries. Max 10,000\n
        :param offset: Skips the first (offset) items when returning\n
        :param fields: List of fields to return. Default is ["all"]\n
        :return: A list of dictionaries, each dictionary including team metadata and EPA statistics\n
        """

        url = "/teams"

        check_type(metric, "str", "metric")
        check_type(limit, "int", "limit")
        check_type(offset, "int", "offset")
        check_type(fields, "list", "fields")

        if limit > 10000:
            raise ValueError("Please reduce 'limit', max is 10,000.")
        url += "?limit=" + str(limit) + "&offset=" + str(offset)

        url += get_locations(country, state, district)

        if active is not None:
            url += "&active=" + str(active)

        if metric not in team_metrics:
            raise ValueError("Invalid metric")
        if ascending is None:
            ascending = True if metric in ["team", "losses"] else False
        url += "&metric=" + metric + "&ascending=" + str(ascending)

        return self._get_plural(url, fields)

    def get_year(self, year: int, fields: List[str] = ["all"]) -> Dict[str, Any]:
        """
        Function to retrieve information for a specific year\n
        :param year: Year, integer\n
        :param fields: List of fields to return. The default is ["all"]\n
        :return: a dictionary with the year, match prediction statistics, and RP prediction statistics\n
        """

        check_type(year, "int", "year")
        check_type(fields, "list", "fields")
        return self._get_singular("/year/" + str(year), fields)

    def get_years(
        self,
        metric: str = "year",
        ascending: Optional[bool] = None,
        limit: int = 100,
        offset: int = 0,
        fields: List[str] = ["all"],
    ) -> List[Dict[str, Any]]:
        """
        Function to retrieve information on multiple years\n
        :param metric: Order output by field. (Ex: "epa_acc", "epa_mse", etc). Default "year"\n
        :param ascending: Order output ascending or descending. Default varies by metric.\n
        :param limit: Limits the output length to speed up queries. Max 10,000\n
        :param offset: Skips the first (offset) items when returning\n
        :param fields: List of fields to return. Default is ["all"]\n
        :return: A list of dictionaries, each dictionary including the year and match/RP prediction statistics\n
        """

        check_type(metric, "str", "metric")
        check_type(limit, "int", "limit")
        check_type(offset, "int", "offset")
        check_type(fields, "list", "fields")
        url = "/years?limit=" + str(limit) + "&offset=" + str(offset)

        if metric not in year_metrics:
            raise ValueError("Invalid metric")
        if ascending is None:
            ascending = True if metric in ["year"] else False
        url += "&metric=" + metric + "&ascending=" + str(ascending)

        return self._get_plural(url, fields)

    def get_team_year(
        self, team: int, year: int, fields: List[str] = ["all"]
    ) -> Dict[str, Any]:
        """
        Function to retrieve information for a specific team's performance in a specific year\n
        :param team: Team number, integer\n
        :param year: Year, integer\n
        :param fields: List of fields to return. The default is ["all"]\n
        :return: a dictionary with the team, year, and EPA statistics\n
        """

        check_type(team, "int", "team")
        check_type(year, "int", "year")
        check_type(fields, "list", "fields")
        url = "/team_year/" + str(team) + "/" + str(year)
        return self._get_singular(url, fields)

    def get_team_years(
        self,
        team: Optional[int] = None,
        year: Optional[int] = None,
        country: Optional[str] = None,
        state: Optional[str] = None,
        district: Optional[str] = None,
        metric: str = "team",
        ascending: Optional[bool] = None,
        limit: int = 100,
        offset: int = 0,
        fields: List[str] = ["all"],
    ) -> List[Dict[str, Any]]:
        """
        Function to retrieve information on multiple (team, year) pairs\n
        :param team: Restrict based on a specific team number\n
        :param country: Restrict based on country (select countries included)\n
        :param state: US States and Canada provinces only. Can infer country.\n
        :param district: Use 2 or 3-letter key (ex: FIM, NE, etc)\n
        :param metric: Order output by field. (Ex: "epa_end", "team", etc). Default "team"\n
        :param ascending: Order output ascending or descending. Default varies by metric.\n
        :param limit: Limits the output length to speed up queries. Max 10,000\n
        :param offset: Skips the first (offset) items when returning\n
        :param fields: List of fields to return. Default is ["all"]\n
        :return: A list of dictionaries, each dictionary including the team, year, and EPA statistics\n
        """

        url = "/team_years"

        check_type(team, "int", "team")
        check_type(year, "int", "year")
        check_type(metric, "str", "metric")
        check_type(limit, "int", "limit")
        check_type(offset, "int", "offset")
        check_type(fields, "list", "fields")

        if limit > 10000:
            raise ValueError("Please reduce 'limit', max is 10,000.")
        url += "?limit=" + str(limit) + "&offset=" + str(offset)

        if team and year:
            raise UserWarning("Use get_team_year() instead")
        if team is not None:
            url += "&team=" + str(team)
        if year is not None:
            url += "&year=" + str(year)

        if team and (country or state or district):
            raise UserWarning("Conflicting location input")
        url += get_locations(country, state, district)

        if metric not in team_year_metrics:
            raise ValueError("Invalid metric")
        if ascending is None:
            ascending = True if metric in ["team", "year"] else False
        url += "&metric=" + metric + "&ascending=" + str(ascending)

        return self._get_plural(url, fields)

    def get_event(self, event: str, fields: List[str] = ["all"]) -> Dict[str, Any]:
        """
        Function to retrieve information for a specific event\n
        :param event: Event key, string (ex: "2019cur")\n
        :param fields: List of fields to return. The default is ["all"]\n
        :return: a dictionary with the event and EPA statistics\n
        """

        check_type(event, "str", "event")
        check_type(fields, "list", "fields")
        url = "/event/" + event
        return self._get_singular(url, fields)

    def get_events(
        self,
        year: Optional[int] = None,
        country: Optional[str] = None,
        state: Optional[str] = None,
        district: Optional[str] = None,
        type: Optional[Union[int, str]] = None,
        week: Optional[int] = None,
        metric: str = "year",
        ascending: Optional[bool] = None,
        limit: int = 100,
        offset: int = 0,
        fields: List[str] = ["all"],
    ) -> List[Dict[str, Any]]:
        """
        Function to retrieve information on multiple events\n
        :param year: Restrict by specific year, integer\n
        :param country: Restrict based on country (select countries included)\n
        :param state: US States and Canada provinces only. Can infer country.\n
        :param district: Use 2 or 3-letter key (ex: FIM, NE, etc)\n
        :param type: 0=regional, 1=district, 2=district champ, 3=champs, 4=einstein\n
        :param week: Week of play, generally between 0 and 8\n
        :param metric: Order output bu field. (Ex: "epa_pre_playoffs", "epa_end", etc). Default "year"\n
        :param ascending: Order output ascending or descending. Default varies by metric.\n
        :param limit: Limits the output length to speed up queries. Max 10,000\n
        :param offset: Skips the first (offset) items when returning\n
        :param fields: List of fields to return. Default is ["all"]\n
        :return: A list of dictionaries, each dictionary including the team, event and EPA statistics\n
        """

        url = "/events"

        check_type(year, "int", "year")
        check_type(metric, "str", "metric")
        type = get_type(type)
        check_type(week, "int", "week")
        check_type(limit, "int", "limit")
        check_type(offset, "int", "offset")
        check_type(fields, "list", "fields")

        if limit > 10000:
            raise ValueError("Please reduce 'limit', max is 10,000.")
        url += "?limit=" + str(limit) + "&offset=" + str(offset)

        if year is not None:
            url += "&year=" + str(year)

        url += get_locations(country, state, district)

        if type is not None:
            url += "&type=" + str(type)

        if week is not None:
            url += "&week=" + str(week)

        if metric not in event_metrics:
            raise ValueError("Invalid metric")
        if ascending is None:
            ascending = True if metric in ["year", "week"] else False
        url += "&metric=" + metric + "&ascending=" + str(ascending)

        return self._get_plural(url, fields)

    def get_team_event(
        self, team: int, event: str, fields: List[str] = ["all"]
    ) -> Dict[str, Any]:
        """
        Function to retrieve information for a specific (team, event) pair\n
        :param team: Team number, integer\n
        :param event: Event key, string (ex: "2019cur")\n
        :param fields: List of fields to return. The default is ["all"]\n
        :return: a dictionary with the event and EPA statistics\n
        """

        check_type(team, "int", "team")
        check_type(event, "str", "event")
        check_type(fields, "list", "fields")
        url = "/team_event/" + str(team) + "/" + event
        return self._get_singular(url, fields)

    def get_team_events(
        self,
        team: Optional[int] = None,
        year: Optional[int] = None,
        event: Optional[str] = None,
        country: Optional[str] = None,
        state: Optional[str] = None,
        district: Optional[str] = None,
        type: Optional[Union[int, str]] = None,
        week: Optional[int] = None,
        metric: str = "year",
        ascending: Optional[bool] = None,
        limit: int = 00,
        offset: int = 0,
        fields: List[str] = ["all"],
    ) -> List[Dict[str, Any]]:
        """
        Function to retrieve information on multiple (team, event) pairs\n
        :param team: Restrict by team number, integer\n
        :param year: Restrict by specific year, integer\n
        :param country: Restrict based on country (select countries included)\n
        :param state: US States and Canada provinces only. Can infer country.\n
        :param district: Use 2 or 3-letter key (ex: FIM, NE, etc)\n
        :param type: 0=regional, 1=district, 2=district champ, 3=champs, 4=einstein\n
        :param week: Week of play, generally between 0 and 8\n
        :param metric: Order output by field. (Ex: "epa_pre_playoffs", "epa_end", etc). Default "year"\n
        :param ascending: Order output ascending or descending. Default varies by metric.\n
        :param limit: Limits the output length to speed up queries. Max 10,000\n
        :param offset: Skips the first (offset) items when returning\n
        :param fields: List of fields to return. Default is ["all"]\n
        :return: A list of dictionaries, each dictionary including the team, event and EPA statistics\n
        """

        url = "/team_events"

        check_type(team, "int", "team")
        check_type(event, "str", "event")
        type = get_type(type)
        check_type(week, "int", "week")
        check_type(metric, "str", "metric")
        check_type(limit, "int", "limit")
        check_type(offset, "int", "offset")
        check_type(fields, "list", "fields")

        if limit > 10000:
            raise ValueError("Please reduce 'limit', max is 10,000.")
        url += "?limit=" + str(limit) + "&offset=" + str(offset)

        if team and event:
            raise UserWarning("Use get_team_event() instead")
        if team is not None:
            url += "&team=" + str(team)
        if year is not None:
            url += "&year=" + str(year)

        if event and (year or type or week):
            raise UserWarning("Overconstrained query")
        url += get_locations(country, state, district)

        if (team or event) and (country or state or district):
            raise UserWarning("Conflicting location input")
        if event is not None:
            url += "&event=" + event

        if type is not None:
            url += "&type=" + str(type)

        if week is not None:
            url += "&week=" + str(week)

        if metric not in team_event_metrics:
            raise ValueError("Invalid metric")
        if ascending is None:
            ascending = True if metric in ["year", "week"] else False
        url += "&metric=" + metric + "&ascending=" + str(ascending)

        return self._get_plural(url, fields)

    def get_match(self, match: str, fields: List[str] = ["all"]) -> Dict[str, Any]:
        """
        Function to retrieve information for a specific match\n
        :param match: Match key, string (ex: "2019cur_qm1", "2019cmptx_f1m3")\n
        :param fields: List of fields to return. The default is ["all"]\n
        :return: a dictionary with the match, score breakdowns, and predictions\n
        """

        check_type(match, "str", "match")
        check_type(fields, "list", "fields")
        return self._get_singular("/match/" + match, fields)

    def get_matches(
        self,
        team: Optional[int] = None,
        year: Optional[int] = None,
        event: Optional[str] = None,
        week: Optional[int] = None,
        elims: Optional[bool] = None,
        metric: str = "time",
        ascending: Optional[bool] = None,
        limit: int = 200,
        offset: int = 0,
        fields: List[str] = ["all"],
    ) -> List[Dict[str, Any]]:
        """
        Function to retrieve information on multiple matches\n
        :param team: Restrict by team number, integer\n
        :param year: Restrict by specific year, integer\n
        :param event: Restrict by specific event key, string\n
        :param week: Week of play, generally between 0 and 8\n
        :param elims: Restrict to only elimination matches, default False\n
        :param metric: Order output by field. (Ex: "time", "epa_pre_playoffs", "epa_end", etc). Default "time"\n
        :param ascending: Order output ascending or descending. Default varies by metric.\n
        :param limit: Limits the output length to speed up queries. Max 10,000\n
        :param offset: Skips the first (offset) items when returning\n
        :param fields: List of fields to return. Default is ["all"]\n
        :return: A list of dictionaries, each dictionary including the match, score breakdowns, and predictions\n
        """

        url = "/matches"

        check_type(team, "int", "team")
        check_type(year, "int", "year")
        check_type(event, "str", "event")
        check_type(week, "int", "week")
        check_type(elims, "bool", "elims")
        check_type(limit, "int", "limit")
        check_type(offset, "int", "offset")
        check_type(fields, "list", "fields")

        if limit > 10000:
            raise ValueError("Please reduce 'limit', max is 10,000.")
        url += "?limit=" + str(limit) + "&offset=" + str(offset)

        if not event and not year and not team:
            raise UserWarning("Query too large, be more specific (event)")

        if year and event:
            raise UserWarning("Year input will be ignored")

        if team is not None:
            url += "&team=" + str(team)
        if year is not None:
            url += "&year=" + str(year)
        if event is not None:
            url += "&event=" + event
        if week is not None:
            url += "&week=" + str(week)
        if elims is not None:
            url += "&elims=" + str(elims)

        if metric not in match_metrics:
            raise ValueError("Invalid metric")
        if ascending is None:
            ascending = True if metric in ["time"] else False
        url += "&metric=" + metric + "&ascending=" + str(ascending)

        return self._get_plural(url, fields)

    def get_team_match(
        self, team: int, match: str, fields: List[str] = ["all"]
    ) -> Dict[str, Any]:
        """
        Function to retrieve information for a specific (team, match) pair\n
        :param team: Team number, integer\n
        :param match: Match key, string (ex: "2019cur_qm1", "2019cmptx_f1m3")\n
        :param fields: List of fields to return. The default is ["all"]\n
        :return: a dictionary with the team, match, alliance, and EPA statistics\n
        """

        check_type(team, "int", "team")
        check_type(match, "str", "match")
        check_type(fields, "list", "fields")
        url = "/team_match/" + str(team) + "/" + str(match)
        return self._get_singular(url, fields)

    def get_team_matches(
        self,
        team: Optional[int] = None,
        year: Optional[int] = None,
        event: Optional[str] = None,
        match: Optional[str] = None,
        week: Optional[int] = None,
        elims: Optional[bool] = None,
        metric: str = "time",
        ascending: Optional[bool] = None,
        limit: int = 100,
        offset: int = 0,
        fields: List[str] = ["all"],
    ) -> List[Dict[str, Any]]:
        """
        Function to retrieve information on multiple (team, match) pairs\n
        :param team: Restrict by team number, integer\n
        :param year: Restrict by specific year, integer\n
        :param event: Restrict by specific event key, string\n
        :param week: Week of play, generally between 0 and 8\n
        :param elims: Restrict to only elimination matches, default False\n
        :param metric: Order output by field. (Ex: "time", "auto_epa", etc). Default "time"\n
        :param ascending: Order output ascending or descending. Default varies by metric.\n
        :param limit: Limits the output length to speed up queries. Max 10,000\n
        :param offset: Skips the first (offset) items when returning\n
        :param fields: List of fields to return. Default is ["all"]\n
        :return: A list of dictionaries, each dictionary including the team, match, alliance, and then elo\n
        """

        url = "/team_matches"

        check_type(team, "int", "team")
        check_type(year, "int", "year")
        check_type(event, "str", "event")
        check_type(week, "int", "week")
        check_type(match, "str", "match")
        check_type(elims, "bool", "elims")
        check_type(limit, "int", "limit")
        check_type(offset, "int", "offset")
        check_type(fields, "list", "fields")

        if limit > 10000:
            raise ValueError("Please reduce 'limit', max is 10,000.")
        url += "?limit=" + str(limit) + "&offset=" + str(offset)

        if not year and not event and not match and not week:
            raise UserWarning(
                "Query too large, be more specific (year, week, event, or match)"
            )

        if (
            (year and event)
            or (year and match)
            or (event and match)
            or (event and week)
            or (match and week)
        ):
            raise UserWarning("Only specify one of (year, week, event, match)")

        if team is not None:
            url += "&team=" + str(team)
        if year is not None:
            url += "&year=" + str(year)
        if event is not None:
            url += "&event=" + event
        if week is not None:
            url += "&week=" + str(week)
        if match is not None:
            url += "&match=" + match
        if elims is not None:
            url += "&elims=" + str(elims)

        if metric not in team_match_metrics:
            raise ValueError("Invalid metric")
        if ascending is None:
            ascending = True if metric in ["time"] else False
        url += "&metric=" + metric + "&ascending=" + str(ascending)

        return self._get_plural(url, fields)
