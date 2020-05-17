import math
import requests
import datetime

from classes import Match
import utils

'''
Helper class to read the TheBlueAlliance (TBA) API
'''

auth_key = "V3FDGbXKFVDRWOeHmotTdbOFBMZPvwG5VulPsEXFwZ5tI6hxK6FbCgOm200OKLm7"
read_pre = "https://www.thebluealliance.com/api/v3/"

session = requests.Session()
session.headers.update({'X-TBA-Auth-Key': auth_key, 'X-TBA-Auth-Id': ''})

def get(url): return session.get(read_pre+url).json()

def getEvents(year=2020):
    events = []
    for event in get("events/"+str(year)+"/simple"):
        if(event["event_type"]<=10): events.append(event["key"])
    return events

def getEventTime(event):
    date = get("event/"+str(event)+"/simple")["start_date"] #for pre 2016 events
    return int(datetime.datetime.strptime(date, "%Y-%m-%d").timestamp())

def getMatches(event):
    matches = []
    time = getEventTime(event)
    for match in get("event/"+str(event)+"/matches/simple"):
        if(match["actual_time"]==None):
            new_time = time+200*match["set_number"]+match["match_number"]
            match["actual_time"] = new_time #correctly orders matches pre 2016
        red_teams = len(match["alliances"]["red"]["team_keys"])
        blue_teams = len(match["alliances"]["blue"]["team_keys"])
        if(red_teams==3 and blue_teams==3): matches.append(Match(match))
    return matches

def saveMatches(year):
    matches = []
    events = getEvents(year)

    for event in events:
        print(event)
        for match in getMatches(event):
            matches.append(match)

    matches.sort()
    utils.saveMatches(year, matches)

def main():
    for year in range(2005,2021):
        saveMatches(year)

if __name__ == "__main__":
    main()
