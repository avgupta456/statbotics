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
        return self._get("/api/team/"+str(team))

    def getTeams(self, country=None, state=None, district=None,
                 active=True, metric=None):

        url = "/api/teams"

        if country and district:
            raise ValueError("Cannot specify country and district")
        if state and district:
            raise ValueError("Cannot specify state and district")
        if metric and metric not in validate.getTeamMetrics():
            raise ValueError("Invalid metric")

        if country:
            country = validate.getCountry(country)
            url += "/country/" + country

        if state:
            temp_country, state = validate.getState(country, state)
            if country and temp_country != country:
                raise ValueError("State from different country")
            if not country:
                url += "/country/" + temp_country
            url += "/state/" + state

        if district:
            district = validate.getDistrict(district)
            url += "/district/" + district

        if active:
            url += "/active"

        if metric:
            if metric[0] == "-":
                metric = metric[1:]
            else:
                metric = "-" + metric
            url += "/by/"+metric

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
'''
