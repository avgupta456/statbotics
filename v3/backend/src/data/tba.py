from collections import defaultdict
from datetime import datetime, timedelta
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, TypeVar

from src.constants import CURR_WEEK, CURR_YEAR
from src.data.utils import objs_type
from src.db.functions import (
    remove_teams_with_no_events,
    update_team_districts,
    update_team_offseason,
)
from src.db.models import (
    ETag,
    Event,
    Team,
    create_event_obj,
    create_team_event_obj,
    create_team_obj,
    create_team_year_obj,
    create_year_obj,
    match_dict_to_objs,
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


def load_teams(cache: bool = True) -> List[Team]:
    teams = get_teams_tba(cache=cache)
    team_objs = [
        create_team_obj(
            team=team["team"],
            name=team["name"],
            country=team["country"],
            state=team["state"],
            rookie_year=team["rookie_year"],
        )
        for team in teams
    ]
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
    return (create_year_obj(year=year), {}, {}, {}, {}, {}, {}, {})


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
    partial: bool,
    cache: bool = True,
) -> objs_type:
    # TODO: Handle 2021 offseason events (low priority)
    if year_num in YEAR_BLACKLIST:
        return objs

    (
        year_obj,
        team_year_objs_dict,
        event_objs_dict,
        team_event_objs_dict,
        match_objs_dict,
        alliance_objs_dict,
        team_match_objs_dict,
        etags_dict,
    ) = objs

    default_etag = ETag(year_num, "NA", "NA")
    new_etags_dict: Dict[str, ETag] = {}

    T = TypeVar("T")

    def call_tba(
        func: Callable[..., Tuple[T, Optional[str]]], path: str
    ) -> Tuple[T, bool]:
        prev_etag = etags_dict.get(path, default_etag).etag
        if partial:
            out, new_etag = func(prev_etag, False)
            if new_etag is not None:
                new_etag_obj = ETag(year_num, path, new_etag)
                new_etags_dict[new_etag_obj.pk()] = new_etag_obj
        else:
            out, new_etag = func(None, cache)
        return out, new_etag is not None and new_etag != prev_etag

    teams_dict: Dict[str, Team] = {team.team: team for team in teams}
    # TODO: can this handle offseason teams? Should we set the offseason flag?
    default_team = create_team_obj(
        team="", name="", country=None, state=None, rookie_year=None
    )

    team_is_competing_dict: Dict[str, bool] = defaultdict(lambda: False)
    team_next_event_dict: Dict[str, Any] = defaultdict(lambda: (None, None, None))
    team_first_event_dict: Dict[str, Any] = defaultdict(lambda: (None, None))

    # maps team to district_abbrev (or None if not in a district)
    district_teams: Dict[str, Optional[str]] = {}

    # maps team to offseason status
    offseason_teams: Dict[str, bool] = {}

    if not partial:
        districts, _ = call_tba(
            lambda etag, cache: get_districts_tba(year_num, etag=etag, cache=cache),
            str(year_num) + "/districts",
        )

        for district_key, district_abbrev in districts:
            curr_district_teams, _ = get_district_teams_tba(district_key, cache=cache)
            for team in curr_district_teams:
                district_teams[team] = DISTRICT_MAPPING.get(
                    district_abbrev, district_abbrev
                )

    events, _ = call_tba(
        lambda etag, cache: get_events_tba(year_num, etag=etag, cache=cache),
        str(year_num) + "/events",
    )

    for event in events:
        key = event["key"]
        curr_obj = event_objs_dict.get(key, None)
        curr_status = curr_obj.status if curr_obj is not None else None
        event_objs_dict[key] = create_event_obj(
            key=key,
            year=year_num,
            name=event["name"],
            time=event["time"],
            country=event["country"],
            district=event["district"],
            state=event["state"],
            start_date=event["start_date"],
            end_date=event["end_date"],
            type=event["type"],
            week=event["week"],
            video=event["video"],
            status=curr_status or "Upcoming",
        )

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

        matches, new_etag = call_tba(
            lambda etag, cache: get_matches_tba(
                year_num, event_key, event_time, etag, cache
            ),
            event_key + "/matches",
        )

        if partial and not new_etag:
            continue

        current_match = 0 if len(matches) > 0 else -1
        qual_matches = 0 if len(matches) > 0 else -1

        # "Completed", "Upcoming", "Ongoing", or "Invalid"
        event_status = get_event_status(matches, year_num)
        event_obj.status = event_status

        event_teams: Set[str] = set()
        rankings: Dict[str, int] = defaultdict(int)

        def add_team_event(team: str, offseason: bool):
            event_teams.add(team)
            if team not in district_teams:
                district_teams[team] = None

            if not offseason or team not in offseason_teams:
                offseason_teams[team] = offseason

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
            temp_event_teams, _ = call_tba(
                lambda etag, cache: get_event_teams_tba(event_key, etag, cache),
                event_key + "/teams",
            )

            for team in temp_event_teams:
                add_team_event(team, event_obj.offseason)

        elif event_status in ["Ongoing", "Completed"]:
            # Update event_obj, accumulate match_obj, alliance_objs, team_match_objs
            for match in matches:
                match["year"] = year_num
                match["week"] = event_obj.week
                match["offseason"] = event_obj.offseason

                (
                    match_obj,
                    curr_alliance_objs,
                    curr_team_match_objs,
                ) = match_dict_to_objs(match)

                current_match += match_obj.status == "Completed"
                qual_matches += not match_obj.playoff

                # Replace even if present, since may be Upcoming -> Completed
                match_objs_dict[match_obj.key] = match_obj
                for alliance_obj in curr_alliance_objs:
                    alliance_objs_dict[alliance_obj.pk()] = alliance_obj

                for team_match_obj in curr_team_match_objs:
                    add_team_event(team_match_obj.team, event_obj.offseason)
                    team_match_objs_dict[team_match_obj.pk()] = team_match_obj

            rankings, _ = call_tba(
                lambda etag, cache: get_event_rankings_tba(event_key, etag, cache),
                event_key + "/rankings",
            )

        # For Upcoming, Ongoing, and Completed events
        for team in event_teams:
            team_obj = teams_dict.get(team, default_team)
            team_event_obj = create_team_event_obj(
                team=team,
                year=year_num,
                event=event_key,
                time=event_time,
                offseason=event_obj.offseason,
                team_name=team_obj.name,
                event_name=event_obj.name,
                country=event_obj.country,
                district=event_obj.district,
                state=event_obj.state,
                type=event_obj.type,
                week=event_obj.week,
                status=event_status,
                first_event=False,
                num_teams=len(rankings),
            )
            if team in rankings:
                team_event_obj.rank = rankings[team]
            team_event_objs_dict[team_event_obj.pk()] = team_event_obj

        event_obj.current_match = current_match
        event_obj.qual_matches = qual_matches
        event_objs_dict[event_key] = event_obj

    # update is_first_event after iterating through all events
    for pk, team_event in team_event_objs_dict.items():
        team_event_objs_dict[pk].first_event = (
            team_first_event_dict[team_event.team][0] == team_event.event
        )

    for team in offseason_teams:
        team_obj = teams_dict.get(team, default_team)
        is_competing = team_is_competing_dict[team]
        next_event = team_next_event_dict[team]
        team_year_obj = create_team_year_obj(
            year=year_num,
            team=team,
            offseason=offseason_teams[team],
            name=team_obj.name,
            state=team_obj.state,
            country=team_obj.country,
            district=district_teams[team],
            is_competing=is_competing,
            next_event_key=next_event[0],
            next_event_name=next_event[1],
            next_event_week=next_event[2],
        )
        team_year_objs_dict[team_year_obj.pk()] = team_year_obj

    return (
        year_obj,
        team_year_objs_dict,
        event_objs_dict,
        team_event_objs_dict,
        match_objs_dict,
        alliance_objs_dict,
        team_match_objs_dict,
        new_etags_dict,
    )


def post_process():
    remove_teams_with_no_events()
    update_team_districts()
    update_team_offseason()
