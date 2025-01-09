from collections import defaultdict
from typing import Dict, List

from src.constants import CURR_YEAR
from src.data.epa.agg import process_year as process_year_agg
from src.data.epa.calc import process_year as process_year_calc
from src.data.epa.metrics import process_year as process_year_metrics
from src.data.utils import objs_type
from src.db.models import Team, TeamYear
from src.utils.utils import r


# MAIN FUNCTION
def process_year(
    objs: objs_type, all_team_years: Dict[int, Dict[int, TeamYear]]
) -> objs_type:
    objs = process_year_calc(objs, all_team_years)
    objs = process_year_agg(objs)
    objs = process_year_metrics(objs)

    return objs


def post_process(
    teams: List[Team], all_team_years: Dict[int, Dict[int, TeamYear]]
) -> List[Team]:
    team_team_years: Dict[int, List[TeamYear]] = defaultdict(list)
    for team_years in all_team_years.values():
        for team_year in team_years.values():
            team_team_years[team_year.team].append(team_year)

    for team in teams:
        years: Dict[int, float] = {}

        for team_year in team_team_years[team.team]:
            if team_year.norm_epa is not None:
                years[team_year.year] = team_year.norm_epa

        keys, values = years.keys(), years.values()

        # get recent epas (last four years)
        recent: List[float] = []
        for year in range(CURR_YEAR - 4, CURR_YEAR + 1):
            if year in keys:
                recent.append(years[year])
        r_y, y = len(recent), len(keys)

        team.norm_epa = None if y == 0 else r(years[max(keys)])
        team.norm_epa_recent = None if r_y == 0 else r(sum(recent) / r_y)
        team.norm_epa_mean = None if y == 0 else r(sum(values) / y)
        team.norm_epa_max = None if y == 0 else r(max(values))

    return teams
