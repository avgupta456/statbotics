from collections import defaultdict
from copy import deepcopy
from typing import Dict, List, Optional, Tuple

from src.constants import CURR_YEAR
from src.data.avg import process_year as process_year_avg
from src.data.epa.main import (
    post_process as post_process_epa,
    process_year as process_year_epa,
)
from src.data.tba import (
    load_teams as load_teams_tba,
    post_process as post_process_tba,
    process_year as process_year_tba,
)
from src.tba.clean_data import clean_district
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
    winrate,
)
from src.db.main import clean_db
from src.db.models import Team, TeamYear
from src.db.read import (
    get_num_years,
    get_team_events as get_team_events_db,
    get_team_years as get_team_years_db,
    get_teams as get_teams_db,
)
from src.db.write.main import (
    update_team_events as update_team_events_db,
    update_team_years as update_team_years_db,
    update_teams as update_teams_db,
)
from src.google.storage import write_objs as write_objs_storage


def process_year(
    year_num: int,
    partial: bool,
    tba_partial: bool,
    cache: bool,
    teams: List[Team],
    objs: objs_type,
    all_team_years: Optional[Dict[int, Dict[int, TeamYear]]],
) -> List[Team]:
    timer = Timer()
    orig_objs = deepcopy(objs)
    if all_team_years is None:
        all_team_years = defaultdict(dict)
        for year in range(max(2002, year_num - 4), year_num):
            team_years = get_team_years_db(year=year)
            for ty in team_years:
                all_team_years[ty.year][ty.team] = ty

    new_teams, objs = process_year_tba(year_num, teams, objs, tba_partial, cache)
    teams += new_teams
    timer.print(str(year_num) + " TBA")

    year_obj = process_year_avg(objs[0], list(objs[4].values()))
    timer.print(str(year_num) + " AVG")

    objs = (year_obj, *objs[1:])

    objs = process_year_wins(objs)
    timer.print(str(year_num) + " Wins")

    objs = process_year_epa(objs, all_team_years)
    timer.print(str(year_num) + " EPA")

    write_objs_db(year_num, objs, orig_objs if partial else None, not partial)
    timer.print(str(year_num) + " Write DB")

    if year_num == CURR_YEAR:
        write_objs_storage(objs, orig_objs if partial else None)
        timer.print(str(year_num) + " Write Storage")

    return teams


def post_process(
    teams: List[Team], all_team_years: Optional[Dict[int, Dict[int, TeamYear]]]
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

    update_teams_db(teams)
    timer.print("Update DB")

    post_process_tba()  # updates DB directly
    timer.print("Post TBA")


def reset_all_years():
    timer = Timer()

    start_year = 2002
    end_year = CURR_YEAR

    try:
        if get_num_years() > 0:
            return
    except Exception:
        pass

    clean_db()
    timer.print("Clean DB")

    teams = load_teams_tba(cache=False)
    timer.print("Load Teams")

    all_team_years: Dict[int, Dict[int, TeamYear]] = {}
    for year_num in range(start_year, end_year + 1):
        objs = create_objs(year_num)
        if year_num == 2021:
            continue

        teams = process_year(year_num, False, False, True, teams, objs, all_team_years)
        all_team_years[year_num] = {ty.team: ty for ty in objs[1].values()}

    post_process(teams, all_team_years)


def update_curr_year(partial: bool, tba_partial: bool):
    year = CURR_YEAR
    timer = Timer()

    teams = get_teams_db()
    timer.print("Load Teams")

    if partial:
        objs: objs_type = read_objs_db(year)
        timer.print("Read Objs")
    else:
        objs = create_objs(year)
        timer.print("Create Objs")

    teams = process_year(
        year, partial, tba_partial, year < CURR_YEAR, teams, objs, None
    )

    if not partial:
        # triggers loading all team years
        post_process(teams, None)


def refresh_teams() -> Dict[str, int]:
    """Refresh all stale team fields from TBA and recompute win records."""
    timer = Timer()

    fresh_teams = load_teams_tba(cache=False)
    fresh_team_map: Dict[int, Team] = {t.team: t for t in fresh_teams}
    timer.print("Fetch TBA Teams")

    db_teams = get_teams_db()
    all_team_years_list = get_team_years_db()
    timer.print("Fetch DB Teams + TeamYears")

    # Compute true last_active_year per team
    true_last: Dict[int, int] = {}
    for ty in all_team_years_list:
        if ty.team not in true_last or ty.year > true_last[ty.team]:
            true_last[ty.team] = ty.year

    # Compute aggregate win record per team from TeamYear data
    t_record: Dict[int, Tuple[int, int, int, int]] = defaultdict(lambda: (0, 0, 0, 0))
    for ty in all_team_years_list:
        t_record[ty.team] = (
            t_record[ty.team][0] + ty.wins,
            t_record[ty.team][1] + ty.losses,
            t_record[ty.team][2] + ty.ties,
            t_record[ty.team][3] + ty.count,
        )

    # Find teams with any stale fields
    teams_to_update: Dict[int, Team] = {}
    for t in db_teams:
        dirty = False
        fresh = fresh_team_map.get(t.team)

        if fresh is not None:
            for field in ("name", "country", "state", "rookie_year"):
                fresh_val = getattr(fresh, field)
                if fresh_val is not None and getattr(t, field) != fresh_val:
                    setattr(t, field, fresh_val)
                    dirty = True

        cleaned = clean_district(t.district)
        if cleaned != t.district:
            t.district = cleaned
            dirty = True

        if true_last.get(t.team) != t.last_active_year:
            t.last_active_year = true_last.get(t.team)
            dirty = True

        rec = t_record[t.team]
        if (t.wins, t.losses, t.ties, t.count) != rec:
            t.wins, t.losses, t.ties, t.count = rec
            t.winrate = winrate(t.wins, t.ties, t.count)
            dirty = True

        if dirty:
            teams_to_update[t.team] = t

    if teams_to_update:
        update_teams_db(list(teams_to_update.values()))
    timer.print(f"Update Teams ({len(teams_to_update)} rows)")

    # Propagate team fields to TeamYear and TeamEvent for all updated teams
    if teams_to_update:
        changed_team_years = [
            ty for ty in all_team_years_list if ty.team in teams_to_update
        ]
        for ty in changed_team_years:
            src = teams_to_update[ty.team]
            ty.name = src.name
            ty.country = src.country
            ty.state = src.state
            ty.district = clean_district(ty.district)
        update_team_years_db(changed_team_years)
        timer.print(f"Update TeamYears ({len(changed_team_years)} rows)")

        all_team_events = get_team_events_db(teams=[str(t) for t in teams_to_update])
        for te in all_team_events:
            te.team_name = teams_to_update[te.team].name
        update_team_events_db(all_team_events)
        timer.print(f"Update TeamEvents ({len(all_team_events)} rows)")

    return {"teams_updated": len(teams_to_update)}
