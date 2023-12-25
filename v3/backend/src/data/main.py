from collections import defaultdict
from typing import Dict, List, Optional

from src.constants import CURR_YEAR
from src.data.avg import process_year as process_year_avg
from src.data.epa.main import (
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
    create_objs,
    objs_type,
    read_objs as read_objs_db,
    write_objs as write_objs_db,
)
from src.data.wins import (
    post_process as post_process_wins,
    process_year as process_year_wins,
)
from src.db.main import clean_db
from src.db.models import Team, TeamYear
from src.db.read import (
    get_etags as get_etags_db,
    get_events as get_events_db,
    get_team_years as get_team_years_db,
    get_teams as get_teams_db,
)
from src.db.write.main import update_teams as update_teams_db


def process_year(
    year_num: int,
    partial: bool,
    cache: bool,
    teams: List[Team],
    objs: objs_type,
    all_team_years: Optional[Dict[int, Dict[str, TeamYear]]],
) -> List[Team]:
    timer = Timer()

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

    if all_team_years is None:
        all_team_years = defaultdict(dict)
        for year in range(max(2002, year_num - 4), year_num):
            team_years = get_team_years_db(year=year)
            for ty in team_years:
                all_team_years[ty.year][ty.team] = ty

    # TODO: temporarily year_num < end_year replaced with True
    new_teams, objs = process_year_tba(year_num, teams, objs, partial, cache)
    teams += new_teams
    timer.print(str(year_num) + " TBA")

    year_obj = process_year_avg(objs[0], list(objs[5].values()))
    timer.print(str(year_num) + " AVG")

    objs = (year_obj, *objs[1:])

    objs = process_year_wins(objs)
    timer.print(str(year_num) + " Wins")

    objs = process_year_epa(objs, all_team_years)
    timer.print(str(year_num) + " EPA")

    write_objs_db(year_num, objs, orig_objs if partial else None, True)
    timer.print(str(year_num) + " Write")

    return teams


def post_process(
    teams: List[Team],
    all_team_years: Optional[Dict[int, Dict[str, TeamYear]]],
):
    timer = Timer()

    if all_team_years is None:
        all_team_years = defaultdict(dict)
        all_team_years_list = get_team_years_db()
        for ty in all_team_years_list:
            all_team_years[ty.year][ty.team] = ty

    teams = post_process_wins(teams, all_team_years)
    timer.print("Post Wins")

    teams = post_process_epa(teams, all_team_years)
    timer.print("Post EPA")

    update_teams_db(teams, True)
    timer.print("Update DB")

    post_process_tba()  # updates DB directly
    timer.print("Post TBA")


def reset_all_years():
    timer = Timer()

    start_year = 2002  # 2002
    end_year = 2006  # CURR_YEAR

    clean_db()
    timer.print("Clean DB")

    teams = load_teams_tba(cache=True)
    timer.print("Load Teams")

    all_team_years: Dict[int, Dict[str, TeamYear]] = {}
    for year_num in range(start_year, end_year + 1):
        objs = create_objs(year_num)
        teams = process_year(year_num, False, True, teams, objs, all_team_years)
        all_team_years[year_num] = {ty.team: ty for ty in objs[1].values()}

    post_process(teams, all_team_years)


def update_curr_year(partial: bool):
    year = CURR_YEAR
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

    teams = process_year(year, partial, False, teams, objs, None)

    if not partial:
        # triggers loading all team years
        post_process(teams, None)
