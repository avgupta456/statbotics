import requests
from cachecontrol import CacheControl

import validate


class Statbotics():
    def __init__(self):
        self.BASE_URL = "https://backend.statbotics.io"
        self.session = CacheControl(requests.Session())
        self.login(self.getToken())
        self.token = self.getToken()

    def getToken(self):
        self.session.get(self.BASE_URL+"/admin/")
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
        if resp.status_code != 200:
            print("Something Went Wrong")
        else:
            return resp.json()

    def getTeam(self, team):
        if not isinstance(team, int):
            raise TypeError("'team' must be an integer")
        return self._get("/api/team/"+str(team))

    def getTeams(self, country=None, state=None, district=None,
                 active=True, metric=None):
        if country and not isinstance(country, str):
            raise TypeError("'country' must be a string")
        if state and not isinstance(state, str):
            raise TypeError("'state' must be a string")
        if district and not isinstance(district, str):
            raise TypeError("'district' must be a string")
        if metric and not isinstance(metric, str):
            raise TypeError("'metric' must be a string")

        url = "/api/teams" + validate.getLocations(country, state, district)

        if active:
            url += "/active"

        if metric:
            if metric not in validate.getTeamMetrics():
                raise ValueError("Invalid metric")
            if metric[0] == "-":
                metric = metric[1:]
            else:
                metric = "-" + metric
            url += "/by/" + metric

        return self._get(url)

    def getYear(self, year):
        if not isinstance(year, int):
            raise TypeError("'year' must be an integer")
        if year not in range(2002, 2021):
            raise ValueError("Enter valid year (2002-Present)")
        return self._get("/api/year/"+str(year))

    def getYears(self):
        return self._get("/api/years")

    def getTeamYear(self, team, year):
        if not isinstance(team, int):
            raise TypeError("'team' must be an integer")
        if not isinstance(year, int):
            raise TypeError("'year' must be an integer")
        if year not in range(2002, 2021):
            raise ValueError("Enter valid year (2002-Present)")
        return self._get("/api/team_year/team/"+str(team)+"/year/"+str(year))

    def getTeamYears(self, team=None, year=None, country=None, state=None,
                     district=None, metric=None, page=None):
        url = "/api/team_years"

        if team and year:
            raise UserWarning("Use getTeamYear() instead")
        if team and (country or state or district):
            raise UserWarning("Location zone disregarded")

        if team and not isinstance(team, int):
            raise TypeError("'team' must be an integer")
        if year and not isinstance(year, int):
            raise TypeError("'year' must be an integer")
        if country and not isinstance(country, str):
            raise TypeError("'country' must be a string")
        if state and not isinstance(state, str):
            raise TypeError("'state' must be a string")
        if district and not isinstance(district, str):
            raise TypeError("'district' must be a string")
        if metric and not isinstance(metric, str):
            raise TypeError("'metric' must be a string")
        if page and not isinstance(page, int):
            raise TypeError("'page' must be an integer")

        if team:
            url += "/team/" + str(team)

        if year:
            if year not in range(2002, 2021):
                raise ValueError("Enter valid year (2002-Present)")
            url += "/year/" + str(year)

        url += validate.getLocations(country, state, district)

        if metric:
            if metric not in validate.getTeamYearMetrics():
                raise ValueError("Invalid metric")
            if metric[0] == "-":
                metric = metric[1:]
            else:
                metric = "-" + metric
            url += "/by/" + metric

        if page:
            url += "/page/" + str(page)

        return self._get(url)


'''
sb = Statbotics()
nc_teams = sb.getTeams(state="north carolina", metric="elo")
for team in nc_teams[:10]:
    print(team['team'], team['elo'])
print()

ca_teams = sb.getTeams(state="CA", metric="elo")
for team in ca_teams[:30]:
    print(team['team'], team['elo'])
print()

print(sb.getYear(2019))
print(sb.getYears())

print(sb.getTeamYear(team=5511, year=2019))
print(sb.getTeamYears(state="NC", year=2004))
'''
