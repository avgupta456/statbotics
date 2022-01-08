from typing import List, Tuple

from db.functions.remove_teams_no_events import remove_teams_with_no_events
from db.models.create import (
    create_event_obj,
    create_match_obj,
    create_team_event_obj,
    create_team_obj,
    create_team_year_obj,
    create_year_obj,
)
from db.models.event import Event
from db.models.match import Match
from db.models.team import Team
from db.models.team_event import TeamEvent
from db.models.team_match import TeamMatch
from db.models.team_year import TeamYear
from db.models.year import Year
from tba.clean_data import get_team_district as get_team_district_tba
from tba.read_tba import (
    get_events as get_events_tba,
    get_matches as get_matches_tba,
    get_team_events as get_team_events_tba,
    get_team_years as get_team_years_tba,
    get_teams as get_teams_tba,
)


def load_teams(cache: bool = True) -> List[Team]:
    teams = get_teams_tba(cache=cache)
    team_objs = [create_team_obj(team) for team in teams]
    for team in team_objs:
        if team.district is None:
            team.district = get_team_district_tba(team.team)
    return team_objs


def process_year(
    year_num: int,
    end_year: int,
    teams: List[Team],
    cache: bool = True,
    fake_matches: bool = False,
) -> Tuple[
    Year, List[TeamYear], List[Event], List[TeamEvent], List[Match], List[TeamMatch]
]:
    year_obj = create_year_obj({"year": year_num})

    team_year_objs: List[TeamYear] = []
    event_objs: List[Event] = []
    team_event_objs: List[TeamEvent] = []
    match_objs: List[Match] = []
    team_match_objs: List[TeamMatch] = []

    teams_dict = {team.team: team for team in teams}

    for team_year in get_team_years_tba(year_num, cache=cache):
        if team_year["team"] in teams_dict:
            team_obj = teams_dict[team_year["team"]]
            team_year["name"] = team_obj.name
            team_year["state"] = team_obj.state
            team_year["country"] = team_obj.country
            team_year["district"] = team_obj.district
            team_year_objs.append(create_team_year_obj(team_year))

    for event in get_events_tba(year_num, cache=cache):
        event_obj = create_event_obj(event)
        event_key, event_time = event_obj.key, event_obj.time

        team_events = get_team_events_tba(event_key, cache=cache)
        team_nums = [team_event["team"] for team_event in team_events]
        fake_matches_num = event_obj.week if fake_matches and len(team_nums) > 24 else 0
        matches = get_matches_tba(
            year_num,
            event_key,
            event_time,
            cache=cache,
            teams=team_nums,
            fake_matches=fake_matches_num,
        )
        num_matches = len(matches)
        num_upcoming_matches = 0
        for match in matches:
            if match["status"] == "Upcoming":
                num_upcoming_matches += 1

        event_status = "Completed"
        if year_num == end_year:
            event_status = (
                "Upcoming"
                if num_matches == 0
                else ("Ongoing" if num_upcoming_matches > 0 else "Completed")
            )

        if event_status == "Completed" and num_matches == 0:
            continue

        for match in matches:
            match["year"] = year_num
            match_obj, curr_team_match_objs = create_match_obj(match)
            match_objs.append(match_obj)
            team_match_objs.extend(curr_team_match_objs)

        for team_event in team_events:
            team_event["year"] = year_num
            team_event["event"] = event_key
            team_event["event_name"] = event_obj.name
            team_event["state"] = event_obj.state
            team_event["country"] = event_obj.country
            team_event["district"] = event_obj.district
            team_event["type"] = event_obj.type
            team_event["week"] = event_obj.week
            team_event["time"] = event_time
            team_event["status"] = event_status

            if team_event["team"] not in teams_dict:
                continue
            team_obj = teams_dict[team_event["team"]]
            team_event["team_name"] = team_obj.name

            team_event_obj = create_team_event_obj(team_event)
            team_event_objs.append(team_event_obj)

        event_obj.status = event_status
        event_objs.append(event_obj)

    return (
        year_obj,
        team_year_objs,
        event_objs,
        team_event_objs,
        match_objs,
        team_match_objs,
    )


def post_process():
    remove_teams_with_no_events()
