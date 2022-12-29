from typing import Any, Dict, List

from src.data.nepa import get_epa_to_norm_epa_func
from src.db.models.team_match import TeamMatch
from src.db.read.team_match import get_team_matches as _get_team_matches
from src.utils.utils import get_match_number


async def get_team_matches(team: int, year: int) -> List[Dict[str, Any]]:
    team_match_objs: List[TeamMatch] = _get_team_matches(year=year, team=team)

    epa_to_norm_epa = get_epa_to_norm_epa_func(year)

    team_matches = [
        {
            "match": get_match_number(x.match),
            "label": x.match,
            "time": x.time,
            "playoff": x.playoff,
            "norm_epa": epa_to_norm_epa(x.epa or 0),
            "total_epa": x.epa,
            "auto_epa": x.auto_epa,
            "teleop_epa": x.teleop_epa,
            "endgame_epa": x.endgame_epa,
            "rp_1_epa": x.rp_1_epa,
            "rp_2_epa": x.rp_2_epa,
        }
        for x in team_match_objs
    ]

    team_matches.sort(key=lambda x: x["time"] or -1)

    return team_matches
