from typing import List, Tuple

from db.functions.remove_teams_no_matches import remove_teams_with_no_matches
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
from db.read.team import get_teams as get_teams_db
from db.read.team_year import get_team_years as get_team_years_db
from db.write.main import update_teams as update_teams_db
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
    return team_objs


def process_year(
    year_num: int, all_team_nums: List[int], cache: bool = True
) -> Tuple[
    Year, List[TeamYear], List[Event], List[TeamEvent], List[Match], List[TeamMatch]
]:
    year_obj = create_year_obj({"id": year_num})

    team_year_objs: List[TeamYear] = []
    event_objs: List[Event] = []
    team_event_objs: List[TeamEvent] = []
    match_objs: List[Match] = []
    team_match_objs: List[TeamMatch] = []

    for team_year in get_team_years_tba(year_num, cache=cache):
        if team_year["team"] in all_team_nums:
            team_year_objs.append(create_team_year_obj(team_year))

    for event in get_events_tba(year_num, cache=cache):
        event_obj = create_event_obj(event)
        event_objs.append(event_obj)
        event_key, event_id, event_time = (
            event_obj.key,
            event_obj.id,
            event_obj.time,
        )
        for team_event in get_team_events_tba(event_key, cache=cache):
            team_event["year"] = year_num
            team_event["event_id"] = event_id
            team_event["time"] = event_time
            team_event_obj = create_team_event_obj(team_event)
            team_event_objs.append(team_event_obj)

        for match in get_matches_tba(year_num, event_key, event_time, cache=cache):
            match["year"] = year_num
            match["event"] = event_id
            match_obj, curr_team_match_objs = create_match_obj(match)
            match_objs.append(match_obj)
            team_match_objs.extend(curr_team_match_objs)

    return (
        year_obj,
        team_year_objs,
        event_objs,
        team_event_objs,
        match_objs,
        team_match_objs,
    )


def post_process():
    remove_teams_with_no_matches()

    active_teams = set([t.team_id for t in get_team_years_db(year=2020)])
    teams: List[Team] = []
    for team in get_teams_db():
        team.active = 1 if team.id in active_teams else 0
        if team.district is None:
            team.district = get_team_district_tba(team.id)
        teams.append(team)
    update_teams_db(teams, False)
