from collections import defaultdict
from typing import Callable, Dict, List, Optional

from src.db.models import TeamMatch
from src.data.utils import objs_type
from src.utils.utils import get_team_event_key


def process_arr(
    tms: List[TeamMatch], acc: Callable[[TeamMatch], Optional[float]], default: float
):
    _arr = [acc(tm) for tm in tms if not tm.offseason]
    arr = [x for x in _arr if x is not None]
    _pre_champs_arr = [acc(tm) for tm in tms if acc(tm) if tm.week < 8]
    pre_champs_arr = [x for x in _pre_champs_arr if x is not None]
    pre_champs = pre_champs_arr[-1] if len(pre_champs_arr) > 0 else default
    end = arr[-1] if len(arr) > 0 else default
    max_ = max(arr[8:]) if len(arr) > 8 else end
    return pre_champs, end, max_


def process_year(objs: objs_type) -> objs_type:
    year_num = objs[0].year
    USE_COMPONENTS = year_num >= 2016

    team_team_matches_dict: Dict[str, List[TeamMatch]] = defaultdict(list)
    team_event_team_matches_dict: Dict[str, List[TeamMatch]] = defaultdict(list)

    for team_match in objs[6].values():
        team_team_matches_dict[team_match.team].append(team_match)
        team_event_key = get_team_event_key(team_match.team, team_match.event)
        team_event_team_matches_dict[team_event_key].append(team_match)

    # TEAM YEARS
    for ty in objs[1].values():
        ms = team_team_matches_dict[ty.team]

        ty.epa_start, ty.epa_end, ty.epa_max = process_arr(
            ms, lambda m: m.epa, ty.epa_start
        )

        if USE_COMPONENTS:
            ty.rp_1_epa_start, ty.rp_1_epa_end, ty.rp_1_epa_max = process_arr(
                ms, lambda m: m.rp_1_epa, ty.rp_1_epa_start or 0
            )
            ty.rp_2_epa_start, ty.rp_2_epa_end, ty.rp_2_epa_max = process_arr(
                ms, lambda m: m.rp_2_epa, ty.rp_2_epa_start or 0
            )

    return objs
