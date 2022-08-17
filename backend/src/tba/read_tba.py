import time
from datetime import datetime
from typing import Any, Dict, List

from src.tba.clean_data import (
    clean_district,
    clean_state,
    get_breakdown,
    get_match_time,
)
from src.tba.constants import EVENT_BLACKLIST
from src.tba.main import get_tba


def get_timestamp_from_str(date: str):
    return int(time.mktime(datetime.strptime(date, "%Y-%m-%d").timetuple()))


def get_teams(cache: bool = True) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for i in range(20):
        data = get_tba("teams/" + str(i) + "/simple", cache=cache)
        for data_team in data:
            num = data_team["team_number"]
            district = None
            district_data = get_tba("team/frc" + str(num) + "/districts")
            if district_data is not None and len(district_data) > 0:
                district = district_data[-1]["abbreviation"]
            new_data = {
                "team": num,
                "name": data_team["nickname"],
                "state": clean_state(data_team["state_prov"]),
                "district": clean_district(district),
                "country": data_team["country"],
            }
            out.append(new_data)
    return out


def get_events(year: int, cache: bool = True) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    data = get_tba("events/" + str(year), cache=cache)
    for event in data:
        key = event["key"]

        # filters out partial/missing events
        if key in EVENT_BLACKLIST:
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


def get_event_rankings(event: str, cache: bool = True) -> Dict[int, int]:
    out: Dict[int, int] = {}

    # queries TBA for rankings, some older events are not populated
    try:
        rankings = get_tba("event/" + str(event) + "/rankings", cache=cache)["rankings"]
        for ranking in rankings:
            team_num = int(ranking["team_key"][3:])
            out[team_num] = ranking["rank"]
    except Exception:
        pass

    return out


def get_matches(
    year: int,
    event: str,
    event_time: int,
    cache: bool = True,
) -> List[Dict[str, Any]]:
    m_type = List[Dict[str, Any]]
    out: m_type = []
    matches: m_type = get_tba("event/" + str(event) + "/matches", cache=cache)
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

        if year <= 2004 and (len(red_teams) < 2 or len(blue_teams) < 2):
            continue

        if year > 2004 and (len(red_teams) < 3 or len(blue_teams) < 3):
            continue

        if len(set(red_teams).intersection(set(blue_teams))) > 0:
            continue

        if max([int(x[3:]) for x in red_teams + blue_teams]) >= 9985:
            continue

        breakdown: Dict[str, Any] = match.get("score_breakdown", {}) or {}
        red_breakdown = get_breakdown(year, breakdown.get("red", None))
        blue_breakdown = get_breakdown(year, breakdown.get("blue", None))

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
