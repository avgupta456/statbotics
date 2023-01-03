from datetime import timedelta
from typing import List, Optional

from src.api.models import APITeamMatch
from src.db.models import TeamMatch
from src.db.read import get_team_matches as _get_team_matches
from src.utils.alru_cache import alru_cache
from src.utils.utils import get_match_number


def unpack_team_match(team_match: TeamMatch) -> APITeamMatch:
    return APITeamMatch(
        num=team_match.team,
        alliance=team_match.alliance,
        match=team_match.match,
        time=team_match.time,
        playoff=team_match.playoff,
        match_number=get_match_number(team_match.match),
        total_epa=team_match.epa or 0,
        auto_epa=team_match.auto_epa or 0,
        teleop_epa=team_match.teleop_epa or 0,
        endgame_epa=team_match.endgame_epa or 0,
        rp_1_epa=team_match.rp_1_epa or 0,
        rp_2_epa=team_match.rp_2_epa or 0,
        offseason=team_match.offseason,
    )


@alru_cache(ttl=timedelta(minutes=5))
async def get_team_matches(
    year: Optional[int] = None,
    event: Optional[str] = None,
    team: Optional[int] = None,
    match: Optional[str] = None,
) -> List[APITeamMatch]:
    team_match_objs: List[TeamMatch] = _get_team_matches(
        team=team, year=year, event=event, match=match
    )

    team_matches = [unpack_team_match(x) for x in team_match_objs]
    return (True, sorted(team_matches, key=lambda x: x.time))  # type: ignore
