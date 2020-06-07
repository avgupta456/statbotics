import requests

'''
Helper class to read the TheBlueAlliance (TBA) API
'''

auth_key = "XeUIxlvO4CPc44NlLE3ncevDg7bAhp6CRy6zC9M2aQb2zGfys0M30eKwavFJSEJr"
read_pre = "https://www.thebluealliance.com/api/v3/"

session = requests.Session()
session.headers.update({'X-TBA-Auth-Key': auth_key, 'X-TBA-Auth-Id': ''})


def get(url):
    return session.get(read_pre+url).json()


def getTeams():
    out = []
    for i in range(20):
        data = get("teams/"+str(i)+"/simple")
        for data_team in data:
            new_data = {
                "num": data_team["team_number"],
                "name": data_team["nickname"],
                "state": data_team["state_prov"],
                "country": data_team["country"]
            }

            if new_data["name"] != "Off-Season Demo Team":
                out.append(new_data)
    return out


def getTeamYears(year):
    out = []
    for i in range(20):
        data = get("teams/"+str(year)+"/"+str(i)+"/simple")
        for data_team in data:
            if data_team["nickname"] != "Off-Season Demo Team":
                out.append({"num": data_team["team_number"]})
    return out
