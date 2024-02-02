from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Response

from src.api.match import get_match_cached, get_matches_cached
from src.api.v2.utils import format_team
from src.db.models import Match
from src.models.epa.math import inv_unit_sigmoid
from src.utils.decorators import (
    async_fail_gracefully_plural,
    async_fail_gracefully_singular,
)

router = APIRouter()


def get_v2_match(match: Match) -> Dict[str, Any]:
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
        "red_auto": match.red_auto,
        "red_auto_movement": 0,
        "red_teleop": match.red_teleop,
        "red_endgame": match.red_endgame,
        "red_no_fouls": match.red_no_foul,
        "red_fouls": match.red_foul,
        "red_rp_1": None if match.red_rp_1 is None else int(match.red_rp_1),
        "red_rp_2": None if match.red_rp_2 is None else int(match.red_rp_2),
        "red_tiebreaker": match.red_tiebreaker,
        "blue_auto": match.blue_auto,
        "blue_auto_movement": 0,
        "blue_teleop": match.blue_teleop,
        "blue_endgame": match.blue_endgame,
        "blue_no_fouls": match.blue_no_foul,
        "blue_fouls": match.blue_foul,
        "blue_rp_1": None if match.blue_rp_1 is None else int(match.blue_rp_1),
        "blue_rp_2": None if match.blue_rp_2 is None else int(match.blue_rp_2),
        "blue_tiebreaker": match.blue_tiebreaker,
    }


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
    if match_obj is None:
        raise Exception("Match not found")
    return get_v2_match(match_obj)


@router.get(
    "/matches/event/{event}",
    description="Get a list of Match objects for a single event. Specify event key ex: 2019ncwak, 2022cmptx",
    response_description="A list of Match objects. See /match/{match} for more information.",
)
@async_fail_gracefully_plural
async def read_matches_event(response: Response, event: str) -> List[Dict[str, Any]]:
    matches = await get_matches_cached(event=event)
    return [get_v2_match(match) for match in matches]


@router.get(
    "/matches/team/{team}/year/{year}",
    description="Get a list of Match objects for a single team in a single year. Specify team number and year, ex: 254, 2019",
    response_description="A list of Match objects. See /match/{match} for more information.",
)
@async_fail_gracefully_plural
async def read_matches_team_year(
    response: Response, team: int, year: int
) -> List[Dict[str, Any]]:
    matches = await get_matches_cached(team=str(team), year=year)
    return [get_v2_match(match) for match in matches]


@router.get(
    "/matches/team/{team}/event/{event}",
    description="Get a list of Match objects for a single team in a single event. Specify team number and event key, ex: 5511, 2019ncwak",
    response_description="A list of Match objects. See /match/{match} for more information.",
)
@async_fail_gracefully_plural
async def read_matches_team_event(
    response: Response, team: int, event: str
) -> List[Dict[str, Any]]:
    matches = await get_matches_cached(team=str(team), event=event)
    return [get_v2_match(match) for match in matches]


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
    matches = await get_matches_cached(
        team=None if team is None else str(team),
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

    return [get_v2_match(match) for match in matches]
