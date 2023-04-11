from typing import Dict, Tuple

from src.constants import CURR_YEAR
from src.data.avg import process_year as process_year_avg
from src.data.epa import (
    post_process as post_process_epa,
    process_year as process_year_epa,
)
from src.data.tba import (
    check_year_partial as check_year_partial_tba,
    load_teams as load_teams_tba,
    post_process as post_process_tba,
    process_year as process_year_tba,
    process_year_partial as process_year_partial_tba,
)
from src.data.utils import (  # print_table_stats,
    objs_type,
    read_objs,
    time_func,
    write_objs,
)
from src.db.main import clean_db
from src.db.models import TeamYear
from src.db.read import (
    get_etags as get_etags_db,
    get_events as get_events_db,
    get_team_years as get_team_years_db,
    get_teams as get_teams_db,
    get_year as get_year_db,
)
from src.db.write.main import update_teams as update_teams_db


def reset_all_years(start_year: int, end_year: int):
    time_func("Clean DB", clean_db)
    teams = time_func("Load Teams", load_teams_tba, cache=True)  # type: ignore
    time_func("Update DB", update_teams_db, teams, True)  # type: ignore

    team_years_dict: Dict[int, Dict[int, TeamYear]] = {}  # main dictionary
    year_epa_stats: Dict[int, Tuple[float, float]] = {}
    for year in range(max(2002, start_year - 4), start_year):
        teams_dict = {t.team: t for t in get_team_years_db(year=year)}
        team_years_dict[year] = teams_dict

        year_epa_stats[year] = (0, 0)
        year_obj = get_year_db(year=year)
        if year_obj is not None:
            num_teams = 2 if year <= 2004 else 3
            mean, sd = year_obj.score_mean, year_obj.score_sd
            year_epa_stats[year] = ((mean or 0) / num_teams, (sd or 0) / num_teams)

    for year_num in range(start_year, end_year + 1):
        objs, new_etags = time_func(
            str(year_num) + " TBA", process_year_tba, year_num, teams, [], False, year_num < end_year  # type: ignore
        )
        year = time_func(
            str(year_num) + " AVG", process_year_avg, objs[0], objs[2], objs[4]  # type: ignore
        )
        objs: objs_type = (year, *objs[1:])

        out = time_func(str(year_num) + " EPA", process_year_epa, year_num, team_years_dict, *objs, year_epa_stats)  # type: ignore
        team_years_dict = out[0]
        objs = out[1:]

        time_func(str(year_num) + " Write", write_objs, year_num, *objs, new_etags, end_year, True)  # type: ignore

        num_teams = 2 if year_num <= 2004 else 3
        new_mean = (objs[0].score_mean or 0) / num_teams
        new_sd = (objs[0].score_sd or 0) / num_teams
        year_epa_stats[year_num] = (new_mean, new_sd)

    time_func("Post TBA", post_process_tba)
    time_func("Post EPA", lambda: post_process_epa(end_year))
    # print_table_stats()


def reset_curr_year(curr_year: int, mock: bool = False):
    teams = time_func("Load Teams", get_teams_db)
    etags = time_func("Load ETags", get_etags_db, curr_year)  # type: ignore

    team_years_dict: Dict[int, Dict[int, TeamYear]] = {}  # main dictionary
    year_epa_stats: Dict[int, Tuple[float, float]] = {}
    for year in range(max(2002, curr_year - 4), curr_year):
        teams_dict = {t.team: t for t in get_team_years_db(year=year)}
        team_years_dict[year] = teams_dict

        year_epa_stats[year] = (0, 0)
        year_obj = get_year_db(year=year)
        if year_obj is not None:
            num_teams = 2 if year <= 2004 else 3
            mean, sd = year_obj.score_mean, year_obj.score_sd
            year_epa_stats[year] = ((mean or 0) / num_teams, (sd or 0) / num_teams)

    objs, new_etags = time_func(
        str(curr_year) + " TBA", process_year_tba, curr_year, teams, etags, mock, False  # type: ignore
    )
    year = time_func(
        str(curr_year) + " AVG", process_year_avg, objs[0], objs[2], objs[4]  # type: ignore
    )
    objs = (year, *objs[1:])

    out = time_func(str(curr_year) + " EPA", process_year_epa, curr_year, team_years_dict, *objs, year_epa_stats)  # type: ignore
    team_years_dict = out[0]
    objs = out[1:]

    # Changed to False to prevent deleting data without a backup
    time_func("Write", write_objs, curr_year, *objs, new_etags, curr_year, False)  # type: ignore

    if curr_year == CURR_YEAR:
        time_func("Post TBA", post_process_tba)
        time_func("Post EPA", lambda: post_process_epa(curr_year))


def update_curr_year(curr_year: int, mock: bool = False, mock_index: int = 0):
    etags = time_func("Load ETags", get_etags_db, curr_year)  # type: ignore

    if not mock:
        event_objs = time_func("Load Events", get_events_db, curr_year)  # type: ignore
        is_new_data = time_func("Check TBA", check_year_partial_tba, curr_year, event_objs, etags)  # type: ignore
        if not is_new_data:
            return

    objs: objs_type = time_func("Load Objs", read_objs, curr_year)  # type: ignore

    objs_dict = {}
    objs_dict[0] = str(objs[0])
    objs_dict[1] = {str(x.team) + "_" + str(x.year): str(x) for x in objs[1]}
    objs_dict[2] = {x.key: str(x) for x in objs[2]}
    objs_dict[3] = {str(x.team) + "_" + x.event: str(x) for x in objs[3]}
    objs_dict[4] = {x.key: str(x) for x in objs[4]}
    objs_dict[5] = {str(x.team) + "_" + x.match: str(x) for x in objs[5]}

    team_years_dict: Dict[int, Dict[int, TeamYear]] = {}  # main dictionary
    year_epa_stats: Dict[int, Tuple[float, float]] = {}
    for year in range(max(2002, curr_year - 4), curr_year):
        teams_dict = {t.team: t for t in get_team_years_db(year=year)}
        team_years_dict[year] = teams_dict

        year_epa_stats[year] = (0, 0)
        year_obj = get_year_db(year=year)
        if year_obj is not None:
            num_teams = 2 if year <= 2004 else 3
            mean, sd = year_obj.score_mean, year_obj.score_sd
            year_epa_stats[year] = ((mean or 0) / num_teams, (sd or 0) / num_teams)

    objs, new_etags = time_func(
        str(curr_year) + " TBA", process_year_partial_tba, curr_year, objs, etags, mock, mock_index  # type: ignore
    )
    year = time_func(
        str(curr_year) + " AVG", process_year_avg, objs[0], objs[2], objs[4]  # type: ignore
    )
    objs = (year, *objs[1:])

    out = time_func(str(curr_year) + " EPA", process_year_epa, curr_year, team_years_dict, *objs, year_epa_stats)  # type: ignore
    team_years_dict = out[0]
    objs = out[1:]

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

    # print(len(ty_objs), len(e_objs), len(te_objs), len(m_objs), len(tm_objs))

    time_func("Write", write_objs, curr_year, *new_objs, new_etags, curr_year, False)  # type: ignore
