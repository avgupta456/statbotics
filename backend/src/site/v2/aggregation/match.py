from datetime import timedelta
from typing import Dict, List, Optional, Tuple

from src.api.v2.utils import format_team, inv_format_team
from src.db.functions.noteworthy_matches import (
    get_noteworthy_matches as _get_noteworthy_matches,
)
from src.db.functions.upcoming_matches import (
    get_upcoming_matches as _get_upcoming_matches,
)
from src.db.models import Match
from src.db.read import get_match as _get_match, get_matches as _get_matches
from src.site.v2.models import APIMatch
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
        playoff=match.elim,
        red=[format_team(team) for team in match.get_red()],
        blue=[format_team(team) for team in match.get_blue()],
        red_surrogates=[format_team(team) for team in match.get_red_surrogates()],
        blue_surrogates=[format_team(team) for team in match.get_blue_surrogates()],
        red_dqs=[format_team(team) for team in match.get_red_dqs()],
        blue_dqs=[format_team(team) for team in match.get_blue_dqs()],
        red_score=match.red_score or 0,
        red_auto=match.red_auto or 0,
        red_teleop=match.red_teleop or 0,
        red_endgame=match.red_endgame or 0,
        red_1=0,
        red_2=0,
        red_fouls=match.red_foul or 0,
        red_rp_1=match.red_rp_1 or 0,
        red_rp_2=match.red_rp_2 or 0,
        red_tiebreaker=match.red_tiebreaker or 0,
        blue_score=match.blue_score or 0,
        blue_auto=match.blue_auto or 0,
        blue_teleop=match.blue_teleop or 0,
        blue_endgame=match.blue_endgame or 0,
        blue_1=0,
        blue_2=0,
        blue_fouls=match.blue_foul or 0,
        blue_rp_1=match.blue_rp_1 or 0,
        blue_rp_2=match.blue_rp_2 or 0,
        blue_tiebreaker=match.blue_tiebreaker or 0,
        winner=match.winner or "",
        red_epa_pred=match.epa_red_score_pred or 0,
        red_auto_epa_pred=match.epa_red_auto_pred or 0,
        red_teleop_epa_pred=match.epa_red_teleop_pred or 0,
        red_endgame_epa_pred=match.epa_red_endgame_pred or 0,
        red_rp_1_pred=match.epa_red_rp_1_pred or 0,
        red_rp_2_pred=match.epa_red_rp_2_pred or 0,
        blue_epa_pred=match.epa_blue_score_pred or 0,
        blue_auto_epa_pred=match.epa_blue_auto_pred or 0,
        blue_teleop_epa_pred=match.epa_blue_teleop_pred or 0,
        blue_endgame_epa_pred=match.epa_blue_endgame_pred or 0,
        blue_rp_1_pred=match.epa_blue_rp_1_pred or 0,
        blue_rp_2_pred=match.epa_blue_rp_2_pred or 0,
        epa_win_prob=match.epa_win_prob or 0,
        pred_winner=match.epa_winner or "",
    )


@alru_cache(ttl=timedelta(minutes=2))
async def get_match(
    match: str, no_cache: bool = False
) -> Tuple[bool, Optional[APIMatch]]:
    match_obj = _get_match(match=match)

    # If invalid, do not cache
    if match_obj is None:
        return (False, None)

    # If valid, cache
    return (True, unpack_match(match_obj))


@alru_cache(ttl=timedelta(minutes=2))
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


@alru_cache(ttl=timedelta(minutes=5))
async def get_upcoming_matches(
    country: Optional[str],
    state: Optional[str],
    district: Optional[str],
    playoff: Optional[bool],
    minutes: int,
    limit: int,
    metric: str,
    no_cache: bool = False,
) -> Tuple[bool, List[Tuple[APIMatch, str]]]:
    match_objs: List[Tuple[Match, str]] = _get_upcoming_matches(
        country=country,
        state=state,
        district=district,
        elim=playoff,
        minutes=minutes,
        limit=limit,
        metric=metric,
    )

    matches = [(unpack_match(match), event_name) for (match, event_name) in match_objs]

    return (True, matches)


@alru_cache(ttl=timedelta(minutes=15))
async def get_noteworthy_matches(
    year: int,
    country: Optional[str],
    state: Optional[str],
    district: Optional[str],
    playoff: Optional[bool],
    week: Optional[int],
    no_cache: bool = False,
) -> Tuple[bool, Dict[str, List[APIMatch]]]:
    match_objs = _get_noteworthy_matches(
        year=year,
        country=country,
        state=state,
        district=district,
        elim=playoff,
        week=week,
    )

    matches = {k: [unpack_match(match) for match in v] for k, v in match_objs.items()}

    return (True, matches)
