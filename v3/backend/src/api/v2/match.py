from typing import Any, Dict, Optional, List

from fastapi import APIRouter, Response

from src.models.epa.math import inv_unit_sigmoid
from src.api.v2.utils import format_team
from src.db.models import Alliance, Match
from src.api.match import get_match_cached, get_matches_cached
from src.api.alliance import get_alliances_cached
from src.utils.decorators import (
    async_fail_gracefully_singular,
    async_fail_gracefully_plural,
)

router = APIRouter()


def get_v2_match(
    match: Match, red_alliance: Alliance, blue_alliance: Alliance
) -> Dict[str, Any]:
    # TODO: epa_{red,blue}_{auto,teleop,endgame}_score_pred
    return {
        "key": match.key,
        "year": match.year,
        "event": match.event,
        "comp_level": match.comp_level,
        "set_number": match.set_number,
        "match_number": match.match_number,
        "offseason": match.offseason,
        "status": match.status,
        "video": match.video,
        "red_1": format_team(match.red_1),
        "red_2": format_team(match.red_2),
        "red_3": None if match.red_3 is None else format_team(match.red_3),
        "red_dq": match.red_dq,
        "red_surrogate": match.red_surrogate,
        "red_epa_sum": match.epa_red_score_pred,
        "red_auto_epa_sum": None,
        "red_teleop_epa_sum": None,
        "red_endgame_epa_sum": None,
        "red_rp_1_epa_sum": None
        if match.epa_red_rp_1_pred is None
        else round(inv_unit_sigmoid(match.epa_red_rp_1_pred), 4),
        "red_rp_2_epa_sum": None
        if match.epa_red_rp_2_pred is None
        else round(inv_unit_sigmoid(match.epa_red_rp_2_pred), 4),
        "blue_1": format_team(match.blue_1),
        "blue_2": format_team(match.blue_2),
        "blue_3": None if match.blue_3 is None else format_team(match.blue_3),
        "blue_dq": match.blue_dq,
        "blue_surrogate": match.blue_surrogate,
        "blue_epa_sum": match.epa_blue_score_pred,
        "blue_auto_epa_sum": None,
        "blue_teleop_epa_sum": None,
        "blue_endgame_epa_sum": None,
        "blue_rp_1_epa_sum": None
        if match.epa_blue_rp_1_pred is None
        else round(inv_unit_sigmoid(match.epa_blue_rp_1_pred), 4),
        "blue_rp_2_epa_sum": None
        if match.epa_blue_rp_2_pred is None
        else round(inv_unit_sigmoid(match.epa_blue_rp_2_pred), 4),
        "winner": match.winner,
        "epa_winner": match.epa_winner,
        "epa_win_prob": match.epa_win_prob,
        "red_rp_1_prob": match.epa_red_rp_1_pred,
        "red_rp_2_prob": match.epa_red_rp_2_pred,
        "blue_rp_1_prob": match.epa_blue_rp_1_pred,
        "blue_rp_2_prob": match.epa_blue_rp_2_pred,
        "playoff": match.elim,
        "time": match.time,
        "predicted_time": match.predicted_time,
        "red_score": match.red_score,
        "blue_score": match.blue_score,
        "red_auto": red_alliance.auto,
        "red_auto_movement": 0,
        "red_teleop": red_alliance.teleop,
        "red_endgame": red_alliance.endgame,
        "red_no_fouls": red_alliance.no_foul,
        "red_fouls": red_alliance.foul,
        "red_rp_1": None if red_alliance.rp_1 is None else int(red_alliance.rp_1),
        "red_rp_2": None if red_alliance.rp_2 is None else int(red_alliance.rp_2),
        "red_tiebreaker": red_alliance.tiebreaker,
        "blue_auto": blue_alliance.auto,
        "blue_auto_movement": 0,
        "blue_teleop": blue_alliance.teleop,
        "blue_endgame": blue_alliance.endgame,
        "blue_no_fouls": blue_alliance.no_foul,
        "blue_fouls": blue_alliance.foul,
        "blue_rp_1": None if blue_alliance.rp_1 is None else int(blue_alliance.rp_1),
        "blue_rp_2": None if blue_alliance.rp_2 is None else int(blue_alliance.rp_2),
        "blue_tiebreaker": blue_alliance.tiebreaker,
    }


async def get_matches_cached_wrapper(
    team: Optional[int] = None,
    year: Optional[int] = None,
    event: Optional[str] = None,
    week: Optional[int] = None,
    elims: Optional[bool] = None,
    offseason: Optional[bool] = False,
    metric: Optional[str] = None,
    ascending: Optional[bool] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> List[Dict[str, Any]]:
    if team is not None:
        raise Exception("Team filter not supported")

    matches: List[Match] = await get_matches_cached(
        year=year,
        event=event,
        week=week,
        elim=elims,
        offseason=offseason,
        metric=metric,
        ascending=ascending,
        limit=limit,
        offset=offset,
    )
    alliances: List[Alliance] = await get_alliances_cached(
        year=year,
        event=event,
        week=week,
        elim=elims,
        offseason=offseason,
        metric=metric,
        ascending=ascending,
        limit=limit,
        offset=offset,
    )
    match_to_red_alliance: Dict[str, Alliance] = {}
    match_to_blue_alliance: Dict[str, Alliance] = {}
    for alliance in alliances:
        if alliance.alliance == "red":
            match_to_red_alliance[alliance.match] = alliance
        elif alliance.alliance == "blue":
            match_to_blue_alliance[alliance.match] = alliance
    out_matches: List[Dict[str, Any]] = []
    for match in matches:
        red_alliance = match_to_red_alliance.get(match.key)
        blue_alliance = match_to_blue_alliance.get(match.key)
        if red_alliance is None or blue_alliance is None:
            raise Exception("Alliance not found")
        out_match = get_v2_match(match, red_alliance, blue_alliance)
        out_matches.append(out_match)
    return out_matches


@router.get("/")
async def read_v2_match_root():
    return {"name": "Match Router"}


@router.get(
    "/match/{match}",
    description="Get a single Match object containing teams, score prediction, and actual results. Specify match key ex: 2019ncwak_f1m1",
    response_description="A Match object.",
)
@async_fail_gracefully_singular
async def read_match(response: Response, match: str) -> Dict[str, Any]:
    match_obj: Optional[Match] = await get_match_cached(match=match)
    alliance_objs: List[Alliance] = await get_alliances_cached(match=match)
    red_alliances = [x for x in alliance_objs if x.alliance == "red"]
    if len(red_alliances) != 1:
        raise Exception("Red alliance not found")
    red_alliance = red_alliances[0]
    blue_alliances = [x for x in alliance_objs if x.alliance == "blue"]
    if len(blue_alliances) != 1:
        raise Exception("Blue alliance not found")
    blue_alliance = blue_alliances[0]
    if match_obj is None:
        raise Exception("Match not found")

    return get_v2_match(match_obj, red_alliance, blue_alliance)


@router.get(
    "/matches/event/{event}",
    description="Get a list of Match objects for a single event. Specify event key ex: 2019ncwak, 2022cmptx",
    response_description="A list of Match objects. See /match/{match} for more information.",
)
@async_fail_gracefully_plural
async def read_matches_event(response: Response, event: str) -> List[Dict[str, Any]]:
    return await get_matches_cached_wrapper(event=event)


@router.get(
    "/matches/team/{team}/year/{year}",
    description="Get a list of Match objects for a single team in a single year. Specify team number and year, ex: 254, 2019",
    response_description="A list of Match objects. See /match/{match} for more information.",
)
@async_fail_gracefully_plural
async def read_matches_team_year(
    response: Response, team: int, year: int
) -> List[Dict[str, Any]]:
    return await get_matches_cached_wrapper(team=team, year=year)


@router.get(
    "/matches/team/{team}/event/{event}",
    description="Get a list of Match objects for a single team in a single event. Specify team number and event key, ex: 5511, 2019ncwak",
    response_description="A list of Match objects. See /match/{match} for more information.",
)
@async_fail_gracefully_plural
async def read_matches_team_event(
    response: Response, team: int, event: str
) -> List[Dict[str, Any]]:
    return await get_matches_cached_wrapper(team=team, event=event)


@router.get(
    "/matches",
    description="Get a list of Matches with optional filters",
    response_description="A list of Match objects. See /match/{match} for more information.",
)
@async_fail_gracefully_plural
async def read_matches(
    response: Response,
    team: Optional[int] = None,
    year: Optional[int] = None,
    event: Optional[str] = None,
    week: Optional[int] = None,
    elims: Optional[bool] = None,
    offseason: Optional[bool] = False,
    metric: Optional[str] = None,
    ascending: Optional[bool] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> List[Dict[str, Any]]:
    return await get_matches_cached_wrapper(
        team=team,
        year=year,
        event=event,
        week=week,
        elims=elims,
        offseason=offseason,
        metric=metric,
        ascending=ascending,
        limit=limit,
        offset=offset,
    )
