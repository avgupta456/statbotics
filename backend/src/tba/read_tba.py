import time
from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Optional, Tuple, cast

from src.tba.breakdown import clean_breakdown, post_clean_breakdown
from src.tba.clean_data import clean_district, clean_state, get_match_time
from src.tba.constants import (
    DISTRICT_OVERRIDES,
    EVENT_BLACKLIST,
    MATCH_BLACKLIST,
    PLACEHOLDER_TEAMS,
)
from src.tba.main import get_tba
from src.tba.types import EventDict, MatchDict, TeamDict
from src.types.enums import CompLevel, EventType, MatchStatus, MatchWinner
from src.utils.utils import get_team_event_key


def get_timestamp_from_str(date: str):
    return int(time.mktime(datetime.strptime(date, "%Y-%m-%d").timetuple()))


def get_teams(cache: bool = True) -> List[TeamDict]:
    out: List[TeamDict] = []
    for i in range(50):
        data, _ = get_tba("teams/" + str(i), etag=None, cache=cache)
        if type(data) is bool:
            continue
        for data_team in data:
            num = data_team["key"][3:]
            new_data: TeamDict = {
                "team": num,
                "name": data_team["nickname"],
                "rookie_year": data_team["rookie_year"],
                "country": data_team["country"],
                "state": clean_state(data_team["state_prov"]),
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
) -> Tuple[List[int], Optional[str]]:
    out: List[int] = []
    data, new_etag = get_tba(
        "district/" + str(district) + "/teams", etag=etag, cache=cache
    )
    if type(data) is bool:
        return out, new_etag
    for team in data:
        out.append(int(team["key"][3:]))
    return out, new_etag


def get_district_rankings(
    district: str, etag: Optional[str] = None, cache: bool = True
) -> Tuple[Tuple[Dict[int, int], Dict[int, int], Dict[str, int]], Optional[str]]:
    team_to_points: Dict[int, int] = {}
    team_to_rank: Dict[int, int] = {}
    team_event_to_points: Dict[str, int] = {}
    data, new_etag = get_tba(
        "district/" + str(district) + "/rankings", etag=etag, cache=cache
    )
    if type(data) is bool or data is None:
        return (team_to_points, team_to_rank, team_event_to_points), new_etag
    for team in data:
        team_num = int(team["team_key"][3:])
        points = int(team["point_total"])
        rank = int(team["rank"])
        team_to_points[team_num] = points
        team_to_rank[team_num] = rank
        for event in team["event_points"]:
            event_key = event["event_key"]
            team_event_key = get_team_event_key(team_num, event_key)
            event_points = int(event["total"])
            team_event_to_points[team_event_key] = event_points

    return (team_to_points, team_to_rank, team_event_to_points), new_etag


def get_event_teams(
    event: str, etag: Optional[str] = None, cache: bool = True
) -> Tuple[List[int], Optional[str]]:
    query_str = "event/" + str(event) + "/teams/simple"
    data, new_etag = get_tba(query_str, etag=etag, cache=cache)
    if type(data) is bool:
        return [], new_etag
    out = [int(x["key"][3:]) for x in data]
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

        if "tempclone" in key:
            continue

        # filters out partial/missing events
        if key in EVENT_BLACKLIST:
            continue

        event_type_int = int(event["event_type"])
        if event_type_int == 99:
            # only keep some offseason events after 2025
            if year < 2025:
                continue
            try:
                event_teams = get_event_teams(key, etag=None, cache=cache)[0]
                # remove events with less than 6 teams
                if len(event_teams) < 6:
                    continue
                if len(set(PLACEHOLDER_TEAMS).intersection(set(event_teams))) > 0:
                    continue
                matches = get_tba(f"event/{key}/matches", etag=None, cache=cache)[0]
                for match in matches:  # type: ignore
                    all_teams = match["alliances"]["red"]["team_keys"]
                    all_teams += match["alliances"]["blue"]["team_keys"]
                    all_teams = [int(x[3:]) for x in all_teams]  # asserts no B teams
            except Exception:
                # remove events with B teams
                continue
        if event_type_int == 100:
            continue  # preseason

        event_type_dict: Dict[int, EventType] = defaultdict(lambda: EventType.INVALID)
        event_type_dict[0] = EventType.REGIONAL
        event_type_dict[1] = EventType.DISTRICT
        event_type_dict[2] = EventType.DISTRICT_CMP
        event_type_dict[3] = EventType.CHAMPS_DIV
        event_type_dict[4] = EventType.EINSTEIN
        # rename district divisions to district championship
        event_type_dict[5] = EventType.DISTRICT_CMP
        # rename festival of championships to einsteins
        event_type_dict[6] = EventType.EINSTEIN

        # TODO: map to OFFSEASON (might require reloading DB)
        event_type_dict[99] = EventType.REGIONAL
        # event_type_dict[99] = EventType.OFFSEASON

        event_type = event_type_dict[event_type_int]

        if event["district"] is not None:
            event["district"] = event["district"]["abbreviation"]

        if event["key"] in DISTRICT_OVERRIDES:
            event["district"] = DISTRICT_OVERRIDES[event["key"]]

        # assigns worlds to week 8
        if event_type.is_champs():
            event["week"] = 8

        # TODO: go through event_type once offseason mapped correctly
        if event_type_int == 99:
            event["week"] = 8  # gets incremented by 1 later

        # filter out incomplete events
        if "week" not in event or event["week"] is None:
            continue

        # bug in TBA API
        if year != 2016 and event_type in [
            EventType.REGIONAL,
            EventType.DISTRICT,
            EventType.DISTRICT_CMP,
        ]:
            # NOTE: affects offseason too (since REGIONAL -> OFFSEASON)
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
            "country": cast(str, event["country"]),
            "state": clean_state(event["state_prov"]),
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


def get_event_matches(
    year: int,
    event: str,
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

        red_score = match.get("alliances", {}).get("red", {}).get("score", None)
        blue_score = match.get("alliances", {}).get("blue", {}).get("score", None)
        status = MatchStatus.UPCOMING
        if red_score >= 0 and blue_score >= 0:
            status = MatchStatus.COMPLETED

        winner = None
        if status == MatchStatus.COMPLETED:
            raw_winner: Optional[str] = match.get("winning_alliance", None)
            if raw_winner == "red":
                winner = MatchWinner.RED
            elif raw_winner == "blue":
                winner = MatchWinner.BLUE
            else:
                winner = MatchWinner.TIE

            if year == 2015 and match["comp_level"] != "f":
                winner = None

        red_teams = [team[3:] for team in red_teams]
        blue_teams = [team[3:] for team in blue_teams]

        breakdown = match.get("score_breakdown", {}) or {}
        red_breakdown = clean_breakdown(
            match["key"], "red", year, breakdown.get("red", None), red_score
        )
        blue_breakdown = clean_breakdown(
            match["key"], "blue", year, breakdown.get("blue", None), blue_score
        )

        red_breakdown, blue_breakdown = post_clean_breakdown(
            match["key"], year, red_breakdown, blue_breakdown
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
            "red_1": int(red_teams[0]),
            "red_2": int(red_teams[1]),
            "red_3": int(red_teams[2]) if len(red_teams) > 2 else None,
            "red_dq": ",".join([t[3:] for t in red_dq_teams]),
            "red_surrogate": ",".join([t[3:] for t in red_surrogate_teams]),
            "blue_1": int(blue_teams[0]),
            "blue_2": int(blue_teams[1]),
            "blue_3": int(blue_teams[2]) if len(blue_teams) > 2 else None,
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


def get_event_alliances(
    event: str, etag: Optional[str] = None, cache: bool = True
) -> Tuple[Tuple[Dict[int, str], Dict[int, bool]], Optional[str]]:
    alliance_dict: Dict[int, str] = {}
    captain_dict: Dict[int, bool] = {}
    new_etag: Optional[str] = None
    # queries TBA for alliances, some older events are not populated
    try:
        query_str = "event/" + str(event) + "/alliances"
        data, new_etag = get_tba(query_str, etag=etag, cache=cache)
        if type(data) is bool:
            return (alliance_dict, captain_dict), new_etag
        for alliance in data:
            captain = alliance["picks"][0]
            for team in alliance["picks"]:
                team_num = team[3:]
                alliance_dict[team_num] = alliance["name"]
                captain_dict[team_num] = team == captain
    except Exception:
        pass

    return (alliance_dict, captain_dict), new_etag
