import os
import statistics
import time
from collections import defaultdict
from datetime import datetime
from typing import Any, Dict, List

from requests import Session

from src.breakdown import clean_breakdown
from src.classes import Match, YearStats
from src.utils import dump_cache, load_cache

# TBA API

AUTH_KEY = "XeUIxlvO4CPc44NlLE3ncevDg7bAhp6CRy6zC9M2aQb2zGfys0M30eKwavFJSEJr"
READ_PREFIX = "https://www.thebluealliance.com/api/v3/"

session = Session()
session.headers.update({"X-TBA-Auth-Key": AUTH_KEY, "X-TBA-Auth-Id": ""})


def get_tba(url: str) -> Any:
    if os.path.exists("cache/" + url + "/data.p"):
        return load_cache("cache/" + url)  # Cache Hit

    data = session.get(READ_PREFIX + url).json()
    dump_cache("cache/" + url, data)  # Cache Miss

    return data


# CONSTANTS

YEAR_BLACKLIST: List[int] = [2002, 2003, 2004, 2021]  # Skip 2002-2004 for simplicity
EVENT_BLACKLIST: List[str] = ["2004va", "2005is", "2005va", "2007ga", "2008cal", "2016cafc2", "2019lafwbb3", "2022zhha"]  # type: ignore
MATCH_BLACKLIST: List[str] = ["2005ct_sf2m3", "2005ct_f1m1", "2005ct_f1m2", "2005fl_sf2m3", "2005fl_f1m1", "2005fl_f1m2", "2005ga_f1m1", "2005gl_f1m1", "2005gl_f1m2", "2005wat_qf1m1", "2005wat_qf1m2", "2006pit_qf1m1", "2006pit_qf1m2", "2014cafc2_qm4", "2016mttd_qm13", "2016mttd_qm18", "2016mttd_qm30", "2016ohsc_qf1m1", "2016ohsc_qf1m2", "2016ohsc_qf3m1", "2016ohsc_qf3m2", "2017crc_qf3m1", "2019wiwi_ef2m1", "2019wiwi_ef5m1", "2019wiwi_qf3m1"]  # type: ignore


# HELPER FUNCTIONS


def get_timestamp_from_str(date: str):
    return int(time.mktime(datetime.strptime(date, "%Y-%m-%d").timetuple()))


def get_match_time(match: Dict[str, Any], event_time: int) -> int:
    comp_offset = {"qm": 0, "ef": 200, "qf": 300, "sf": 400, "f": 500}
    return event_time + comp_offset[match["comp_level"]] + 10 * match["set_number"] + match["match_number"]  # type: ignore


# GET DATA


def get_data(year: int) -> List[Any]:
    if year < 2002 or year > 2023 or year in YEAR_BLACKLIST:
        return []

    all_matches: List[Match] = []
    for event in get_tba(f"events/{year}"):
        event_key: str = event["key"]
        event_offseason = event["event_type"] > 10
        if event_key in EVENT_BLACKLIST or event_offseason:
            continue

        event_type: int = event["event_type"]
        # District divisions -> district champs
        if event_type == 5:
            event_type = 2

        # assigns worlds to week 8
        if event_type >= 3:
            event["week"] = 8

        # bug in TBA API
        if event_type < 3 and year != 2016:
            event["week"] += 1

        event_time = get_timestamp_from_str(event["start_date"])

        for match in get_tba(f"event/{event_key}/matches"):
            key = match["key"]
            if key in MATCH_BLACKLIST:
                continue

            # Skip handling DQs and surrogates for simplicity
            red_teams = [int(t[3:]) for t in match["alliances"]["red"]["team_keys"]]
            blue_teams = [int(t[3:]) for t in match["alliances"]["blue"]["team_keys"]]

            red_score = match["alliances"]["red"]["score"]
            blue_score = match["alliances"]["blue"]["score"]

            # Skip matches with missing data
            if red_score < 0 or blue_score < 0:
                continue

            # Skip playoff matches with DQ
            if match["comp_level"] != "qm" and min(red_score, blue_score) <= 0:
                continue

            red_breakdown = clean_breakdown(
                year,
                key,
                (match.get("score_breakdown", {}) or {}).get("red", {}),
                red_score,
            )
            blue_breakdown = clean_breakdown(
                year,
                key,
                (match.get("score_breakdown", {}) or {}).get("blue", {}),
                blue_score,
            )

            red_no_fouls = red_breakdown["no_foul_points"]
            blue_no_fouls = blue_breakdown["no_foul_points"]

            red_rp_1 = red_breakdown["rp_1"]
            blue_rp_1 = blue_breakdown["rp_1"]

            red_rp_2 = red_breakdown["rp_2"]
            blue_rp_2 = blue_breakdown["rp_2"]

            all_matches.append(
                Match(
                    key,
                    event_key,
                    event["week"],
                    year,
                    match["comp_level"] != "qm",
                    match["time"] or get_match_time(match, event_time),
                    red_teams[0],
                    red_teams[1],
                    red_teams[2],
                    blue_teams[0],
                    blue_teams[1],
                    blue_teams[2],
                    red_score,
                    blue_score,
                    red_no_fouls,
                    blue_no_fouls,
                    red_rp_1,
                    blue_rp_1,
                    red_rp_2,
                    blue_rp_2,
                    red_breakdown,
                    blue_breakdown,
                )
            )

    scores: List[int] = []
    rp_1s: List[int] = []
    rp_2s: List[int] = []
    breakdown: Dict[str, List[int]] = defaultdict(list)
    for match in all_matches:
        if match.week == 1 and not match.playoff:
            scores.extend([match.red_score, match.blue_score])
            rp_1s.extend([match.red_rp_1, match.blue_rp_1])
            rp_2s.extend([match.red_rp_2, match.blue_rp_2])
            for k in match.red_breakdown:
                breakdown[k].extend([match.red_breakdown[k], match.blue_breakdown[k]])

    score_mean = statistics.mean(scores)
    score_sd = statistics.pstdev(scores)

    rp_1_mean = statistics.mean(rp_1s)
    rp_1_sd = statistics.pstdev(rp_1s)

    rp_2_mean = statistics.mean(rp_2s)
    rp_2_sd = statistics.pstdev(rp_2s)

    breakdown_mean = {}
    breakdown_sd = {}
    for k in breakdown:
        breakdown_mean[k] = statistics.mean(breakdown[k])
        breakdown_sd[k] = statistics.pstdev(breakdown[k])

    stats = YearStats(
        year,
        score_mean,
        score_sd,
        rp_1_mean,
        rp_1_sd,
        rp_2_mean,
        rp_2_sd,
        breakdown_mean,
        breakdown_sd,
    )

    dump_cache(
        f"cache/processed/{year}",
        (all_matches, stats),
    )

    return all_matches
