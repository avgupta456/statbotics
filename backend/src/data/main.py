from typing import Dict

from src.data.avg import process_year as process_year_avg
from src.data.tba import (
    load_teams,
    post_process as post_process_tba,
    process_year as process_year_tba,
    process_year_partial as process_year_partial_tba,
)
from src.data.utils import (
    objs_type,
    print_table_stats,
    read_objs,
    time_func,
    write_objs,
)
from src.db.main import clean_db
from src.db.models.team_year import TeamYear
from src.db.read.team import get_teams as get_teams_db
from src.db.read.team_year import get_team_years as get_team_years_db
from src.db.write.main import update_teams as update_teams_db


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


def reset_curr_year(curr_year: int):
    teams = time_func("Load Teams", get_teams_db)

    team_years_dict: Dict[int, Dict[int, TeamYear]] = {}  # master dictionary
    # Need up to four years of previous data for rating initialization
    for year in range(max(2002, curr_year - 4), curr_year):
        teams_dict = {t.team: t for t in get_team_years_db(year)}
        team_years_dict[year] = teams_dict

    # NOTE: True normally False
    objs: objs_type = time_func(
        str(curr_year) + " TBA", process_year_tba, curr_year, curr_year, teams, True  # type: ignore
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

    time_func("Write", write_objs, curr_year, *objs, curr_year, True)  # type: ignore
    """
    post_process_elo(end_year)
    """
    time_func("Post TBA", post_process_tba)
    print_table_stats()


def update_curr_year(curr_year: int):
    objs = time_func("Load Objs", read_objs, curr_year)  # type: ignore

    objs_dict = {}
    objs_dict[0] = str(objs[0])
    objs_dict[1] = {str(x.team) + "_" + str(x.year): str(x) for x in objs[1]}
    objs_dict[2] = {x.key: str(x) for x in objs[2]}
    objs_dict[3] = {str(x.team) + "_" + x.event: str(x) for x in objs[3]}
    objs_dict[4] = {x.key: str(x) for x in objs[4]}
    objs_dict[5] = {str(x.team) + "_" + x.match: str(x) for x in objs[5]}

    objs: objs_type = time_func(
        str(curr_year) + " TBA", process_year_partial_tba, curr_year, objs  # type: ignore
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

    year_obj = objs[0]
    curr_dict = {str(x.team) + "_" + str(x.year): x for x in objs[1]}
    ty_objs = [x for k, x in curr_dict.items() if str(x) != objs_dict[1].get(k, "")]
    curr_dict = {x.key: x for x in objs[2]}
    e_objs = [x for k, x in curr_dict.items() if str(x) != objs_dict[2].get(k, "")]
    curr_dict = {str(x.team) + "_" + x.event: x for x in objs[3]}
    te_objs = [x for k, x in curr_dict.items() if str(x) != objs_dict[3].get(k, "")]
    curr_dict = {x.key: x for x in objs[4]}
    m_objs = [x for k, x in curr_dict.items() if str(x) != objs_dict[4].get(k, "")]
    curr_dict = {str(x.team) + "_" + x.match: x for x in objs[5]}
    tm_objs = [x for k, x in curr_dict.items() if str(x) != objs_dict[5].get(k, "")]
    new_objs = (year_obj, ty_objs, e_objs, te_objs, m_objs, tm_objs)

    time_func("Write", write_objs, curr_year, *new_objs, curr_year, False)  # type: ignore
    print_table_stats()
