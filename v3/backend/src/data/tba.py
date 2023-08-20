from collections import defaultdict
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Set, Tuple

from src.constants import CURR_WEEK, CURR_YEAR, MAX_TEAM
from src.data.utils import objs_type
from src.db.functions import remove_teams_with_no_events, update_team_districts
from src.db.models import (
    Alliance,
    ETag,
    Event,
    Match,
    Team,
    TeamEvent,
    TeamMatch,
    TeamYear,
)
from src.db.models.create import (
    create_event_obj,
    create_match_obj,
    create_team_event_obj,
    create_team_obj,
    create_team_year_obj,
    create_year_obj,
)
from src.tba.constants import DISTRICT_MAPPING, YEAR_BLACKLIST
from src.tba.read_tba import (
    get_district_teams as get_district_teams_tba,
    get_districts as get_districts_tba,
    get_event_rankings as get_event_rankings_tba,
    get_event_teams as get_event_teams_tba,
    get_events as get_events_tba,
    get_matches as get_matches_tba,
    get_teams as get_teams_tba,
)

"""
HELPER FUNCTIONS
"""

# TODO: change objs_type from List of Lists to List of Dicts, add primary_key func to each object


def load_teams(cache: bool = True) -> List[Team]:
    teams = get_teams_tba(cache=cache)
    team_objs = [create_team_obj(team) for team in teams]
    return team_objs


def get_event_status(matches: List[Dict[str, Any]], year: int) -> str:
    num_matches = len(matches)
    num_qual_matches = len([m for m in matches if m["comp_level"] == "qm"])
    finals_matches = [m for m in matches if m["comp_level"] == "f"]

    red_final_match_wins = len([m for m in finals_matches if m["winner"] == "red"])
    blue_final_match_wins = len([m for m in finals_matches if m["winner"] == "blue"])
    max_finals_winner = max(red_final_match_wins, blue_final_match_wins)

    num_upcoming_matches = 0
    for match in matches:
        if match["status"] == "Upcoming":
            num_upcoming_matches += 1

    elims_started = num_matches > num_qual_matches
    finals_finished = num_upcoming_matches == 0 and max_finals_winner >= 2

    event_status = "Completed"
    if year == CURR_YEAR:
        if num_matches == 0:
            event_status = "Upcoming"
        elif not elims_started or not finals_finished:
            event_status = "Ongoing"
        else:
            event_status = "Completed"
    elif num_matches == 0:
        return "Invalid"

    return event_status


def create_objs(year: int) -> objs_type:
    year_obj = create_year_obj({"year": year})
    team_year_objs: List[TeamYear] = []
    event_objs: List[Event] = []
    team_event_objs: List[TeamEvent] = []
    match_objs: List[Match] = []
    alliance_objs: List[Alliance] = []
    team_match_objs: List[TeamMatch] = []

    return (
        year_obj,
        team_year_objs,
        event_objs,
        team_event_objs,
        match_objs,
        alliance_objs,
        team_match_objs,
    )


"""
MAIN FUNCTIONS
"""


def check_year_partial(
    year_num: int, event_objs: List[Event], etags: List[ETag]
) -> bool:
    etags_dict = {etag.path: etag for etag in etags}
    default_etag = ETag(year_num, "NA", "NA")

    prev_etag = etags_dict.get(str(year_num) + "/events", default_etag).etag
    _, new_etag = get_events_tba(year_num, etag=prev_etag, cache=False)
    if new_etag != prev_etag:
        return True  # If any new events

    for event_obj in event_objs:
        if event_obj.status == "Completed":
            continue

        start_date = datetime.strptime(event_obj.start_date, "%Y-%m-%d")
        end_date = datetime.strptime(event_obj.end_date, "%Y-%m-%d")
        if start_date - timedelta(days=1) > datetime.now():
            continue

        if end_date + timedelta(days=1) < datetime.now():
            continue

        prev_etag = etags_dict.get(event_obj.key + "/matches", default_etag).etag
        _, new_etag = get_matches_tba(
            year_num, event_obj.key, event_obj.time, prev_etag, cache=False
        )
        if new_etag == prev_etag and new_etag is not None:
            continue

        prev_etag = etags_dict.get(event_obj.key + "/rankings", default_etag).etag
        _, new_etag = get_event_rankings_tba(event_obj.key, prev_etag, cache=False)
        if new_etag == prev_etag and new_etag is not None:
            continue

        return True  # If any event has new matches, return True
    return False  # Otherwise return False


def process_year(
    year_num: int,
    teams: List[Team],
    objs: objs_type,
    etags: List[ETag],
    partial: bool,
    cache: bool = True,
) -> Tuple[objs_type, List[ETag]]:
    # TODO: Handle 2021 offseason events (low priority)
    if year_num in YEAR_BLACKLIST:
        return (objs, [])

    (
        year_obj,
        team_year_objs,
        event_objs,
        team_event_objs,
        match_objs,
        alliance_objs,
        team_match_objs,
    ) = objs

    event_objs_dict = {x.key: x for x in event_objs}
    team_event_objs_dict = {(x.team, x.event): x for x in team_event_objs}
    match_objs_dict = {x.key: x for x in match_objs}
    alliance_objs_dict = {(x.match, x.alliance): x for x in alliance_objs}
    team_match_objs_dict = {(x.team, x.match): x for x in team_match_objs}

    etags_dict = {etag.path: etag for etag in etags}
    default_etag = ETag(year_num, "NA", "NA")
    new_etags: List[ETag] = []

    teams_dict: Dict[str, Team] = {team.team: team for team in teams}
    # TODO: can this handle offseason teams? Should we set the offseason flag?
    default_team = create_team_obj(
        {"name": None, "team": None, "state": None, "country": None, "district": None}
    )

    team_is_competing_dict: Dict[str, bool] = defaultdict(lambda: False)
    team_next_event_dict: Dict[str, Any] = defaultdict(lambda: (None, None, None))
    team_first_event_dict: Dict[str, Any] = defaultdict(lambda: (None, None))

    # maps team to district_abbrev (or None if not in a district)
    district_teams: Dict[str, Optional[str]] = {}

    if not partial:
        districts, _ = get_districts_tba(year_num, cache=cache)
        for district_key, district_abbrev in districts:
            curr_district_teams, _ = get_district_teams_tba(district_key, cache=cache)
            for team in curr_district_teams:
                district_teams[team] = DISTRICT_MAPPING.get(
                    district_abbrev, district_abbrev
                )

    if partial:
        etag_key = str(year_num) + "/events"
        prev_etag = etags_dict.get(etag_key, default_etag).etag
        events, new_etag = get_events_tba(year_num, etag=prev_etag, cache=False)
        if new_etag is not None and new_etag != prev_etag:
            new_etags.append(ETag(year_num, etag_key, new_etag))
    else:
        events, _ = get_events_tba(year_num, etag=None, cache=cache)

    for event in events:
        event_objs_dict[event["key"]] = create_event_obj(event)

    for event_obj in event_objs_dict.values():
        if partial:
            if event_obj.status == "Completed":
                continue

            start_date = datetime.strptime(event_obj.start_date, "%Y-%m-%d")
            end_date = datetime.strptime(event_obj.end_date, "%Y-%m-%d")
            if start_date - timedelta(days=1) > datetime.now():
                continue

            if end_date + timedelta(days=1) < datetime.now():
                continue

        event_key, event_time = event_obj.key, event_obj.time

        if partial:
            etag_key = event_key + "/matches"
            prev_etag = etags_dict.get(etag_key, default_etag).etag
            matches, new_etag = get_matches_tba(
                year_num, event_key, event_time, etag=prev_etag, cache=False
            )
            if new_etag is not None:
                if new_etag == prev_etag:
                    continue
                else:
                    new_etags.append(ETag(year_num, etag_key, new_etag))
        else:
            matches, _ = get_matches_tba(
                year_num, event_key, event_time, etag=None, cache=cache
            )

        current_match = 0 if len(matches) > 0 else -1
        qual_matches = 0 if len(matches) > 0 else -1

        # "Completed", "Upcoming", "Ongoing", or "Invalid"
        event_status = get_event_status(matches, year_num)
        event_obj.status = event_status

        event_teams: Set[str] = set()
        rankings: Dict[str, int] = defaultdict(int)

        def add_team_event(team: str):
            event_teams.add(team)
            if team not in district_teams:
                district_teams[team] = None

            event_name = event_obj.name
            event_week = event_obj.week
            event_year = event_obj.year

            # Stores whether a team is competing this week
            if event_year == CURR_YEAR and event_week == CURR_WEEK:
                team_is_competing_dict[team] = True

            # Store closest upcoming/ongoing event
            if (
                event_week >= CURR_WEEK
                and event_status != "Completed"
                and (
                    team not in team_next_event_dict
                    or team_next_event_dict[team][2] > event_week
                )
            ):
                team_next_event_dict[team] = (event_key, event_name, event_week)

            # Store first event
            if (
                team not in team_first_event_dict
                or team_first_event_dict[team][1] > event_week
            ):
                team_first_event_dict[team] = (event_key, event_week)

        if event_status == "Invalid":
            continue

        elif event_status == "Upcoming":
            if partial:
                etag_key = event_key + "/teams"
                prev_etag = etags_dict.get(etag_key, default_etag).etag
                temp_event_teams, new_etag = get_event_teams_tba(
                    event_key, etag=prev_etag, cache=False
                )
                if new_etag is not None and new_etag != prev_etag:
                    new_etags.append(ETag(year_num, etag_key, new_etag))
            else:
                temp_event_teams, _ = get_event_teams_tba(
                    event_key, etag=None, cache=cache
                )

            for team in temp_event_teams:
                add_team_event(team)

        elif event_status in ["Ongoing", "Completed"]:
            # Update event_obj, accumulate match_obj, alliance_objs, team_match_objs
            for match in matches:
                match["year"] = year_num
                match["week"] = event_obj.week
                match["offseason"] = event_obj.offseason
                match_obj, curr_alliance_objs, curr_team_match_objs = create_match_obj(
                    match
                )
                current_match += match_obj.status == "Completed"
                qual_matches += not match_obj.playoff
                # Replace even if present, since may be Upcoming -> Completed
                match_objs_dict[match_obj.key] = match_obj
                for alliance_obj in curr_alliance_objs:
                    alliance_objs_dict[
                        (alliance_obj.match, alliance_obj.alliance)
                    ] = alliance_obj
                for team_match_obj in curr_team_match_objs:
                    add_team_event(team_match_obj.team)
                    team_match_objs_dict[
                        (team_match_obj.team, team_match_obj.match)
                    ] = team_match_obj

            if partial:
                etag_key = event_key + "/rankings"
                prev_etag = etags_dict.get(etag_key, default_etag).etag
                rankings, new_etag = get_event_rankings_tba(
                    event_key, etag=prev_etag, cache=False
                )
                if new_etag is not None and new_etag != prev_etag:
                    new_etags.append(ETag(year_num, etag_key, new_etag))
            else:
                rankings, _ = get_event_rankings_tba(event_key, etag=None, cache=cache)

        # For Upcoming, Ongoing, and Completed events
        for team in event_teams:
            team_obj = teams_dict.get(team, default_team)
            team_event_objs_dict[(team, event_key)] = create_team_event_obj(
                {
                    "team": team,
                    "year": year_num,
                    "event": event_key,
                    "time": event_time,
                    "team_name": team_obj.name,
                    "event_name": event_obj.name,
                    "offseason": event_obj.offseason,
                    "state": event_obj.state,
                    "country": event_obj.country,
                    "district": event_obj.district,
                    "type": event_obj.type,
                    "week": event_obj.week,
                    "status": event_status,
                    "rank": rankings.get(team, -1),
                    "num_teams": len(rankings),
                }
            )

        event_obj.current_match = current_match
        event_obj.qual_matches = qual_matches
        event_objs_dict[event_key] = event_obj

    event_objs = list(event_objs_dict.values())
    team_event_objs = list(team_event_objs_dict.values())
    match_objs = list(match_objs_dict.values())
    alliance_objs = list(alliance_objs_dict.values())
    team_match_objs = list(team_match_objs_dict.values())

    # update is_first_event after iterating through all events
    for team_event in team_event_objs:
        team_event.first_event = (
            team_first_event_dict[team_event.team][0] == team_event.event
        )

    team_year_objs_dict = {(x.team, x.year): x for x in team_year_objs}
    for team in district_teams:
        team_obj = teams_dict.get(team, default_team)
        is_competing = team_is_competing_dict[team]
        next_event = team_next_event_dict[team]
        team_year_objs_dict[(team, year_num)] = create_team_year_obj(
            {
                "year": year_num,
                "team": team,
                "offseason": team > MAX_TEAM,
                "name": team_obj.name,
                "state": team_obj.state,
                "country": team_obj.country,
                "district": district_teams[team],
                "is_competing": is_competing,
                "next_event_key": next_event[0],
                "next_event_name": next_event[1],
                "next_event_week": next_event[2],
            }
        )

    team_year_objs = list(team_year_objs_dict.values())

    print(
        len(team_year_objs),
        len(event_objs),
        len(team_event_objs),
        len(match_objs),
        len(alliance_objs),
        len(team_match_objs),
    )

    return (
        (
            year_obj,
            team_year_objs,
            event_objs,
            team_event_objs,
            match_objs,
            alliance_objs,
            team_match_objs,
        ),
        new_etags,
    )


def post_process():
    remove_teams_with_no_events()
    update_team_districts()
