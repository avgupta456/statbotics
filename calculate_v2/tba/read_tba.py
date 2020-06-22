import requests
import os

from tba.clean_data import (
    cleanState,
    cleanDistrict,
    getMatchTime,
    getBreakdown,
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

    def get(self, url, cache=True):
        if cache and os.path.exists("tba/cache/"+url):
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

    def getTeams(self, cache=True):
        out = []
        for i in range(20):
            data = self.get("teams/"+str(i)+"/simple", cache=cache)
            for data_team in data:
                new_data = {
                    "number": data_team["team_number"],
                    "name": data_team["nickname"],
                    "state": cleanState(data_team["state_prov"]),
                    "country": data_team["country"]
                }
                out.append(new_data)
        return out

    def getTeamYears(self, year, cache=True):
        out = []
        for i in range(20):
            data = self.get("teams/"+str(year)+"/"+str(i)+"/simple",
                            cache=cache)
            for team in data:
                new_data = {
                    "year": year,
                    "team": team["team_number"],
                }
                out.append(new_data)
        return out

    def getEvents(self, year, cache=True):
        out = []
        data = self.get("events/"+str(year), cache=cache)
        # print(len(data))
        for event in data:
            key = event["key"]

            # filters out partial/missing events
            if key in self.event_blacklist:
                continue
            # filters out offseason events
            if int(event["event_type"]) > 10:
                continue
            # filters out events with no matches
            if len(self.get("event/"+str(key)+"/matches", cache=cache)) == 0:
                continue

            if event["district"] is not None:
                event["district"] = event["district"]["abbreviation"]

            # renames district divisions to district championship
            # renames festival of championships to einsteins
            type = event["event_type"]
            if type == 5:
                type = 2
            if type == 6:
                type = 4

            # assigns worlds to week 8
            if type >= 3:
                event["week"] = 8

            out.append({
                "year": year,
                "key": key,
                "name": event["name"],
                "state": cleanState(event["state_prov"]),
                "country": event["country"],
                "district": cleanDistrict(event["district"]),
                "time": utils.getTime(event["start_date"]),
                "type": type,
                "week": event["week"],
            })
        # print(len(out))
        return out

    def getTeamEvents(self, event, cache=True):
        out = []
        data = self.get("event/"+str(event)+"/teams/simple", cache=cache)
        for team in data:
            new_data = {
                "team": team["team_number"],
            }
            out.append(new_data)
        return out

    def getMatches(self, year, event, event_time, cache=True):
        out = []
        matches = self.get("event/"+str(event)+"/matches", cache=cache)
        for match in matches:
            red_teams = match["alliances"]["red"]["team_keys"]
            blue_teams = match["alliances"]["blue"]["team_keys"]
            red_score = match["alliances"]["red"]["score"]
            blue_score = match["alliances"]["blue"]["score"]
            winner = "draw"
            if red_score > blue_score:
                winner = "red"
            elif blue_score > red_score:
                winner = "blue"

            if year > 2004 and (len(red_teams) < 3 or len(blue_teams) < 3):
                continue
            if year <= 2004 and (len(red_teams) < 2 or len(blue_teams) < 2):
                continue

            # handles elims in 2 team alliance era
            if year <= 2004:
                red_teams = red_teams[:2]
                blue_teams = blue_teams[:2]

            breakdown = match["score_breakdown"]
            if breakdown is None or year < 2016:
                red_breakdown, blue_breakdown = getBreakdown(), getBreakdown()
            else:
                red_breakdown = getBreakdown(breakdown["red"], year)
                blue_breakdown = getBreakdown(breakdown["blue"], year)

            match_data = {
                "event": event,
                "key": match["key"],
                "comp_level": match["comp_level"],
                "set_number": match["set_number"],
                "match_number": match["match_number"],
                "red": ",".join([t[3:] for t in red_teams]),
                "blue": ",".join([t[3:] for t in blue_teams]),
                "winner": winner,
                "time": getMatchTime(match, event_time),
                "red_score": red_score,
                "blue_score": blue_score,
                "red_score_breakdown": red_breakdown,
                "blue_score_breakdown": blue_breakdown
            }
            out.append(match_data)
        # print(len(out))
        return out

    def getTeamDistrict(self, team):
        teams_info = utils.load("tba/cache/teams_info.p")
        return teams_info[team][3]
