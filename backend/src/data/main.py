from typing import Dict

from src.data.avg import process_year as process_year_avg
from src.data.tba import (
    load_teams,
    post_process as post_process_tba,
    process_year as process_year_tba,
    process_year_partial as process_year_partial_tba,
)
from src.data.utils import objs_type
from src.db.main import clean_db
from src.db.models.team_year import TeamYear
from src.db.read.team import get_teams as get_teams_db
from src.db.read.team_year import get_team_years as get_team_years_db
from src.db.write.main import update_teams as update_teams_db
from src.data.utils import write_objs, print_table_stats
from src.data.utils import time_func


def reset_all_years(start_year: int, end_year: int):
    time_func("Clean DB", clean_db)
    teams = time_func("Load Teams", load_teams, cache=True)  # type: ignore
    time_func("Update DB", update_teams_db, teams, True)  # type: ignore

    team_years_dict: Dict[int, Dict[int, TeamYear]] = {}  # main dictionary
    for year in range(max(2002, start_year - 4), start_year):
        teams_dict = {t.team: t for t in get_team_years_db(year)}
        team_years_dict[year] = teams_dict

    for year_num in range(start_year, end_year + 1):
        objs: objs_type = time_func(
            str(year_num) + " TBA", process_year_tba, year_num, end_year, teams, year_num <= end_year  # type: ignore
        )
        year = time_func(
            str(year_num) + " AVG", process_year_avg, objs[0], objs[2], objs[4]  # type: ignore
        )
        objs = (year, *objs[1:])

        """
        out = process_year_elo(year_num, team_years_dict, *objs)
        team_years_dict = out[0]
        objs = out[1:]
        """

        time_func(str(year_num) + " Write", write_objs, year_num, *objs, end_year, True)  # type: ignore

    """
    post_process_elo(end_year)
    """

    time_func("Post TBA", post_process_tba)
    print_table_stats()


def reset_curr_year(curr_year: int, clean: bool = True):
    teams = time_func("Load Teams", get_teams_db)

    team_years_dict: Dict[int, Dict[int, TeamYear]] = {}  # master dictionary
    # Need up to four years of previous data for rating initialization
    for year in range(max(2002, curr_year - 4), curr_year):
        teams_dict = {t.team: t for t in get_team_years_db(year)}
        team_years_dict[year] = teams_dict

    objs: objs_type = time_func(
        str(curr_year) + " TBA", process_year_tba, curr_year, curr_year, teams, False  # type: ignore
    )
    year = time_func(
        str(curr_year) + " AVG", process_year_avg, objs[0], objs[2], objs[4]  # type: ignore
    )
    objs = (year, *objs[1:])

    """
    out = process_year_elo(year_num, team_years_dict, *objs)
    team_years_dict = out[0]
    objs = out[1:]
    """

    time_func("Write", write_objs, curr_year, *objs, curr_year, clean)  # type: ignore
    """
    post_process_elo(end_year)
    """
    time_func("Post TBA", post_process_tba)
    print_table_stats()


def update_curr_year(curr_year: int):
    teams = time_func("Load Teams", get_teams_db)

    objs: objs_type = time_func(
        str(curr_year) + " TBA", process_year_partial_tba, curr_year, curr_year, teams  # type: ignore
    )
    year = time_func(
        str(curr_year) + " AVG", process_year_avg, objs[0], objs[2], objs[4]  # type: ignore
    )
    objs = (year, *objs[1:])

    """
    out = process_year_elo(year_num, team_years_dict, *objs)
    team_years_dict = out[0]
    objs = out[1:]
    """

    time_func("Write", write_objs, curr_year, *objs, curr_year, False)  # type: ignore
    print_table_stats()
