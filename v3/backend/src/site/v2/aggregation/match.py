from datetime import timedelta
from typing import List, Optional, Tuple

from src.api.v2.utils import format_team, inv_format_team
from src.db.models import Match
from src.db.read import get_match as _get_match, get_matches as _get_matches
from src.site.v2.models import APIMatch
from src.utils.alru_cache import alru_cache
from src.utils.utils import get_match_name


def unpack_match(match: Match) -> APIMatch:
    # TODO: take in red_alliance, blue_alliance for components
    return APIMatch(
        year=match.year,
        event=match.event,
        time=match.time or -1,
        predicted_time=match.predicted_time or -1,
        key=match.key,
        match_name=get_match_name(match.key),
        status=match.status,
        video=match.video,
        comp_level=match.comp_level,
        set_number=match.set_number,
        match_number=match.match_number,
        playoff=match.elim,
        red=[format_team(team) for team in match.get_red()],
        blue=[format_team(team) for team in match.get_blue()],
        red_surrogates=[format_team(team) for team in match.get_red_surrogates()],
        blue_surrogates=[format_team(team) for team in match.get_blue_surrogates()],
        red_dqs=[format_team(team) for team in match.get_red_dqs()],
        blue_dqs=[format_team(team) for team in match.get_blue_dqs()],
        red_score=match.red_score or 0,
        red_auto=0,
        red_teleop=0,
        red_endgame=0,
        red_1=0,
        red_2=0,
        red_fouls=0,
        red_rp_1=match.red_rp_1 or 0,
        red_rp_2=match.red_rp_2 or 0,
        red_tiebreaker=0,
        blue_score=match.blue_score or 0,
        blue_auto=0,
        blue_teleop=0,
        blue_endgame=0,
        blue_1=0,
        blue_2=0,
        blue_fouls=0,
        blue_rp_1=match.blue_rp_1 or 0,
        blue_rp_2=match.blue_rp_2 or 0,
        blue_tiebreaker=0,
        winner=match.winner or "",
        red_epa_pred=match.epa_red_score_pred or 0,
        red_auto_epa_pred=0,
        red_teleop_epa_pred=0,
        red_endgame_epa_pred=0,
        red_rp_1_pred=match.epa_red_rp_1_pred or 0,
        red_rp_2_pred=match.epa_red_rp_2_pred or 0,
        blue_epa_pred=match.epa_blue_score_pred or 0,
        blue_auto_epa_pred=0,
        blue_teleop_epa_pred=0,
        blue_endgame_epa_pred=0,
        blue_rp_1_pred=match.epa_blue_rp_1_pred or 0,
        blue_rp_2_pred=match.epa_blue_rp_2_pred or 0,
        epa_win_prob=match.epa_win_prob or 0,
        pred_winner=match.epa_winner or "",
    )


@alru_cache(ttl=timedelta(minutes=1))
async def get_match(
    match: str, no_cache: bool = False
) -> Tuple[bool, Optional[APIMatch]]:
    match_obj = _get_match(match=match)

    # If invalid, do not cache
    if match_obj is None:
        return (False, None)

    # If valid, cache
    return (True, unpack_match(match_obj))


@alru_cache(ttl=timedelta(minutes=1))
async def get_matches(
    team: Optional[int] = None,
    year: Optional[int] = None,
    event: Optional[str] = None,
    offseason: Optional[bool] = False,
    no_cache: bool = False,
) -> Tuple[bool, List[APIMatch]]:
    match_objs: List[Match] = _get_matches(
        team=None if team is None else inv_format_team(team),
        year=year,
        event=event,
        offseason=offseason,
    )
    matches = [unpack_match(match) for match in match_objs]
    return (True, sorted(matches, key=lambda x: x.time))
