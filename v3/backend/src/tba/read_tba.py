import time
from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Optional, Tuple, cast

from src.types.enums import EventType, MatchStatus, MatchWinner, CompLevel
from src.tba.breakdown import clean_breakdown
from src.tba.clean_data import clean_district, clean_state, get_match_time
from src.tba.constants import DISTRICT_OVERRIDES, EVENT_BLACKLIST, MATCH_BLACKLIST
from src.tba.main import get_tba
from src.tba.types import EventDict, MatchDict, TeamDict


def get_timestamp_from_str(date: str):
    return int(time.mktime(datetime.strptime(date, "%Y-%m-%d").timetuple()))


def get_teams(cache: bool = True) -> List[TeamDict]:
    out: List[TeamDict] = []
    for i in range(20):
        data, _ = get_tba("teams/" + str(i), etag=None, cache=cache)
        if type(data) is bool:
            continue
        for data_team in data:
            num = data_team["key"][3:]
            new_data: TeamDict = {
                "team": num,
                "name": data_team["nickname"],
                "rookie_year": data_team["rookie_year"],
                "offseason": True,
                "state": clean_state(data_team["state_prov"]),
                "country": data_team["country"],
            }
            out.append(new_data)
    return out


def get_districts(
    year: int, etag: Optional[str] = None, cache: bool = True
) -> Tuple[List[Tuple[str, str]], Optional[str]]:
    out: List[Tuple[str, str]] = []
    data, new_etag = get_tba("districts/" + str(year), etag=etag, cache=cache)
    if type(data) is bool:
        return out, new_etag
    for district in data:
        out.append((district["key"], district["abbreviation"]))
    return out, new_etag


def get_district_teams(
    district: str, etag: Optional[str] = None, cache: bool = True
) -> Tuple[List[str], Optional[str]]:
    out: List[str] = []
    data, new_etag = get_tba(
        "district/" + str(district) + "/rankings", etag=etag, cache=cache
    )
    if type(data) is bool:
        return out, new_etag
    for team in data:
        team_num = team["team_key"][3:]
        # points = int(team["point_total"])
        out.append(team_num)

    return out, new_etag


def get_events(
    year: int, etag: Optional[str] = None, cache: bool = True
) -> Tuple[List[EventDict], Optional[str]]:
    out: List[EventDict] = []
    data, new_etag = get_tba("events/" + str(year), etag=etag, cache=cache)
    if type(data) is bool:
        return out, new_etag
    for event in data:
        key: str = event["key"]

        # filters out partial/missing events
        if key in EVENT_BLACKLIST:
            continue

        if event["district"] is not None:
            event["district"] = event["district"]["abbreviation"]

        if event["key"] in DISTRICT_OVERRIDES:
            event["district"] = DISTRICT_OVERRIDES[event["key"]]

        # renames district divisions to district championship
        # renames festival of championships to einsteins

        event_type_int = int(event["event_type"])
        event_type_dict: Dict[int, EventType] = defaultdict(lambda: EventType.INVALID)
        event_type_dict[0] = EventType.REGIONAL
        event_type_dict[1] = EventType.DISTRICT
        event_type_dict[2] = EventType.DISTRICT_CMP
        event_type_dict[3] = EventType.CHAMPS_DIV
        event_type_dict[4] = EventType.EINSTEIN
        event_type_dict[
            5
        ] = EventType.DISTRICT_CMP  # rename district divisions to district championship
        event_type_dict[
            6
        ] = EventType.EINSTEIN  # rename festival of championships to einsteins
        event_type_dict[99] = EventType.OFFSEASON
        event_type_dict[100] = EventType.PRESEASON
        event_type = event_type_dict[event_type_int]

        # assigns worlds to week 8
        if event_type.is_champs():
            event["week"] = 8

        # assigns preseason to week 0
        if event_type == EventType.PRESEASON:
            event["week"] = 0

        # assigns offseasons to week 9
        if event_type == EventType.OFFSEASON:
            event["week"] = 9

        # filter out incomplete events
        if "week" not in event or event["week"] is None:
            continue

        # bug in TBA API
        if year != 2016 and event_type in [
            EventType.REGIONAL,
            EventType.DISTRICT,
            EventType.DISTRICT_CMP,
        ]:
            event["week"] += 1

        video: Optional[str] = None
        webcasts = event["webcasts"]
        if len(webcasts) > 0:
            video_type = webcasts[0]["type"]
            if video_type == "twitch":
                video = "https://www.twitch.tv/" + webcasts[0]["channel"]
            elif video_type == "youtube":
                video = "https://www.youtube.com/watch?v=" + webcasts[0]["channel"]

            if video is not None and len(video) > 50:
                video = None

        new_data: EventDict = {
            "year": year,
            "key": key,
            "name": cast(str, event["name"]),
            "state": clean_state(event["state_prov"]),
            "country": cast(str, event["country"]),
            "district": clean_district(event["district"]),
            "start_date": cast(str, event["start_date"]),
            "end_date": cast(str, event["end_date"]),
            "time": get_timestamp_from_str(event["start_date"]),
            "type": event_type,
            "week": cast(int, event["week"]),
            "video": video,
        }

        out.append(new_data)

    return out, new_etag


def get_event_teams(
    event: str, etag: Optional[str] = None, cache: bool = True
) -> Tuple[List[str], Optional[str]]:
    query_str = "event/" + str(event) + "/teams/simple"
    data, new_etag = get_tba(query_str, etag=etag, cache=cache)
    if type(data) is bool:
        return [], new_etag
    out = [x["key"][3:] for x in data]
    return out, new_etag


def get_event_rankings(
    event: str, etag: Optional[str] = None, cache: bool = True
) -> Tuple[Dict[str, int], Optional[str]]:
    out: Dict[str, int] = {}
    new_etag: Optional[str] = None
    # queries TBA for rankings, some older events are not populated
    try:
        query_str = "event/" + str(event) + "/rankings"
        data, new_etag = get_tba(query_str, etag=etag, cache=cache)
        if type(data) is bool:
            return out, new_etag
        rankings = data["rankings"]
        for ranking in rankings:
            team_num = ranking["team_key"][3:]
            out[team_num] = ranking["rank"]
    except Exception:
        pass

    return out, new_etag


def get_event_matches(
    year: int,
    event: str,
    offseason: bool,
    event_time: int,
    etag: Optional[str] = None,
    cache: bool = True,
) -> Tuple[List[MatchDict], Optional[str]]:
    out: List[MatchDict] = []
    query_str = "event/" + str(event) + "/matches"
    matches, new_etag = get_tba(query_str, etag=etag, cache=cache)

    if type(matches) is bool:
        return out, new_etag

    for match in matches:
        red_teams: List[str] = match["alliances"]["red"]["team_keys"]
        red_dq_teams: List[str] = match["alliances"]["red"]["dq_team_keys"]
        red_surrogate_teams: List[str] = match["alliances"]["red"][
            "surrogate_team_keys"
        ]
        blue_teams: List[str] = match["alliances"]["blue"]["team_keys"]
        blue_dq_teams: List[str] = match["alliances"]["blue"]["dq_team_keys"]
        blue_surrogate_teams: List[str] = match["alliances"]["blue"][
            "surrogate_team_keys"
        ]

        if match["key"] in MATCH_BLACKLIST:
            continue

        if year <= 2004 and (len(set(red_teams)) < 2 or len(set(blue_teams)) < 2):
            continue

        if year > 2004 and (len(set(red_teams)) < 3 or len(set(blue_teams)) < 3):
            continue

        if len(set(red_teams).intersection(set(blue_teams))) > 0:
            continue

        raw_red_score: int = match["alliances"]["red"]["score"]
        raw_blue_score: int = match["alliances"]["blue"]["score"]

        status = (
            MatchStatus.COMPLETED
            if min(raw_red_score, raw_blue_score) >= 0
            else MatchStatus.UPCOMING
        )

        red_score = None
        blue_score = None
        winner = None
        if status == MatchStatus.COMPLETED:
            red_score = raw_red_score
            blue_score = raw_blue_score

            if match["winning_alliance"] == "red":
                winner = MatchWinner.RED
            elif match["winning_alliance"] == "blue":
                winner = MatchWinner.BLUE
            elif match["winning_alliance"] == "" and red_score == blue_score:
                winner = MatchWinner.TIE

            if year == 2015 and match["comp_level"] != "f":
                winner = None

        red_teams = [team[3:] for team in red_teams]
        blue_teams = [team[3:] for team in blue_teams]

        breakdown = match.get("score_breakdown", {}) or {}
        red_breakdown = clean_breakdown(
            match["key"], year, offseason, breakdown.get("red", None), red_score
        )
        blue_breakdown = clean_breakdown(
            match["key"], year, offseason, breakdown.get("blue", None), blue_score
        )

        video = None
        if "videos" in match:
            if len(match["videos"]) > 0:
                if match["videos"][0]["type"] == "youtube":
                    video = match["videos"][0]["key"].split("&")[0].split("?")[0]
                    if len(video) > 20:
                        video = None

        time: int = match["time"] or get_match_time(
            match["comp_level"],
            match["set_number"],
            match["match_number"],
            event_time,
        )

        comp_level = CompLevel.INVALID
        if match["comp_level"] == "qm":
            comp_level = CompLevel.QUAL
        elif match["comp_level"] == "ef":
            comp_level = CompLevel.EIGHTH
        elif match["comp_level"] == "qf":
            comp_level = CompLevel.QUARTER
        elif match["comp_level"] == "sf":
            comp_level = CompLevel.SEMI
        elif match["comp_level"] == "f":
            comp_level = CompLevel.FINAL

        match_data: MatchDict = {
            "event": event,
            "key": cast(str, match["key"]),
            "comp_level": comp_level,
            "set_number": cast(int, match["set_number"]),
            "match_number": cast(int, match["match_number"]),
            "status": status,
            "video": video,
            "red_1": red_teams[0],
            "red_2": red_teams[1],
            "red_3": red_teams[2] if len(red_teams) > 2 else None,
            "red_dq": ",".join([t[3:] for t in red_dq_teams]),
            "red_surrogate": ",".join([t[3:] for t in red_surrogate_teams]),
            "blue_1": blue_teams[0],
            "blue_2": blue_teams[1],
            "blue_3": blue_teams[2] if len(blue_teams) > 2 else None,
            "blue_dq": ",".join([t[3:] for t in blue_dq_teams]),
            "blue_surrogate": ",".join([t[3:] for t in blue_surrogate_teams]),
            "winner": winner,
            "time": time,
            "predicted_time": cast(Optional[int], match["predicted_time"]),
            "red_score": red_score,
            "blue_score": blue_score,
            "red_score_breakdown": red_breakdown,
            "blue_score_breakdown": blue_breakdown,
        }
        out.append(match_data)

    return out, new_etag
