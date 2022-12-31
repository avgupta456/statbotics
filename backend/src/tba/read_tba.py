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
        data, _ = get_tba("teams/" + str(i), etag=None, cache=cache)
        if type(data) is bool:
            continue
        for data_team in data:
            num = data_team["team_number"]
            new_data = {
                "team": num,
                "name": data_team["nickname"],
                "rookie_year": data_team["rookie_year"],
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

        # assigns preseason to week 0
        if event_type == 100:
            event["week"] = 0

        # assigns offseasons to week 9
        if event_type == 99:
            event["week"] = 9

        # filter out incomplete events
        if "week" not in event or event["week"] is None:
            continue

        # bug in TBA API
        if event_type < 3 and year != 2016:
            event["week"] += 1

        video = None
        webcasts = event["webcasts"]
        if len(webcasts) > 0:
            video_type = webcasts[0]["type"]
            if video_type == "twitch":
                video = "https://www.twitch.tv/" + webcasts[0]["channel"]
            elif video_type == "youtube":
                video = "https://www.youtube.com/watch?v=" + webcasts[0]["channel"]

        out.append(
            {
                "year": year,
                "key": key,
                "name": event["name"],
                "state": clean_state(event["state_prov"]),
                "country": event["country"],
                "district": clean_district(event["district"]),
                "start_date": event["start_date"],
                "end_date": event["end_date"],
                "time": get_timestamp_from_str(event["start_date"]),
                "type": event_type,
                "week": event["week"],
                "video": video,
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
        red_dq_teams = match["alliances"]["red"]["dq_team_keys"]
        red_surrogate_teams = match["alliances"]["red"]["surrogate_team_keys"]
        blue_teams = match["alliances"]["blue"]["team_keys"]
        blue_dq_teams = match["alliances"]["blue"]["dq_team_keys"]
        blue_surrogate_teams = match["alliances"]["blue"]["surrogate_team_keys"]

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

        def format_team(team: str) -> int:
            team = team[3:]
            if not team[-1].isdigit():
                team = team[:-1] + "000" + str(ord(team[-1]) - ord("A")).rjust(2, "0")
            return int(team)

        red_teams = [format_team(team) for team in red_teams]
        blue_teams = [format_team(team) for team in blue_teams]

        breakdown: Dict[str, Any] = match.get("score_breakdown", {}) or {}
        red_breakdown = get_breakdown(year, breakdown.get("red", None))
        blue_breakdown = get_breakdown(year, breakdown.get("blue", None))

        video = None
        if "videos" in match:
            if len(match["videos"]) > 0:
                if match["videos"][0]["type"] != "youtube":
                    continue
                video = match["videos"][0]["key"].split("&")[0].split("?")[0]
                if len(video) > 20:
                    video = None

        match_data: Dict[str, Any] = {
            "event": event,
            "key": match["key"],
            "comp_level": match["comp_level"],
            "set_number": match["set_number"],
            "match_number": match["match_number"],
            "status": "Completed" if min(red_score, blue_score) >= 0 else "Upcoming",
            "video": video,
            "red_1": red_teams[0] if len(red_teams) > 0 else None,
            "red_2": red_teams[1] if len(red_teams) > 1 else None,
            "red_3": red_teams[2] if len(red_teams) > 2 else None,
            "blue_1": blue_teams[0] if len(blue_teams) > 0 else None,
            "blue_2": blue_teams[1] if len(blue_teams) > 1 else None,
            "blue_3": blue_teams[2] if len(blue_teams) > 2 else None,
            "red_dq": ",".join([str(format_team(t)) for t in red_dq_teams]),
            "blue_dq": ",".join([str(format_team(t)) for t in blue_dq_teams]),
            "red_surrogate": ",".join(
                [str(format_team(t)) for t in red_surrogate_teams]
            ),
            "blue_surrogate": ",".join(
                [str(format_team(t)) for t in blue_surrogate_teams]
            ),
            "winner": winner,
            "time": get_match_time(match, event_time),
            "red_score": red_score,
            "blue_score": blue_score,
            "red_score_breakdown": red_breakdown,
            "blue_score_breakdown": blue_breakdown,
        }
        out.append(match_data)
    return out, new_etag
