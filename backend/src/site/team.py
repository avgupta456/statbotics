from typing import Any, List, Optional

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from src.api import (
    get_teams_cached,
    get_team_cached,
    get_team_events_cached,
    get_team_year_cached,
    get_team_years_cached,
    get_year_cached,
    get_matches_cached,
    get_team_matches_cached,
)
from src.db.models import Match, TeamEvent, TeamMatch, TeamYear, Year, Team
from src.site.helper import compress
from src.utils.decorators import (
    async_fail_gracefully_plural,
    async_fail_gracefully_singular,
)

router = APIRouter()


@router.get("/teams/all")
@async_fail_gracefully_plural
async def read_all_teams(response: StreamingResponse, no_cache: bool = False) -> Any:
    teams: List[Team] = await get_teams_cached(site=True, no_cache=no_cache)
    data = [
        {"team": x.team, "name": x.name, "active": x.active}
        for x in teams
        if not x.offseason
    ]
    return compress(data)


@router.get("/team/{team_num}")
@async_fail_gracefully_singular
async def read_team(
    response: StreamingResponse, team_num: str, no_cache: bool = False
) -> Any:
    team: Optional[Team] = await get_team_cached(team=team_num, no_cache=no_cache)
    if team is None or team.offseason:
        raise Exception("Team not found")

    return compress(team.to_dict())


@router.get("/team/{team_num}/years")
@async_fail_gracefully_plural
async def read_team_years(
    response: StreamingResponse, team_num: str, no_cache: bool = False
) -> Any:
    team_years: List[TeamYear] = await get_team_years_cached(
        team=team_num, no_cache=True
    )
    out = [
        {
            "year": x.year,
            "team": x.team,
            "norm_epa": x.norm_epa,
            "unitless_epa": x.unitless_epa,
            "epa_rank": x.total_epa_rank,
            "epa_percentile": x.total_epa_percentile,
            "country_epa_rank": x.country_epa_rank,
            "country_epa_percentile": x.country_epa_percentile,
            "district_epa_rank": x.district_epa_rank,
            "district_epa_percentile": x.district_epa_percentile,
            "state_epa_rank": x.state_epa_rank,
            "state_epa_percentile": x.state_epa_percentile,
        }
        for x in team_years
    ]

    return compress(out)


@router.get("/team/{team_num}/{year}")
@async_fail_gracefully_singular
async def read_team_year(
    response: StreamingResponse, team_num: str, year: int, no_cache: bool = False
) -> Any:
    year_obj: Optional[Year] = await get_year_cached(year=year, no_cache=no_cache)
    if year_obj is None:
        raise Exception("Year not found")

    team_year: Optional[TeamYear] = await get_team_year_cached(
        team=team_num,
        year=year,
        no_cache=no_cache,
    )
    if team_year is None or team_year.offseason:
        raise Exception("TeamYear not found")

    team_events: List[TeamEvent] = await get_team_events_cached(
        year=year,
        team=team_num,
        offseason=None,
        no_cache=no_cache,
    )

    matches: List[Match] = await get_matches_cached(
        team=team_num, year=year, offseason=None, no_cache=no_cache
    )
    team_matches: List[TeamMatch] = await get_team_matches_cached(
        team=team_num, year=year, offseason=None, no_cache=no_cache
    )

    out = {
        "year": year_obj.to_dict(),
        "team_year": team_year.to_dict(),
        "team_events": [x.to_dict() for x in team_events],
        "matches": [x.to_dict() for x in matches],
        "team_matches": [x.to_dict() for x in team_matches],
    }

    return compress(out)
