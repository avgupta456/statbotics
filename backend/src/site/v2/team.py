from typing import Any, List, Optional

from fastapi import APIRouter, Response

from src.site.v2.aggregation import (
    get_matches,
    get_team,
    get_team_events,
    get_team_matches,
    get_team_year,
    get_team_years,
    get_teams,
    get_year,
)
from src.site.v2.models import (
    APIMatch,
    APITeam,
    APITeamEvent,
    APITeamMatch,
    APITeamYear,
    APIYear,
)
from src.site.v2.utils import async_fail_gracefully

router = APIRouter()


@router.get("/teams/all")
@async_fail_gracefully
async def read_all_teams(response: Response, no_cache: bool = False) -> Any:
    teams: List[APITeam] = await get_teams(no_cache=no_cache)
    return [
        {"num": x.num, "team": x.team, "active": x.active}
        for x in teams
        if not x.offseason
    ]


@router.get("/team/{team_num}")
@async_fail_gracefully
async def read_team(response: Response, team_num: int, no_cache: bool = False) -> Any:
    team: Optional[APITeam] = await get_team(team=team_num, no_cache=no_cache)
    if team is None or team.offseason:
        raise Exception("Team not found")

    return team.to_dict()


@router.get("/team/{team_num}/years")
@async_fail_gracefully
async def read_team_years(
    response: Response, team_num: int, no_cache: bool = False
) -> Any:
    team_years: List[APITeamYear] = await get_team_years(
        team=team_num, no_cache=no_cache
    )
    return [
        {
            "year": x.year,
            "team": x.team,
            "norm_epa": x.norm_epa,
            "unitless_epa": x.unitless_epa,
            "epa_rank": x.epa_rank if x.epa_count > 0 else None,
            "epa_percentile": x.epa_rank / x.epa_count if x.epa_count > 0 else None,
            "country_epa_rank": x.country_epa_rank if x.country_epa_count > 0 else None,
            "country_epa_percentile": (
                x.country_epa_rank / x.country_epa_count
                if x.country_epa_count > 0
                else None
            ),
            "district_epa_rank": (
                x.district_epa_rank if x.district_epa_count > 0 else None
            ),
            "district_epa_percentile": (
                x.district_epa_rank / x.district_epa_count
                if x.district_epa_count > 0
                else None
            ),
            "state_epa_rank": x.state_epa_rank if x.state_epa_count > 0 else None,
            "state_epa_percentile": (
                x.state_epa_rank / x.state_epa_count if x.state_epa_count > 0 else None
            ),
        }
        for x in team_years
    ]


@router.get("/team/{team_num}/{year}")
@async_fail_gracefully
async def read_team_year(
    response: Response, team_num: int, year: int, no_cache: bool = False
) -> Any:
    year_obj: Optional[APIYear] = await get_year(year=year, no_cache=no_cache)
    if year_obj is None:
        raise Exception("Year not found")

    team_year: Optional[APITeamYear] = await get_team_year(
        team=team_num, year=year, no_cache=no_cache
    )
    if team_year is None or team_year.offseason:
        raise Exception("TeamYear not found")

    team_events: List[APITeamEvent] = await get_team_events(
        year=year, team=team_num, offseason=None, no_cache=no_cache
    )

    matches: List[APIMatch] = await get_matches(
        team=team_num, year=year, offseason=None, no_cache=no_cache
    )
    team_matches: List[APITeamMatch] = await get_team_matches(
        team=team_num, year=year, offseason=None, no_cache=no_cache
    )

    out = {
        "year": year_obj.to_dict(),
        "team_year": team_year.to_dict(),
        "team_events": [x.to_dict() for x in team_events],
        "matches": [x.to_dict() for x in matches],
        "team_matches": [x.to_dict() for x in team_matches],
    }

    return out
