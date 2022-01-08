import os
import time
from datetime import datetime
from typing import Any, Dict, List

from helper.utils import dump_cache, load_cache
from tba.clean_data import clean_district, clean_state, get_breakdown, get_match_time
from tba.config import event_blacklist, get_tba as _get_tba
from tba.fake_matches import (
    elims_complete,
    elims_in_progress,
    quals_complete,
    quals_in_progress,
    schedule_release,
)


def get_timestamp_from_str(date: str):
    return int(time.mktime(datetime.strptime(date, "%Y-%m-%d").timetuple()))


def get_tba(url: str, cache: bool = True) -> Any:
    if cache and os.path.exists("cache/" + url):
        # Cache Hit
        return load_cache("cache/" + url)

    # Cache Miss
    data = _get_tba(url)
    dump_cache("cache/" + url, data)
    return data


def get_teams(cache: bool = True) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for i in range(20):
        data = get_tba("teams/" + str(i) + "/simple", cache=cache)
        for data_team in data:
            new_data = {
                "team": data_team["team_number"],
                "name": data_team["nickname"],
                "state": clean_state(data_team["state_prov"]),
                "country": data_team["country"],
            }
            out.append(new_data)
    return out


def get_team_years(year: int, cache: bool = True) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for i in range(20):
        data = get_tba("teams/" + str(year) + "/" + str(i) + "/simple", cache=cache)
        for team in data:
            new_data = {"year": year, "team": team["team_number"]}
            out.append(new_data)
    return out


def get_events(year: int, cache: bool = True) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    data = get_tba("events/" + str(year), cache=cache)
    for event in data:
        key = event["key"]

        # filters out partial/missing events
        if key in event_blacklist:
            continue

        # filters out offseason events
        if int(event["event_type"]) > 10:
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

        # filter out incomplete events
        if "week" not in event or event["week"] is None:
            continue

        # bug in TBA API
        if type < 3 and year != 2016:
            event["week"] += 1

        out.append(
            {
                "year": year,
                "key": key,
                "name": event["name"],
                "state": clean_state(event["state_prov"]),
                "country": event["country"],
                "district": clean_district(event["district"]),
                "time": get_timestamp_from_str(event["start_date"]),
                "type": type,
                "week": event["week"],
            }
        )

    return out


def get_team_events(event: str, cache: bool = True) -> List[Dict[str, Any]]:
    out: Dict[int, Dict[str, Any]] = {}
    data = get_tba("event/" + str(event) + "/teams/simple", cache=cache)
    for team in data:
        team_num = team["team_number"]
        new_data = {"team": team_num, "rank": -1}
        out[team_num] = new_data

    # queries TBA for rankings, some older events are not populated
    try:
        rankings = get_tba("event/" + str(event) + "/rankings", cache=cache)["rankings"]
        for ranking in rankings:
            team_num = int(ranking["team_key"][3:])
            out[team_num]["rank"] = ranking["rank"]
    except Exception:
        pass

    return list(out.values())


def get_matches(
    year: int,
    event: str,
    event_time: int,
    cache: bool = True,
    teams: List[int] = [],  # solely for fake_matches
    fake_matches: int = 0,  # solely for fake_matches
) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    if fake_matches == 1:
        matches = schedule_release(event, teams)
    elif fake_matches == 2:
        matches = quals_in_progress(event, teams, last_qual=30)
    elif fake_matches == 3:
        matches = quals_complete(event, teams)
    elif fake_matches == 4:
        matches = elims_in_progress(event, teams, last_elim=10)
    elif fake_matches == 5:
        matches = elims_complete(event, teams)
    else:
        matches = get_tba("event/" + str(event) + "/matches", cache=cache)
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

        if len(set(red_teams).intersection(set(blue_teams))) > 0:
            continue

        breakdown = match["score_breakdown"]
        if breakdown is None or year < 2016:
            red_breakdown, blue_breakdown = get_breakdown(year), get_breakdown(year)
        else:
            red_breakdown = get_breakdown(year, breakdown["red"])
            blue_breakdown = get_breakdown(year, breakdown["blue"])

        match_data: Dict[str, Any] = {
            "event": event,
            "key": match["key"],
            "comp_level": match["comp_level"],
            "set_number": match["set_number"],
            "match_number": match["match_number"],
            "status": "Completed" if min(red_score, blue_score) >= 0 else "Upcoming",
            "red": ",".join([t[3:] for t in red_teams]),
            "blue": ",".join([t[3:] for t in blue_teams]),
            "winner": winner,
            "time": get_match_time(match, event_time),
            "red_score": red_score,
            "blue_score": blue_score,
            "red_score_breakdown": red_breakdown,
            "blue_score_breakdown": blue_breakdown,
        }
        out.append(match_data)
    return out
