from typing import Any, Dict, List, Optional

import requests
from cachecontrol import CacheControl  # type: ignore

from .validate import check_type, get_locations
from .constants import team_metrics


class Statbotics:
    """
    Main Object for interfacing with the Statbotics API
    """

    def __init__(self):
        # self.BASE_URL = "https://api.statbotics.io/v2"
        self.BASE_URL = "http://localhost:8000/v2"
        self.session = CacheControl(requests.Session())

    def _filter_singular(
        self, data: Dict[str, Any], fields: List[str]
    ) -> Dict[str, Any]:
        if fields == ["all"]:
            return data

        for field in fields:
            if field not in data:
                raise ValueError("Invalid field: " + str(field))

        return {field: data[field] for field in fields}

    def _filter_plural(
        self, data: List[Dict[str, Any]], fields: List[str]
    ) -> List[Dict[str, Any]]:
        if fields == ["all"]:
            return data

        for field in fields:
            if field not in data[0]:
                raise ValueError("Invalid field: " + str(field))

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

    def _negate(self, string: str) -> str:
        if len(string) == 0:
            return string
        return string[1:] if string[0] == "-" else "-" + string

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
        limit: int = 1000,
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

        if active:
            url += "&active=True"

        if metric not in team_metrics:
            raise ValueError("Invalid metric")
        if ascending is None:
            ascending = True if metric in ["team", "losses"] else False
        url += "&metric=" + metric + "&ascending=" + str(ascending)

        return self._get_plural(url, fields)
