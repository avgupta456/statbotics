from typing import Any, Dict, List, Optional

from fastapi import APIRouter
from fastapi.responses import Response

from src.api import (
    get_matches_cached,
    get_team_cached,
    get_team_events_cached,
    get_team_matches_cached,
    get_team_year_cached,
    get_team_years_cached,
    get_teams_cached,
    get_year_cached,
)
from src.db.models import Match, Team, TeamEvent, TeamMatch, TeamYear, Year

# from src.site.helper import compress
from src.utils.decorators import (
    async_fail_gracefully_plural,
    async_fail_gracefully_singular,
)

router = APIRouter()


def _read_all_teams(teams: List[Team]) -> List[Dict[str, Any]]:
    return [{"team": x.team, "name": x.name, "active": x.active} for x in teams]


@router.get("/teams/all")
@async_fail_gracefully_plural
async def read_all_teams(response: Response, no_cache: bool = False) -> Any:
    teams: List[Team] = await get_teams_cached(site=True, no_cache=no_cache)
    return _read_all_teams(teams)


@router.get("/team/{team_num}")
@async_fail_gracefully_singular
async def read_team_years(
    response: Response, team_num: int, no_cache: bool = False
) -> Any:
    team: Optional[Team] = await get_team_cached(team=team_num, no_cache=no_cache)
    if team is None:
        raise Exception("Team not found")

    team_years: List[TeamYear] = await get_team_years_cached(
        team=team_num, no_cache=True
    )
    team_year_stats = [
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

    out = {
        "team": team.to_dict(),
        "team_years": team_year_stats,
    }

    return out


@router.get("/team/{team_num}/{year}")
@async_fail_gracefully_singular
async def read_team_year(
    response: Response, team_num: int, year: int, no_cache: bool = False
) -> Any:
    year_obj: Optional[Year] = await get_year_cached(year=year, no_cache=no_cache)
    if year_obj is None:
        raise Exception("Year not found")

    team_year: Optional[TeamYear] = await get_team_year_cached(
        team=team_num,
        year=year,
        no_cache=no_cache,
    )
    if team_year is None:
        return {
            "year": year_obj.to_dict(),
        }

    team_events: List[TeamEvent] = await get_team_events_cached(
        year=year,
        team=team_num,
        no_cache=no_cache,
    )

    matches: List[Match] = await get_matches_cached(
        team=team_num, year=year, no_cache=no_cache
    )
    team_matches: List[TeamMatch] = await get_team_matches_cached(
        team=team_num, year=year, no_cache=no_cache
    )

    team_matches = sorted(team_matches, key=lambda x: x.time)
    matches = sorted(matches, key=lambda x: x.time)

    event_times: Dict[str, Optional[int]] = {e.event: None for e in team_events}
    for m in matches:
        event_time = event_times.get(m.event, None)
        if event_time is None or m.time < event_time:
            event_times[m.event] = m.time

    team_events = sorted(
        team_events, key=lambda x: (x.week, event_times[x.event] or x.time)
    )

    out = {
        "year": year_obj.to_dict(),
        "team_year": team_year.to_dict(),
        "team_events": [x.to_dict() for x in team_events],
        "matches": [x.to_dict() for x in matches],
        "team_matches": [x.to_dict() for x in team_matches],
    }

    return out
