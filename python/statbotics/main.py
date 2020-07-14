import requests
from cachecontrol import CacheControl


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
