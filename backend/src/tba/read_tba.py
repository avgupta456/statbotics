import time
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

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


def get_district(team: int) -> Optional[str]:
    query_str = "team/frc" + str(team) + "/districts"
    district_data, _ = get_tba(query_str, etag=None, cache=True)
    if type(district_data) is bool or district_data is None or len(district_data) == 0:
        return None
    return district_data[0]["abbreviation"]


def get_teams(cache: bool = True) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for i in range(20):
        data, _ = get_tba("teams/" + str(i) + "/simple", etag=None, cache=cache)
        if type(data) is bool:
            continue
        for data_team in data:
            num = data_team["team_number"]
            new_data = {
                "team": num,
                "name": data_team["nickname"],
                "state": clean_state(data_team["state_prov"]),
                "district": clean_district(get_district(num)),
                "country": data_team["country"],
            }
            out.append(new_data)
    return out


def get_events(
    year: int, etag: Optional[str] = None, cache: bool = True
) -> Tuple[List[Dict[str, Any]], Optional[str]]:
    out: List[Dict[str, Any]] = []
    data, new_etag = get_tba("events/" + str(year), etag=etag, cache=cache)
    if type(data) is bool:
        return out, new_etag
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
        event_type = event["event_type"]
        if event_type == 5:
            event_type = 2
        if event_type == 6:
            event_type = 4

        # assigns worlds to week 8
        if event_type >= 3:
            event["week"] = 8

        # filter out incomplete events
        if "week" not in event or event["week"] is None:
            continue

        # bug in TBA API
        if event_type < 3 and year != 2016:
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
                "type": event_type,
                "week": event["week"],
            }
        )

    return out, new_etag


def get_event_rankings(
    event: str, etag: Optional[str] = None, cache: bool = True
) -> Tuple[Dict[int, int], Optional[str]]:
    out: Dict[int, int] = {}
    new_etag: Optional[str] = None
    # queries TBA for rankings, some older events are not populated
    try:
        query_str = "event/" + str(event) + "/rankings"
        data, new_etag = get_tba(query_str, etag=etag, cache=cache)
        if type(data) is bool:
            return out, new_etag
        rankings = data["rankings"]
        for ranking in rankings:
            team_num = int(ranking["team_key"][3:])
            out[team_num] = ranking["rank"]
    except Exception:
        pass

    return out, new_etag


def get_matches(
    year: int,
    event: str,
    event_time: int,
    etag: Optional[str] = None,
    cache: bool = True,
) -> Tuple[List[Dict[str, Any]], Optional[str]]:
    m_type = List[Dict[str, Any]]
    out: m_type = []
    query_str = "event/" + str(event) + "/matches"
    matches, new_etag = get_tba(query_str, etag=etag, cache=cache)
    if type(matches) is bool:
        return out, new_etag
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
    return out, new_etag
