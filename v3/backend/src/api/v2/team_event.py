from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Response

from src.api.v2.utils import format_team, inv_format_team, format_type
from src.db.models import TeamEvent
from src.api.team_event import get_team_event_cached, get_team_events_cached
from src.utils.decorators import (
    async_fail_gracefully_plural,
    async_fail_gracefully_singular,
)

router = APIRouter()


def get_v2_team_event(team_event: TeamEvent) -> Dict[str, Any]:
    # TODO: {auto,teleop,endgame,rp_1,rp_2}_epa_{start,pre_playoffs,mean,max}
    return {
        "team": format_team(team_event.team),
        "year": team_event.year,
        "event": team_event.event,
        "offseason": team_event.offseason,
        "team_name": team_event.team_name,
        "event_name": team_event.event_name,
        "state": team_event.state,
        "country": team_event.country,
        "district": team_event.district,
        "type": format_type(team_event.type),
        "week": team_event.week,
        "status": team_event.status,
        "first_event": team_event.first_event,
        "epa_start": team_event.epa_start,
        "epa_pre_playoffs": team_event.epa_pre_elim,
        "epa_end": team_event.epa,
        "epa_mean": team_event.epa_mean,
        "epa_max": team_event.epa_max,
        "epa_diff": team_event.epa - team_event.epa_start,
        "auto_epa_start": None,
        "auto_epa_pre_playoffs": None,
        "auto_epa_end": team_event.auto_epa,
        "auto_epa_mean": None,
        "auto_epa_max": None,
        "teleop_epa_start": None,
        "teleop_epa_pre_playoffs": None,
        "teleop_epa_end": team_event.teleop_epa,
        "teleop_epa_mean": None,
        "teleop_epa_max": None,
        "endgame_epa_start": None,
        "endgame_epa_pre_playoffs": None,
        "endgame_epa_end": team_event.endgame_epa,
        "endgame_epa_mean": None,
        "endgame_epa_max": None,
        "rp_1_epa_start": None,
        "rp_1_epa_end": team_event.rp_1_epa,
        "rp_1_epa_mean": None,
        "rp_1_epa_max": None,
        "rp_2_epa_start": None,
        "rp_2_epa_end": team_event.rp_2_epa,
        "rp_2_epa_mean": None,
        "rp_2_epa_max": None,
        "wins": team_event.wins,
        "losses": team_event.losses,
        "ties": team_event.ties,
        "count": team_event.count,
        "winrate": team_event.winrate,
        "qual_wins": team_event.qual_wins,
        "qual_losses": team_event.qual_losses,
        "qual_ties": team_event.qual_ties,
        "qual_count": team_event.qual_count,
        "qual_winrate": team_event.qual_winrate,
        "rps": team_event.rps,
        "rps_per_match": team_event.rps_per_match,
        "rank": team_event.rank,
        "num_teams": team_event.num_teams,
    }


@router.get("/")
async def read_root():
    return {"name": "Team Event Router"}


@router.get(
    "/team_event/{team}/{event}",
    description="Get a single Team Event object containing event metadata, EPA statistics, and winrate. Specify team number and event key ex: 5511, 2019ncwak",
    response_description="A Team Event object.",
)
@async_fail_gracefully_singular
async def read_team_event(response: Response, team: int, event: str) -> Dict[str, Any]:
    team_event_obj: Optional[TeamEvent] = await get_team_event_cached(
        team=inv_format_team(team), event=event
    )
    if team_event_obj is None:
        raise Exception("Team Event not found")

    return get_v2_team_event(team_event_obj)


@router.get(
    "/team_events/team/{team}",
    description="Get a list of Team Event objects for a single team. Specify team number, ex: 5511",
    response_description="A list of Team Event objects. See /team_event/{team}/{event} for more information.",
)
@async_fail_gracefully_plural
async def read_team_events_team(response: Response, team: int) -> List[Dict[str, Any]]:
    team_events: List[TeamEvent] = await get_team_events_cached(
        team=inv_format_team(team)
    )
    return [get_v2_team_event(team_event) for team_event in team_events]


@router.get(
    "/team_events/team/{team}/year/{year}",
    description="Get a list of Team Event objects for a single team and year. Specify team number and year, ex: 5511, 2019",
    response_description="A list of Team Event objects. See /team_event/{team}/{event} for more information.",
)
@async_fail_gracefully_plural
async def read_team_events_team_year(
    response: Response, team: int, year: int
) -> List[Dict[str, Any]]:
    team_events: List[TeamEvent] = await get_team_events_cached(
        team=inv_format_team(team), year=year
    )
    return [get_v2_team_event(team_event) for team_event in team_events]


@router.get(
    "/team_events/event/{event}",
    description="Get a list of Team Event objects for a single event. Specify event key, ex: 2019ncwak",
    response_description="A list of Team Event objects. See /team_event/{team}/{event} for more information.",
)
@async_fail_gracefully_plural
async def read_team_events_event(
    response: Response, event: str
) -> List[Dict[str, Any]]:
    team_events: List[TeamEvent] = await get_team_events_cached(event=event)
    return [get_v2_team_event(team_event) for team_event in team_events]


@router.get(
    "/team_events/year/{year}/district/{district}",
    description="Get a list of Team Event objects for a single year and district. Specify year and district, ex: 2019, fnc",
    response_description="A list of Team Event objects. See /team_event/{team}/{event} for more information.",
)
@async_fail_gracefully_plural
async def read_team_events_year_district(
    response: Response, year: int, district: str
) -> List[Dict[str, Any]]:
    team_events: List[TeamEvent] = await get_team_events_cached(
        year=year, district=district
    )
    return [get_v2_team_event(team_event) for team_event in team_events]


@router.get(
    "/team_events/year/{year}/state/{state}",
    description="Get a list of Team Event objects for a single year and state. Specify year and state, ex: 2019, NC",
    response_description="A list of Team Event objects. See /team_event/{team}/{event} for more information.",
)
@async_fail_gracefully_plural
async def read_team_events_year_state(
    response: Response, year: int, state: str
) -> List[Dict[str, Any]]:
    team_events: List[TeamEvent] = await get_team_events_cached(year=year, state=state)
    return [get_v2_team_event(team_event) for team_event in team_events]


@router.get(
    "/team_events",
    description="Get a list of all Team Event objects with optional filters.",
    response_description="A list of Team Event objects. See /team_event/{team}/{event} for more information.",
)
@async_fail_gracefully_plural
async def read_team_events(
    response: Response,
    team: Optional[int] = None,
    year: Optional[int] = None,
    event: Optional[str] = None,
    country: Optional[str] = None,
    district: Optional[str] = None,
    state: Optional[str] = None,
    type: Optional[int] = None,
    week: Optional[int] = None,
    offseason: Optional[bool] = False,
    metric: Optional[str] = None,
    ascending: Optional[bool] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> List[Dict[str, Any]]:
    if type is not None:
        raise Exception("Event type filter not supported")
    team_events: List[TeamEvent] = await get_team_events_cached(
        team=None if team is None else inv_format_team(team),
        year=year,
        event=event,
        country=country,
        district=district,
        state=state,
        week=week,
        offseason=offseason,
        metric=metric,
        ascending=ascending,
        limit=limit,
        offset=offset,
    )
    return [get_v2_team_event(team_event) for team_event in team_events]
