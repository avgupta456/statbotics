from typing import Dict

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
)
from src.data.utils import (
    Timer,
    objs_type,
    read_objs as read_objs_db,
    write_objs as write_objs_db,
    create_objs,
)
from src.db.main import clean_db
from src.db.models import TeamYear
from src.db.read import (
    get_etags as get_etags_db,
    get_events as get_events_db,
    get_team_years as get_team_years_db,
    get_teams as get_teams_db,
)
from src.db.write.main import update_teams as update_teams_db


def get_team_years_dict(year: int) -> Dict[int, Dict[str, TeamYear]]:
    team_years_dict: Dict[int, Dict[str, TeamYear]] = {}
    for temp_year in range(max(2002, year - 4), year):
        teams_dict = {t.team: t for t in get_team_years_db(year=temp_year)}
        team_years_dict[temp_year] = teams_dict

    return team_years_dict


def reset_all_years(start_year: int, end_year: int):
    timer = Timer()

    start_year = 2023
    end_year = 2023

    clean_db()
    timer.print("Clean DB")

    teams = load_teams_tba(cache=True)
    timer.print("Load Teams")

    update_teams_db(teams, True)
    timer.print("Update DB")

    # team_years_dict = get_team_years_dict(start_year)
    for year_num in range(start_year, end_year + 1):
        objs = create_objs(year_num)

        # TODO: temporarily year_num < end_year replaced with True
        new_teams, objs = process_year_tba(year_num, teams, objs, False, True)
        teams += new_teams
        timer.print(str(year_num) + " TBA")

        year_obj = process_year_avg(objs[0], list(objs[5].values()))
        timer.print(str(year_num) + " AVG")

        objs = (year_obj, *objs[1:])

        # objs, team_years_dict = process_year_epa(year_num, team_years_dict, objs)
        # timer.print(str(year_num) + " EPA")

        update_teams_db(teams, False)
        write_objs_db(year_num, objs, None, True)
        timer.print(str(year_num) + " Write")

    post_process_tba()
    timer.print("Post TBA")

    post_process_epa(end_year)
    timer.print("Post EPA")


def update_single_year(year: int, partial: bool):
    timer = Timer()

    teams = get_teams_db()
    timer.print("Load Teams")

    if partial:
        event_objs = get_events_db(year=year, offseason=None)
        etags = get_etags_db(year)
        is_new_data = check_year_partial_tba(year, event_objs, etags)
        timer.print("Check TBA")

        if not is_new_data:
            return

    if partial:
        objs: objs_type = read_objs_db(year)
        timer.print("Read Objs")
    else:
        objs = create_objs(year)

    orig_objs = (
        objs[0],
        {**objs[1]},
        {**objs[2]},
        {**objs[3]},
        {**objs[4]},
        {**objs[5]},
        {**objs[6]},
        {**objs[7]},
    )

    new_teams, objs = process_year_tba(year, teams, objs, partial, False)
    teams += new_teams
    timer.print(str(year) + " TBA")

    year_obj = process_year_avg(objs[0], list(objs[5].values()))
    timer.print(str(year) + " AVG")

    objs = (year_obj, *objs[1:])

    team_years_dict = get_team_years_dict(year)
    objs, team_years_dict = process_year_epa(year, team_years_dict, objs)
    timer.print(str(year) + " EPA")

    if not partial:
        update_teams_db(teams, False)
    # Set clean=False to prevent deleting data without a backup
    write_objs_db(year, objs, orig_objs if partial else None, False)
    timer.print(str(year) + " Write")

    if not partial and year == CURR_YEAR:
        post_process_tba()
        timer.print("Post TBA")

        post_process_epa(year)
        timer.print("Post EPA")
