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
        if resp.status_code == 200:
            return resp.json()
        raise UserWarning("Invalid Query (large queries do not support metric)")

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

        if page:
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
                      state=None, district=None, metric=None):

        url = "/api/team_events"

        validate.checkType(team, "int", "team")
        validate.checkType(event, "str", "event")
        validate.checkType(metric, "str", "metric")

        if team and event:
            raise UserWarning("Use getTeamEvent() instead")
        if year and event:
            raise UserWarning("Year input will be ignored")
        if team and (country or state or district):
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

        return self._get(url)


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

print(sb.getEvent("2019ncwak"))
print(sb.getEvents(year=2016, district="fnc", metric='elo_top8'))

print(sb.getTeamEvent(team=5511, event="2020ncwak"))
print(sb.getTeamEvents(metric="opr_end"))
