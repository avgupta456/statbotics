import requests
import os

from tba.clean_data import (
    cleanState,
    cleanDistrict,
    getMatchTime,
)

from helper import (
    utils
)


'''
Helper class to read the TheBlueAlliance (TBA) API
'''


class ReadTBA:
    def __init__(self):
        self.auth_key = \
            "XeUIxlvO4CPc44NlLE3ncevDg7bAhp6CRy6zC9M2aQb2zGfys0M30eKwavFJSEJr"
        self.read_pre = "https://www.thebluealliance.com/api/v3/"

        self.session = requests.Session()
        self.session.headers.update({'X-TBA-Auth-Key': self.auth_key,
                                     'X-TBA-Auth-Id': ''})

        self.cache = 0
        self.count = 0

        # some events where no matches were played must be blacklisted
        self.event_blacklist = ["2005va", "2007ga"]

    def get(self, url):
        if os.path.exists("tba/cache/"+url):
            self.cache += 1
            return utils.load_cache("tba/cache/"+url)
        else:
            self.count += 1
            data = self.session.get(self.read_pre+url).json()
            utils.dump_cache("tba/cache/"+url, data)
            return data

    # counts TBA calls
    def getStats(self):
        return [self.count, self.cache]

    def getTeams(self):
        out = []
        for i in range(20):
            data = self.get("teams/"+str(i)+"/simple")
            for data_team in data:
                new_data = {
                    "number": data_team["team_number"],
                    "name": data_team["nickname"],
                    "state": cleanState(data_team["state_prov"]),
                    "country": data_team["country"]
                }
                out.append(new_data)
        return out

    def getTeamYears(self, year):
        out = []
        for i in range(20):
            data = self.get("teams/"+str(year)+"/"+str(i)+"/simple")
            for team in data:
                new_data = {
                    "year": year,
                    "team": team["team_number"],
                }
                out.append(new_data)
        return out

    def getEvents(self, year):
        out = []
        data = self.get("events/"+str(year)+"/simple")
        for event in data:
            key = event["key"]
            if key in self.event_blacklist:
                continue
            if event["district"] is not None:
                event["district"] = event["district"]["abbreviation"]
            if int(event["event_type"]) <= 10:
                # filters out events with no matches
                if len(self.get("event/"+str(key)+"/matches")) == 0:
                    continue
                new_data = {
                    "year": year,
                    "key": key,
                    "name": event["name"],
                    "state": cleanState(event["state_prov"]),
                    "country": event["country"],
                    "district": cleanDistrict(event["district"]),
                    "time": utils.getTime(event["start_date"])
                }
                out.append(new_data)
        return out

    def getTeamEvents(self, event):
        out = []
        data = self.get("event/"+str(event)+"/teams/simple")
        for team in data:
            new_data = {
                "team": team["team_number"],
            }
            out.append(new_data)
        return out

    def getMatches(self, event, event_time):
        out = []
        matches = self.get("event/"+str(event)+"/matches")
        for match in matches:
            # handles issues such as 2005wat qf1 blue alliance
            if len(match["alliances"]["blue"]["team_keys"]) > 0:
                match_data = {
                    "event": event,
                    "key": match["key"],
                    "comp_level": match["comp_level"],
                    "set_number": match["set_number"],
                    "match_number": match["match_number"],
                    "red": ",".join([t[3:] for t in
                                    match["alliances"]["red"]["team_keys"]]),
                    "blue": ",".join([t[3:] for t in
                                     match["alliances"]["blue"]["team_keys"]]),
                    "winner": match["winning_alliance"],
                    "time": getMatchTime(match, event_time),
                    "red_score": match["alliances"]["red"]["score"],
                    "blue_score": match["alliances"]["blue"]["score"],
                    "score_breakdown": match["score_breakdown"]
                }
                out.append(match_data)
        return out

    def getTeamDistrict(self, team):
        teams_info = utils.load("tba/cache/teams_info.p")
        return teams_info[team][3]
