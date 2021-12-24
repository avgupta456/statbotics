from datetime import datetime
from typing import Dict, List, Tuple

from db.main import clean_db
from db.models.event import Event
from db.models.match import Match
from db.models.team import Team
from db.models.team_event import TeamEvent
from db.models.team_match import TeamMatch
from db.models.team_year import TeamYear
from db.models.year import Year
from db.read.event import get_num_events as get_num_events_db
from db.read.match import get_num_matches as get_num_matches_db
from db.read.team import get_num_teams as get_num_teams_db
from db.read.team_event import get_num_team_events as get_num_team_events_db
from db.read.team_match import get_num_team_matches
from db.read.team_year import get_num_team_years as get_num_team_years_db
from db.read.year import get_num_years as get_num_years_db
from db.write.main import (
    update_events as update_events_db,
    update_matches as update_matches_db,
    update_teams as update_teams_db,
    update_team_years as update_team_years_db,
    update_team_events as update_team_events_db,
    update_team_matches as update_team_matches_db,
    update_years as update_years_db,
)

from process.process_tba import (
    load_teams,
    process_year as process_year_tba,
    post_process as post_process_tba,
)
from process.process_avg import process_year as process_year_avg
from process.process_elo import (
    process_year as process_year_elo,
    post_process as post_process_elo,
)
from process.process_opr import process_year as process_year_opr


def write_teams(teams: List[Team]) -> None:
    update_teams_db(teams, True)


def write_objs(
    year: Year,
    team_years: List[TeamYear],
    events: List[Event],
    team_events: List[TeamEvent],
    matches: List[Match],
    team_matches: List[TeamMatch],
) -> None:
    # removes records with no events/matches
    team_years = [t for t in team_years if t.elo_end > 0]
    team_ids = [t.team_id for t in team_years]
    team_events = [t for t in team_events if t.team_id in team_ids]
    event_ids = set([t.event_id for t in team_events])
    events = [e for e in events if e.id in event_ids]

    # writes to db
    update_years_db([year], True)
    update_team_years_db(team_years, True)
    update_events_db(events, True)
    update_team_events_db(team_events, True)
    update_matches_db(matches, True)
    update_team_matches_db(team_matches, True)


def print_table_stats() -> None:
    print("Num Teams:", get_num_teams_db())
    print("Num Years:", get_num_years_db())
    print("Num Team Years:", get_num_team_years_db())
    print("Num Events:", get_num_events_db())
    print("Num Team Events:", get_num_team_events_db())
    print("Num Matches:", get_num_matches_db())
    print("Num Team Matches:", get_num_team_matches())


def process_main(start_year: int, end_year: int):
    main_start = datetime.now()

    print("Pre Processing")
    overall_start = datetime.now()
    start = overall_start
    clean_db()
    print("Clean\t", datetime.now() - start)
    start = datetime.now()
    teams = load_teams()
    print("Load\t", datetime.now() - start)
    start = datetime.now()
    write_teams(teams)
    print("Write\t", datetime.now() - start)
    print("Total\t", datetime.now() - overall_start)
    print()

    print("Processing")
    all_team_nums = [t.id for t in teams]
    team_years_dict: Dict[int, Dict[int, TeamYear]] = {}  # master dictionary
    means: Dict[int, float] = {}  # for OPR seed ratings
    for year_num in range(start_year, end_year + 1):
        overall_start = datetime.now()
        start = overall_start
        objs_type = Tuple[
            Year,
            List[TeamYear],
            List[Event],
            List[TeamEvent],
            List[Match],
            List[TeamMatch],
        ]
        objs: objs_type = process_year_tba(year_num, all_team_nums)
        print(year_num, "\tTBA\t", datetime.now() - start)
        start = datetime.now()

        year = process_year_avg(objs[0], objs[2], objs[4])
        objs = (year, *objs[1:])
        print(year_num, "\tAvg\t", datetime.now() - start)
        start = datetime.now()

        out = process_year_elo(year_num, team_years_dict, *objs)
        team_years_dict = out[0]
        objs = out[1:]
        print(year_num, "\tElo\t", datetime.now() - start)
        start = datetime.now()

        out = process_year_opr(year_num, team_years_dict, means, *objs)
        team_years_dict = out[0]
        means = out[1]
        objs = out[2:]
        print(year_num, "\tOPR\t", datetime.now() - start)
        start = datetime.now()

        write_objs(*objs)
        print(year_num, "\tWrite\t", datetime.now() - start)
        start = datetime.now()

        print(year_num, "\tTotal\t", datetime.now() - overall_start)
        print()

    print("Post Processing")
    overall_start = datetime.now()
    start = overall_start
    post_process_elo(end_year)
    print("Elo\t", datetime.now() - start)
    start = datetime.now()
    post_process_tba()
    print("TBA\t", datetime.now() - start)
    print("Total\t", datetime.now() - overall_start)

    print()
    print("Main\t", datetime.now() - main_start)

    print()
    print_table_stats()
