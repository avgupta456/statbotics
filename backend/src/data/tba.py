from collections import defaultdict
from datetime import datetime, timedelta
from typing import Any, Dict, List, Set, Tuple

from src.constants import MAX_TEAM
from src.data.utils import objs_type
from src.db.functions.remove_teams_no_events import remove_teams_with_no_events
from src.db.models import ETag, Event, Match, Team, TeamEvent, TeamMatch, TeamYear
from src.db.models.create import (
    create_event_obj,
    create_match_obj,
    create_team_event_obj,
    create_team_obj,
    create_team_year_obj,
    create_year_obj,
)
from src.tba.constants import YEAR_BLACKLIST
from src.tba.read_tba import (
    get_event_rankings as get_event_rankings_tba,
    get_event_teams as get_event_teams_tba,
    get_events as get_events_tba,
    get_matches as get_matches_tba,
    get_teams as get_teams_tba,
)


def load_teams(cache: bool = True) -> List[Team]:
    teams = get_teams_tba(cache=cache)
    team_objs = [create_team_obj(team) for team in teams]
    return team_objs


def get_event_status(matches: List[Dict[str, Any]], curr_year: bool) -> str:
    num_matches = len(matches)
    num_qual_matches = len([m for m in matches if m["comp_level"] == "qm"])
    num_upcoming_matches = 0
    for match in matches:
        if match["status"] == "Upcoming":
            num_upcoming_matches += 1

    # TODO: Some 2022 offseason matches are marked Ongoing
    # Incorporate start/end date to move these to invalid
    # Not a problem until offseason matches displayed on frontend

    event_status = "Completed"
    if curr_year:
        if num_matches == 0:
            event_status = "Upcoming"
        elif num_upcoming_matches > 0 or num_matches == num_qual_matches:
            event_status = "Ongoing"
        else:
            event_status = "Completed"
    elif num_matches == 0:
        return "Invalid"

    return event_status


def process_year(
    year_num: int,
    end_year: int,
    teams: List[Team],
    etags: List[ETag],
    mock: bool = False,
    cache: bool = True,
) -> Tuple[objs_type, List[ETag]]:
    year_obj = create_year_obj({"year": year_num})
    team_year_objs: List[TeamYear] = []
    event_objs: List[Event] = []
    team_event_objs: List[TeamEvent] = []
    match_objs: List[Match] = []
    team_match_objs: List[TeamMatch] = []
    new_etags: List[ETag] = []

    # TODO: Handle 2021 offseason events (low priority)
    if year_num in YEAR_BLACKLIST:
        return (
            (
                year_obj,
                team_year_objs,
                event_objs,
                team_event_objs,
                match_objs,
                team_match_objs,
            ),
            new_etags,
        )

    etags_dict = {etag.path: etag for etag in etags}
    default_etag = ETag(year_num, "NA", "NA")

    default_team = create_team_obj(
        {"name": None, "team": None, "state": None, "country": None, "district": None}
    )
    teams_dict: Dict[int, Team] = defaultdict(lambda: default_team)
    for team in teams:
        teams_dict[team.team] = team

    year_teams: Set[int] = set()

    events, _ = get_events_tba(year_num, mock=mock, cache=cache)

    for event in events:
        event_obj = create_event_obj(event)
        event_key, event_time = event_obj.key, event_obj.time

        matches, new_etag = get_matches_tba(
            year_num, event_key, event_time, mock=mock, cache=cache
        )
        prev_etag = etags_dict.get(event_key + "/matches", default_etag).etag
        if new_etag != prev_etag and new_etag is not None:
            new_etags.append(ETag(year_num, event_key + "/matches", new_etag))

        current_match = 0 if len(matches) > 0 else -1
        qual_matches = 0 if len(matches) > 0 else -1

        # "Completed", "Upcoming", "Ongoing", or "Invalid"
        event_status = get_event_status(matches, year_num == end_year)
        event_obj.status = event_status

        event_teams: Set[int] = set()
        rankings: Dict[int, int] = defaultdict(int)
        if event_status == "Invalid":
            continue
        elif event_status == "Upcoming":
            temp_event_teams, _ = get_event_teams_tba(event_key, mock=mock, cache=cache)
            for team in temp_event_teams:
                event_teams.add(team)
                year_teams.add(team)
        elif event_status in ["Ongoing", "Completed"]:
            for match in matches:
                match["year"] = year_num
                match["offseason"] = event_obj.offseason
                match_obj, curr_team_match_objs = create_match_obj(match)
                current_match += match_obj.status == "Completed"
                qual_matches += not match_obj.playoff
                match_objs.append(match_obj)
                team_match_objs.extend(curr_team_match_objs)
                for team_match in curr_team_match_objs:
                    event_teams.add(team_match.team)
                    year_teams.add(team_match.team)

            rankings, _ = get_event_rankings_tba(event_key, mock=mock, cache=cache)

        # For Upcoming, Ongoing, and Completed events
        for team in event_teams:
            team_obj = teams_dict[team]
            team_event_objs.append(
                create_team_event_obj(
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
            )

        event_obj.current_match = current_match
        event_obj.qual_matches = qual_matches
        event_objs.append(event_obj)

    for team in year_teams:
        team_obj = teams_dict[team]
        team_year_objs.append(
            create_team_year_obj(
                {
                    "year": year_num,
                    "team": team,
                    "offseason": team >= MAX_TEAM,
                    "name": team_obj.name,
                    "state": team_obj.state,
                    "country": team_obj.country,
                    "district": team_obj.district,
                }
            )
        )

    return (
        (
            year_obj,
            team_year_objs,
            event_objs,
            team_event_objs,
            match_objs,
            team_match_objs,
        ),
        new_etags,
    )


def process_year_partial(
    year_num: int,
    objs: objs_type,
    etags: List[ETag],
    mock: bool = False,
    mock_index: int = 0,
) -> Tuple[objs_type, List[ETag]]:
    (y_obj, ty_objs, event_objs, team_event_objs, match_objs, team_match_objs) = objs

    etags_dict = {etag.path: etag for etag in etags}
    default_etag = ETag(year_num, "NA", "NA")
    new_etags: List[ETag] = []

    for event_obj in event_objs:
        if event_obj.status == "Completed":
            continue

        if not mock:
            start_date = datetime.strptime(event_obj.start_date, "%Y-%m-%d")
            end_date = datetime.strptime(event_obj.end_date, "%Y-%m-%d")
            if start_date - timedelta(days=1) > datetime.now():
                continue

            if end_date + timedelta(days=1) < datetime.now():
                continue

        # Load matches, if same as before then skip event
        prev_etag = etags_dict.get(event_obj.key + "/matches", default_etag).etag
        matches, new_etag = get_matches_tba(
            year_num,
            event_obj.key,
            event_obj.time,
            prev_etag,
            mock=mock,
            mock_index=mock_index,
            cache=False,
        )
        if new_etag == prev_etag and new_etag is not None:
            continue

        current_match = 0 if len(matches) > 0 else -1
        qual_matches = 0 if len(matches) > 0 else -1

        # "Completed", "Upcoming", "Ongoing", or "Invalid"
        event_status = get_event_status(matches, True)
        event_obj.status = event_status

        if event_status == "Invalid":
            continue
        elif event_status == "Upcoming":
            # Only update ongoing/recently completed events in partial update
            # Load new events every hour in full update
            continue
        elif event_status in ["Ongoing", "Completed"]:
            # Update event_obj, accumulate match_obj, team_match_objs
            event_match_keys = [m.key for m in match_objs if m.event == event_obj.key]
            for match in matches:
                match["year"] = year_num
                match["offseason"] = event_obj.offseason
                match_obj, curr_team_match_objs = create_match_obj(match)
                current_match += match_obj.status == "Completed"
                qual_matches += not match_obj.playoff
                if match_obj.key not in event_match_keys:
                    match_objs.append(match_obj)
                    team_match_objs.extend(curr_team_match_objs)
            event_obj.current_match = current_match
            event_obj.qual_matches = qual_matches

            # Update team_event_objs
            rankings, new_etag = get_event_rankings_tba(
                event_obj.key, None, mock=mock, mock_index=mock_index, cache=False
            )
            for team_event_obj in team_event_objs:
                if team_event_obj.event == event_obj.key:
                    team_event_obj.status = event_status
                    team_event_obj.rank = rankings.get(team_event_obj.team, -1)
                    team_event_obj.num_teams = len(rankings)

    return (
        (y_obj, ty_objs, event_objs, team_event_objs, match_objs, team_match_objs),
        new_etags,
    )


def post_process():
    remove_teams_with_no_events()
