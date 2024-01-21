from fastapi import APIRouter, Response

from typing import Any, Dict, List, Optional
from src.db.models import TeamMatch
from src.utils.decorators import (
    async_fail_gracefully_plural,
    async_fail_gracefully_singular,
)
from src.api.team_match import get_team_match_cached, get_team_matches_cached

from src.api.v2.utils import format_team, inv_format_team

router = APIRouter()


def get_v2_team_match(team_match: TeamMatch) -> Dict[str, Any]:
    # TODO: epa_{red,blue}_{auto,teleop,endgame}_score_pred
    return {
        "team": format_team(team_match.team),
        "year": team_match.year,
        "event": team_match.event,
        "match": team_match.match,
        "time": team_match.time,
        "offseason": team_match.offseason,
        "playoff": team_match.elim,
        "alliance": team_match.alliance,
        "status": team_match.status,
        "dq": team_match.dq,
        "surrogate": team_match.surrogate,
        "epa": team_match.epa,
        "auto_epa": team_match.auto_epa,
        "teleop_epa": team_match.teleop_epa,
        "endgame_epa": team_match.endgame_epa,
        "rp_1_epa": team_match.rp_1_epa,
        "rp_2_epa": team_match.rp_2_epa,
        "post_epa": team_match.post_epa,
    }


@router.get("/")
async def read_root():
    return {"name": "Team Match Router"}


@router.get(
    "/team_match/{team}/{match}",
    description="Get a single Team Match object containing team and EPA predictions. Specify team number and match key ex: 5511, 2019ncwak_f1m1",
    response_description="A Team Match object.",
)
@async_fail_gracefully_singular
async def read_team_match(response: Response, team: int, match: str) -> Dict[str, Any]:
    team_match_obj: Optional[TeamMatch] = await get_team_match_cached(
        team=inv_format_team(team), match=match
    )
    if team_match_obj is None:
        raise Exception("Team Match not found")

    return get_v2_team_match(team_match_obj)


@router.get(
    "/team_matches/team/{team}/year/{year}",
    description="Get a list of Team Match objects for a single team and year. Specify team number and year ex: 5511, 2019. Note, includes offseason events.",
    response_description="A list of Team Match objects. See /team_match/{team}/{match} for more information.",
)
@async_fail_gracefully_plural
async def read_team_matches_team_year(
    response: Response, team: int, year: int
) -> List[Dict[str, Any]]:
    team_matches: List[TeamMatch] = await get_team_matches_cached(
        team=inv_format_team(team), year=year
    )
    return [get_v2_team_match(team_match) for team_match in team_matches]


@router.get(
    "/team_matches/team/{team}/event/{event}",
    description="Get a list of Team Match objects for a single team and event. Specify team number and event key ex: 5511, 2019ncwak",
    response_description="A list of Team Match objects. See /team_match/{team}/{match} for more information.",
)
@async_fail_gracefully_plural
async def read_team_matches_team_event(
    response: Response, team: int, event: str
) -> List[Dict[str, Any]]:
    team_matches: List[TeamMatch] = await get_team_matches_cached(
        team=inv_format_team(team), event=event
    )
    return [get_v2_team_match(team_match) for team_match in team_matches]


@router.get(
    "/team_matches/event/{event}",
    description="Get a list of Team Match objects for a single event. Specify event key ex: 2019ncwak",
    response_description="A list of Team Match objects. See /team_match/{team}/{match} for more information.",
)
@async_fail_gracefully_plural
async def read_team_matches_event(
    response: Response, event: str
) -> List[Dict[str, Any]]:
    team_matches: List[TeamMatch] = await get_team_matches_cached(event=event)
    return [get_v2_team_match(team_match) for team_match in team_matches]


@router.get(
    "/team_matches",
    description="Get a list of Team Match objects with optional filters",
    response_description="A list of Team Match objects. See /team_match/{team}/{match} for more information.",
)
@async_fail_gracefully_plural
async def read_team_matches(
    response: Response,
    team: Optional[int] = None,
    year: Optional[int] = None,
    event: Optional[str] = None,
    week: Optional[int] = None,
    match: Optional[str] = None,
    elims: Optional[bool] = None,
    offseason: Optional[bool] = False,
    metric: Optional[str] = None,
    ascending: Optional[bool] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> List[Dict[str, Any]]:
    team_matches: List[TeamMatch] = await get_team_matches_cached(
        team=None if team is None else inv_format_team(team),
        year=year,
        event=event,
        week=week,
        match=match,
        elim=elims,
        offseason=offseason,
        metric=metric,
        ascending=ascending,
        limit=limit,
        offset=offset,
    )
    return [get_v2_team_match(team_match) for team_match in team_matches]
