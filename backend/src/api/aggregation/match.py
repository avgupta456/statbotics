from datetime import timedelta
from typing import List, Optional

from src.api.models.match import APIMatch
from src.db.models.match import Match
from src.db.read.match import get_match as _get_match, get_matches as _get_matches
from src.utils.alru_cache import alru_cache
from src.utils.utils import get_match_name


def unpack_match(match: Match) -> APIMatch:
    return APIMatch(
        year=match.year,
        event=match.event,
        time=match.time or -1,
        key=match.key,
        match_name=get_match_name(match.key),
        video=match.video,
        comp_level=match.comp_level,
        set_number=match.set_number,
        match_number=match.match_number,
        playoff=match.playoff,
        red=match.get_red(),
        blue=match.get_blue(),
        red_score=match.red_score or 0,
        red_auto=match.red_auto or 0,
        red_teleop=match.red_teleop or 0,
        red_endgame=match.red_endgame or 0,
        red_1=(match.red_auto_1 or 0) + (match.red_teleop_1 or 0),
        red_2=(match.red_auto_2 or 0) + (match.red_teleop_2 or 0),
        red_fouls=match.red_fouls or 0,
        red_rp_1=match.red_rp_1 or 0,
        red_rp_2=match.red_rp_2 or 0,
        blue_score=match.blue_score or 0,
        blue_auto=match.blue_auto or 0,
        blue_teleop=match.blue_teleop or 0,
        blue_endgame=match.blue_endgame or 0,
        blue_1=(match.blue_auto_1 or 0) + (match.blue_teleop_1 or 0),
        blue_2=(match.blue_auto_2 or 0) + (match.blue_teleop_2 or 0),
        blue_fouls=match.blue_fouls or 0,
        blue_rp_1=match.blue_rp_1 or 0,
        blue_rp_2=match.blue_rp_2 or 0,
        winner=match.winner or "",
        red_epa_pred=match.red_epa_sum or 0,
        red_auto_epa_pred=match.red_auto_epa_sum or 0,
        red_teleop_epa_pred=match.red_teleop_epa_sum or 0,
        red_endgame_epa_pred=match.red_endgame_epa_sum or 0,
        red_rp_1_pred=match.red_rp_1_epa_sum or 0,
        red_rp_2_pred=match.red_rp_2_epa_sum or 0,
        blue_epa_pred=match.blue_epa_sum or 0,
        blue_auto_epa_pred=match.blue_auto_epa_sum or 0,
        blue_teleop_epa_pred=match.blue_teleop_epa_sum or 0,
        blue_endgame_epa_pred=match.blue_endgame_epa_sum or 0,
        blue_rp_1_pred=match.blue_rp_1_epa_sum or 0,
        blue_rp_2_pred=match.blue_rp_2_epa_sum or 0,
        epa_win_prob=match.epa_win_prob or 0,
        pred_winner=match.epa_winner or "",
    )


@alru_cache(ttl=timedelta(minutes=5))
async def get_match(match: str, no_cache: bool = False) -> Optional[APIMatch]:
    match_obj = _get_match(match=match)

    # If invalid, do not cache
    if match_obj is None:
        return (False, None)  # type: ignore

    # If valid, cache
    return (True, unpack_match(match_obj))  # type: ignore


@alru_cache(ttl=timedelta(minutes=5))
async def get_matches(
    team: Optional[int] = None,
    year: Optional[int] = None,
    event: Optional[str] = None,
    no_cache: bool = False,
) -> List[APIMatch]:
    matches: List[Match] = _get_matches(team=team, year=year, event=event)
    return (True, [unpack_match(match) for match in matches])  # type: ignore
