from datetime import datetime
from typing import List

from db.functions.remove_teams_no_matches import remove_teams_with_no_matches
from db.main import clean_db
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
from db.read.event import get_num_events as get_num_events_db
from db.read.match import get_num_matches as get_num_matches_db
from db.read.team import get_num_teams as get_num_teams_db, get_teams as get_teams_db
from db.read.team_event import get_num_team_events as get_num_team_events_db
from db.read.team_match import get_num_team_matches
from db.read.team_year import (
    get_num_team_years as get_num_team_years_db,
    get_team_years as get_team_years_db,
)
from db.read.year import get_num_years as get_num_years_db
from db.write.main import (
    update_events as update_events_db,
    update_matches as update_matches_db,
    update_team_events as update_team_events_db,
    update_team_matches as update_team_matches_db,
    update_team_years as update_team_years_db,
    update_teams as update_teams_db,
    update_years as update_years_db,
)
from tba.clean_data import get_team_district as get_team_district_tba
from tba.read_tba import (
    get_events as get_events_tba,
    get_matches as get_matches_tba,
    get_team_events as get_team_events_tba,
    get_team_years as get_team_years_tba,
    get_teams as get_teams_tba,
)


def load_teams(cache: bool = True) -> None:
    print("Loading Teams")
    teams = get_teams_tba(cache=cache)
    team_objs = [create_team_obj(team) for team in teams]
    update_teams_db(team_objs, True)


def print_table_stats() -> None:
    print("Num Teams:", get_num_teams_db())
    print("Num Years:", get_num_years_db())
    print("Num Team Years:", get_num_team_years_db())
    print("Num Events:", get_num_events_db())
    print("Num Team Events:", get_num_team_events_db())
    print("Num Matches:", get_num_matches_db())
    print("Num Team Matches:", get_num_team_matches())


def process(start_year: int, end_year: int, cache: bool = True) -> None:
    clean_db()
    load_teams(cache=cache)
    all_team_nums = [t.id for t in get_teams_db()]
    for year in range(start_year, end_year + 1):
        print("Year:", str(year))
        start = datetime.now()
        year_obj = create_year_obj({"id": year})
        update_years_db([year_obj], True)

        team_year_objs: List[TeamYear] = []
        event_objs: List[Event] = []
        team_event_objs: List[TeamEvent] = []
        match_objs: List[Match] = []
        team_match_objs: List[TeamMatch] = []

        for team_year in get_team_years_tba(year, cache=cache):
            if team_year["team"] in all_team_nums:
                team_year_objs.append(create_team_year_obj(team_year))

        for event in get_events_tba(year, cache=cache):
            event_obj = create_event_obj(event)
            event_objs.append(event_obj)
            event_key, event_id, event_time = (
                event_obj.key,
                event_obj.id,
                event_obj.time,
            )
            for team_event in get_team_events_tba(event_key, cache=cache):
                team_event["year"] = year
                team_event["event_id"] = event_id
                team_event["time"] = event_time
                team_event_obj = create_team_event_obj(team_event)
                team_event_objs.append(team_event_obj)

            for match in get_matches_tba(year, event_key, event_time, cache=cache):
                match["year"] = year
                match["event"] = event_id
                match_obj, curr_team_match_objs = create_match_obj(match)
                match_objs.append(match_obj)
                team_match_objs.extend(curr_team_match_objs)

        update_team_years_db(team_year_objs, True)
        update_events_db(event_objs, True)
        update_team_events_db(team_event_objs, True)
        update_matches_db(match_objs, True)
        update_team_matches_db(team_match_objs, True)

        end = datetime.now()
        print("Time:", end - start)
        print()


# removes REALLY old teams and adds district labels
def post_process():
    print("Removing Old Teams")
    remove_teams_with_no_matches()

    active_teams = set([t.team_id for t in get_team_years_db(year=2020)])
    teams: List[Team] = []
    for team in get_teams_db():
        team.active = 1 if team.id in active_teams else 0
        if team.district is None:
            team.district = get_team_district_tba(team.id)
        teams.append(team)
    update_teams_db(teams, False)


def main(start_year: int, end_year: int, cache: bool = True) -> None:
    process(start_year, end_year, cache)
    post_process()
    print_table_stats()
