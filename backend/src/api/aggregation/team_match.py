from typing import Callable, List, Optional
from datetime import timedelta

from src.api.models.team_match import APITeamMatch
from src.data.nepa import get_epa_to_norm_epa_func
from src.db.models.team_match import TeamMatch
from src.db.read.team_match import get_team_matches as _get_team_matches
from src.utils.utils import get_match_number
from src.utils.alru_cache import alru_cache


def unpack_team_match(
    epa_to_norm_epa: Callable[[float], float], team_match: TeamMatch
) -> APITeamMatch:
    return APITeamMatch(
        match=get_match_number(team_match.match),
        label=team_match.match,
        time=team_match.time,
        playoff=team_match.playoff,
        norm_epa=epa_to_norm_epa(team_match.epa or 0),
        total_epa=team_match.epa or 0,
        auto_epa=team_match.auto_epa or 0,
        teleop_epa=team_match.teleop_epa or 0,
        endgame_epa=team_match.endgame_epa or 0,
        rp_1_epa=team_match.rp_1_epa or 0,
        rp_2_epa=team_match.rp_2_epa or 0,
    )


@alru_cache(ttl=timedelta(minutes=5))
async def get_team_matches(
    year: Optional[int] = None,
    event: Optional[str] = None,
    team: Optional[int] = None,
    match: Optional[str] = None,
    epa_to_norm_epa: Optional[Callable[[float], float]] = None,
) -> List[APITeamMatch]:
    team_match_objs: List[TeamMatch] = _get_team_matches(
        team=team, year=year, event=event, match=match
    )

    if epa_to_norm_epa is None:
        epa_to_norm_epa = get_epa_to_norm_epa_func(year)

    team_matches = [unpack_team_match(epa_to_norm_epa, x) for x in team_match_objs]
    return (True, sorted(team_matches, key=lambda x: x.time))  # type: ignore
