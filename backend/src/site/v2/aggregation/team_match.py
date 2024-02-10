from datetime import timedelta
from typing import List, Optional, Tuple

from src.api.v2.utils import format_team, inv_format_team
from src.db.models import TeamMatch
from src.db.read import get_team_matches as _get_team_matches
from src.site.v2.models import APITeamMatch
from src.utils.alru_cache import alru_cache
from src.utils.utils import get_match_number


def unpack_team_match(team_match: TeamMatch) -> APITeamMatch:
    return APITeamMatch(
        num=format_team(team_match.team),
        alliance=team_match.alliance,
        match=team_match.match,
        time=team_match.time,
        playoff=team_match.elim,
        match_number=get_match_number(team_match.match),
        total_epa=team_match.epa or 0,
        auto_epa=team_match.auto_epa or 0,
        teleop_epa=team_match.teleop_epa or 0,
        endgame_epa=team_match.endgame_epa or 0,
        rp_1_epa=team_match.rp_1_epa or 0,
        rp_2_epa=team_match.rp_2_epa or 0,
        post_epa=team_match.post_epa,
        offseason=team_match.offseason,
        status=team_match.status,
    )


@alru_cache(ttl=timedelta(minutes=1))
async def get_team_matches(
    year: Optional[int] = None,
    event: Optional[str] = None,
    team: Optional[int] = None,
    match: Optional[str] = None,
    offseason: Optional[bool] = False,
    no_cache: bool = False,
) -> Tuple[bool, List[APITeamMatch]]:
    team_match_objs: List[TeamMatch] = _get_team_matches(
        team=None if team is None else inv_format_team(team),
        year=year,
        event=event,
        match=match,
        offseason=offseason,
    )

    team_matches = [unpack_team_match(x) for x in team_match_objs]
    return (True, sorted(team_matches, key=lambda x: x.time or 0))
