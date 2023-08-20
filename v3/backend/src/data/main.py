from typing import Dict, Tuple

from src.constants import CURR_YEAR
from src.data.avg import process_year as process_year_avg
from src.data.epa import (
    post_process as post_process_epa,
    process_year as process_year_epa,
)
from src.data.tba import (
    check_year_partial as check_year_partial_tba,
    create_objs as create_objs_tba,
    load_teams as load_teams_tba,
    post_process as post_process_tba,
    process_year as process_year_tba,
)
from src.data.utils import (
    Timer,
    objs_type,
    read_objs as read_objs_db,
    write_objs as write_objs_db,
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


def get_team_years_dict(
    year: int,
) -> Tuple[Dict[int, Dict[str, TeamYear]], Dict[int, Tuple[float, float]]]:
    team_years_dict: Dict[int, Dict[str, TeamYear]] = {}  # main dictionary
    year_epa_stats: Dict[int, Tuple[float, float]] = {}
    for temp_year in range(max(2002, year - 4), year):
        teams_dict = {t.team: t for t in get_team_years_db(year=temp_year)}
        team_years_dict[temp_year] = teams_dict

        year_epa_stats[temp_year] = (0, 0)
        year_obj = get_year_db(year=temp_year)
        if year_obj is not None:
            num_teams = 2 if temp_year <= 2004 else 3
            mean, sd = year_obj.score_mean, year_obj.score_sd
            year_epa_stats[temp_year] = ((mean or 0) / num_teams, (sd or 0) / num_teams)

    return team_years_dict, year_epa_stats


def reset_all_years(start_year: int, end_year: int):
    timer = Timer()

    end_year = 2002

    clean_db()
    timer.print("Clean DB")

    teams = load_teams_tba(cache=True)
    timer.print("Load Teams")

    update_teams_db(teams, True)
    timer.print("Update DB")

    team_years_dict, year_epa_stats = get_team_years_dict(start_year)
    for year_num in range(start_year, end_year + 1):
        objs = create_objs_tba(year_num)

        # TODO: temporarily year_num < end_year replaced with True
        objs, new_etags = process_year_tba(year_num, teams, objs, [], False, True)
        timer.print(str(year_num) + " TBA")

        year = process_year_avg(objs[0], objs[5])
        timer.print(str(year_num) + " AVG")

        objs: objs_type = (year, *objs[1:])

        out = process_year_epa(year_num, team_years_dict, *objs, year_epa_stats)
        timer.print(str(year_num) + " EPA")

        team_years_dict = out[0]
        objs = out[1:]

        write_objs_db(year_num, *objs, new_etags, True)
        timer.print(str(year_num) + " Write")

        num_teams = 2 if year_num <= 2004 else 3
        new_mean = (objs[0].score_mean or 0) / num_teams
        new_sd = (objs[0].score_sd or 0) / num_teams
        year_epa_stats[year_num] = (new_mean, new_sd)

    post_process_tba()
    timer.print("Post TBA")

    post_process_epa(end_year)
    timer.print("Post EPA")


def update_single_year(year: int, partial: bool):
    timer = Timer()

    teams = get_teams_db()
    timer.print("Load Teams")

    etags = get_etags_db(year)
    timer.print("Load ETags")

    if partial:
        event_objs = get_events_db(year=year, offseason=None)
        is_new_data = check_year_partial_tba(year, event_objs, etags)
        timer.print("Check TBA")

        if not is_new_data:
            return

    if partial:
        objs: objs_type = read_objs_db(year)
        timer.print("Read Objs")
    else:
        objs = create_objs_tba(year)

    objs_dict = {}
    objs_dict[0] = str(objs[0])
    objs_dict[1] = {x.team + "_" + str(x.year): str(x) for x in objs[1]}
    objs_dict[2] = {x.key: str(x) for x in objs[2]}
    objs_dict[3] = {x.team + "_" + x.event: str(x) for x in objs[3]}
    objs_dict[4] = {x.key: str(x) for x in objs[4]}
    objs_dict[5] = {x.match + "_" + x.alliance: str(x) for x in objs[5]}
    objs_dict[6] = {str(x.team) + "_" + x.match: str(x) for x in objs[6]}

    team_years_dict, year_epa_stats = get_team_years_dict(year)

    objs, new_etags = process_year_tba(year, teams, objs, etags, partial, False)
    timer.print(str(year) + " TBA")

    year_obj = process_year_avg(objs[0], objs[5])
    timer.print(str(year) + " AVG")

    objs = (year_obj, *objs[1:])

    out = process_year_epa(year, team_years_dict, *objs, year_epa_stats)
    timer.print(str(year) + " EPA")

    team_years_dict = out[0]
    objs = out[1:]

    if partial:
        # TODO: reduce code duplication
        year_obj = objs[0]
        curr_dict = {str(x.team) + "_" + str(x.year): x for x in objs[1]}
        ty_objs = [x for k, x in curr_dict.items() if str(x) != objs_dict[1].get(k, "")]
        curr_dict = {x.key: x for x in objs[2]}
        e_objs = [x for k, x in curr_dict.items() if str(x) != objs_dict[2].get(k, "")]
        curr_dict = {str(x.team) + "_" + x.event: x for x in objs[3]}
        te_objs = [x for k, x in curr_dict.items() if str(x) != objs_dict[3].get(k, "")]
        curr_dict = {x.key: x for x in objs[4]}
        m_objs = [x for k, x in curr_dict.items() if str(x) != objs_dict[4].get(k, "")]
        curr_dict = {x.match + "_" + x.alliance: x for x in objs[5]}
        a_objs = [x for k, x in curr_dict.items() if str(x) != objs_dict[5].get(k, "")]
        curr_dict = {str(x.team) + "_" + x.match: x for x in objs[6]}
        tm_objs = [x for k, x in curr_dict.items() if str(x) != objs_dict[6].get(k, "")]
        new_objs = (year_obj, ty_objs, e_objs, te_objs, m_objs, a_objs, tm_objs)

        # print(len(ty_objs), len(e_objs), len(te_objs), len(m_objs), len(a_objs), len(tm_objs))

        write_objs_db(year, *new_objs, new_etags, False)
        timer.print(str(year) + " Write")
    else:
        # Changed to False to prevent deleting data without a backup
        write_objs_db(year, *objs, new_etags, False)
        timer.print(str(year) + " Write")

        if year == CURR_YEAR:
            post_process_tba()
            timer.print("Post TBA")

            post_process_epa(year)
            timer.print("Post EPA")
