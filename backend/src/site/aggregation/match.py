from datetime import timedelta
from typing import Dict, List, Optional, Tuple

from src.db.models import Match
from src.db.read import get_match as _get_match, get_matches as _get_matches
from src.db.functions.upcoming_matches import (
    get_upcoming_matches as _get_upcoming_matches,
)
from src.site.models import APIMatch
from src.utils.alru_cache import alru_cache
from src.utils.utils import get_match_name


def unpack_match(match: Match) -> APIMatch:
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
        playoff=match.playoff,
        red=match.get_red(),
        blue=match.get_blue(),
        red_surrogates=match.get_red_surrogates(),
        blue_surrogates=match.get_blue_surrogates(),
        red_dqs=match.get_red_dqs(),
        blue_dqs=match.get_blue_dqs(),
        red_score=match.red_score or 0,
        red_auto=match.red_auto or 0,
        red_teleop=match.red_teleop or 0,
        red_endgame=match.red_endgame or 0,
        red_1=(match.red_auto_1 or 0) + (match.red_teleop_1 or 0),
        red_2=(match.red_auto_2 or 0) + (match.red_teleop_2 or 0),
        red_fouls=match.red_fouls or 0,
        red_rp_1=match.red_rp_1 or 0,
        red_rp_2=match.red_rp_2 or 0,
        red_tiebreaker=match.red_tiebreaker or 0,
        blue_score=match.blue_score or 0,
        blue_auto=match.blue_auto or 0,
        blue_teleop=match.blue_teleop or 0,
        blue_endgame=match.blue_endgame or 0,
        blue_1=(match.blue_auto_1 or 0) + (match.blue_teleop_1 or 0),
        blue_2=(match.blue_auto_2 or 0) + (match.blue_teleop_2 or 0),
        blue_fouls=match.blue_fouls or 0,
        blue_rp_1=match.blue_rp_1 or 0,
        blue_rp_2=match.blue_rp_2 or 0,
        blue_tiebreaker=match.blue_tiebreaker or 0,
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


@alru_cache(ttl=timedelta(minutes=1))
async def get_match(match: str, no_cache: bool = False) -> Optional[APIMatch]:
    match_obj = _get_match(match=match)

    # If invalid, do not cache
    if match_obj is None:
        return (False, None)  # type: ignore

    # If valid, cache
    return (True, unpack_match(match_obj))  # type: ignore


@alru_cache(ttl=timedelta(minutes=1))
async def get_matches(
    team: Optional[int] = None,
    year: Optional[int] = None,
    event: Optional[str] = None,
    no_cache: bool = False,
) -> List[APIMatch]:
    match_objs: List[Match] = _get_matches(team=team, year=year, event=event)
    matches = [unpack_match(match) for match in match_objs]
    return (True, sorted(matches, key=lambda x: x.time))  # type: ignore


@alru_cache(ttl=timedelta(minutes=1))
async def get_upcoming_matches(
    no_cache: bool = False,
) -> List[Tuple[Match, str, Dict[int, float]]]:
    match_objs: List[Tuple[Match, str, Dict[int, float]]] = _get_upcoming_matches()
    matches = [
        (unpack_match(match), event_name, team_matches)
        for (match, event_name, team_matches) in match_objs
    ]

    return (True, sorted(matches, key=lambda x: x[0].time))  # type: ignore
