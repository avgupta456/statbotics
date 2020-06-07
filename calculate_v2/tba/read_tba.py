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


# Todo: get district
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


# Todo: get district
def getTeamYears(year):
    out = []
    for i in range(20):
        data = get("teams/"+str(year)+"/"+str(i)+"/simple")
        for team in data:
            if team["nickname"] != "Off-Season Demo Team":
                out.append({"num": team["team_number"]})
    return out


def getEvents(year):
    out = []
    data = get("events/"+str(year)+"/simple")
    for event in data:
        if int(event["event_type"]) <= 10:
            event_data = {
                "key": event["key"],
                "name": event["name"],
                "state": event["state_prov"],
                "country": event["country"],
                "district": event["district"],
                "start_date": event["start_date"],
                "end_date": event["end_date"],
            }
            out.append(event_data)
    return out


def getTeamEvents(event):
    out = []
    data = get("event/"+str(event)+"/teams/simple")
    for team in data:
        out.append({"num": team["team_number"]})
    return out


def getMatches(event):
    out = []
    matches = get("event/"+str(event)+"/matches")
    for match in matches:
        match_data = {
            "key": match["key"],
            "comp_level": match["comp_level"],
            "set_number": match["set_number"],
            "match_number": match["match_number"],
            "red": [int(t[3:]) for t in
                    match["alliances"]["red"]["team_keys"]],
            "blue": [int(t[3:]) for t in
                     match["alliances"]["blue"]["team_keys"]],
            "winner": match["winning_alliance"],
            "time": match["actual_time"],
            "score_breakdown": match["score_breakdown"]
        }
        out.append(match_data)
    return out
