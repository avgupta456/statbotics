from typing import Any, Dict, List, Set, Tuple

from src.data.utils import objs_type
from src.db.functions.remove_teams_no_events import remove_teams_with_no_events
from src.db.models.create import (
    create_event_obj,
    create_match_obj,
    create_team_event_obj,
    create_team_obj,
    create_team_year_obj,
    create_year_obj,
)
from src.db.models.etag import ETag
from src.db.models.event import Event
from src.db.models.match import Match
from src.db.models.team import Team
from src.db.models.team_event import TeamEvent
from src.db.models.team_match import TeamMatch
from src.db.models.team_year import TeamYear
from src.tba.read_tba import (
    get_event_rankings as get_event_rankings_tba,
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
    cache: bool = True,
) -> Tuple[objs_type, List[ETag]]:
    year_obj = create_year_obj({"year": year_num})
    team_year_objs: List[TeamYear] = []
    event_objs: List[Event] = []
    team_event_objs: List[TeamEvent] = []
    match_objs: List[Match] = []
    team_match_objs: List[TeamMatch] = []

    etags_dict = {etag.path: etag for etag in etags}
    default_etag = ETag(year_num, "NA", "NA")
    new_etags: List[ETag] = []

    teams_dict = {team.team: team for team in teams}
    year_teams: Set[int] = set()

    events, _ = get_events_tba(year_num, cache=cache)

    for event in events:
        event_teams: Set[int] = set()

        event_obj = create_event_obj(event)
        event_key, event_time = event_obj.key, event_obj.time

        matches, new_etag = get_matches_tba(
            year_num, event_key, event_time, cache=cache
        )
        prev_etag = etags_dict.get(event_key + "/matches", default_etag).etag
        if new_etag != prev_etag and new_etag is not None:
            new_etags.append(ETag(year_num, event_key + "/matches", new_etag))

        # Hack: remove "Upcoming" matches once finals finished
        finals = [m["status"] for m in matches if m["comp_level"] == "f"]
        if len(finals) >= 2 and set(finals) == {"Completed"}:
            matches = [m for m in matches if m["status"] == "Completed"]

        # "Completed", "Upcoming", "Ongoing", or "Invalid"
        event_status = get_event_status(matches, year_num == end_year)
        if event_status == "Invalid":
            continue
        event_obj.status = event_status

        rankings, _ = get_event_rankings_tba(event_key, cache=cache)

        current_match = 0 if len(matches) > 0 else -1
        qual_matches = 0 if len(matches) > 0 else -1
        for match in matches:
            match["year"] = year_num
            match_obj, curr_team_match_objs = create_match_obj(match)
            current_match += match_obj.status == "Completed"
            qual_matches += not match_obj.playoff
            match_objs.append(match_obj)
            team_match_objs.extend(curr_team_match_objs)
            for team_match in curr_team_match_objs:
                event_teams.add(team_match.team)
                year_teams.add(team_match.team)

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
    year_num: int, objs: objs_type, etags: List[ETag]
) -> Tuple[objs_type, List[ETag]]:
    (y_obj, ty_objs, event_objs, team_event_objs, match_objs, team_match_objs) = objs

    etags_dict = {etag.path: etag for etag in etags}
    default_etag = ETag(year_num, "NA", "NA")
    new_etags: List[ETag] = []

    for event_obj in event_objs:
        if event_obj.status == "Completed":
            continue

        # Load matches, if same as before then skip event
        prev_etag = etags_dict.get(event_obj.key + "/matches", default_etag).etag
        matches, new_etag = get_matches_tba(
            year_num, event_obj.key, event_obj.time, prev_etag, False
        )
        if new_etag == prev_etag and new_etag is not None:
            continue

        # Hack: remove "Upcoming" matches once finals start
        finals = [m["status"] for m in matches if m["comp_level"] == "f"]
        if len(finals) >= 2 and set(finals) == {"Completed"}:
            matches = [m for m in matches if m["status"] == "Completed"]

        # "Completed", "Upcoming", "Ongoing", or "Invalid"
        event_status = get_event_status(matches, True)
        if event_status == "Invalid":
            continue
        event_obj.status = event_status

        event_match_keys = [m.key for m in match_objs if m.event == event_obj.key]
        current_match = 0 if len(matches) > 0 else -1
        qual_matches = 0 if len(matches) > 0 else -1
        for match in matches:
            match["year"] = year_num
            match_obj, curr_team_match_objs = create_match_obj(match)
            current_match += match_obj.status == "Completed"
            qual_matches += not match_obj.playoff
            if match_obj.key not in event_match_keys:
                match_objs.append(match_obj)
                team_match_objs.extend(curr_team_match_objs)

        rankings, new_etag = get_event_rankings_tba(event_obj.key, None, False)
        for team_event_obj in team_event_objs:
            if team_event_obj.event == event_obj.key:
                team_event_obj.status = event_status
                team_event_obj.rank = rankings.get(team_event_obj.team, -1)
                team_event_obj.num_teams = len(rankings)

        event_obj.current_match = current_match
        event_obj.qual_matches = qual_matches

    return (
        (y_obj, ty_objs, event_objs, team_event_objs, match_objs, team_match_objs),
        new_etags,
    )


def post_process():
    remove_teams_with_no_events()
