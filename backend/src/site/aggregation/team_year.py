from datetime import timedelta
from typing import Dict, List, Optional

from src.db.models import TeamYear
from src.db.read import (
    get_team_year as _get_team_year,
    get_team_years as _get_team_years,
)
from src.site.models import APITeamYear
from src.site.static import get_epa_breakdown
from src.utils.alru_cache import alru_cache


def unpack_team_year(
    team_year: TeamYear, epa_breakdown: Optional[Dict[str, float]]
) -> APITeamYear:
    out_epa_breakdown = {}
    if epa_breakdown is not None:
        out_epa_breakdown["auto_cycles"] = epa_breakdown["auto_cycles"]
        out_epa_breakdown["teleop_cycles"] = epa_breakdown["teleop_cycles"]
        out_epa_breakdown["total_cycles"] = epa_breakdown["total_cycles"]

    return APITeamYear(
        year=team_year.year,
        num=team_year.team,
        team=team_year.name or str(team_year.team),
        state=team_year.state,
        country=team_year.country,
        district=team_year.district,
        is_competing=team_year.is_competing,
        next_event_key=team_year.next_event_key,
        next_event_name=team_year.next_event_name,
        next_event_week=team_year.next_event_week,
        epa_rank=team_year.total_epa_rank or -1,
        epa_count=team_year.total_team_count or -1,
        state_epa_rank=team_year.state_epa_rank or -1,
        state_epa_count=team_year.state_team_count or -1,
        country_epa_rank=team_year.country_epa_rank or -1,
        country_epa_count=team_year.country_team_count or -1,
        district_epa_rank=team_year.district_epa_rank or -1,
        district_epa_count=team_year.district_team_count or -1,
        total_epa=team_year.epa_end or 0,
        unitless_epa=team_year.unitless_epa_end or 0,
        norm_epa=team_year.norm_epa_end or 0,
        auto_epa=team_year.auto_epa_end or 0,
        teleop_epa=team_year.teleop_epa_end or 0,
        endgame_epa=team_year.endgame_epa_end or 0,
        rp_1_epa=team_year.rp_1_epa_end or 0,
        rp_2_epa=team_year.rp_2_epa_end or 0,
        wins=team_year.wins,
        losses=team_year.losses,
        ties=team_year.ties,
        count=team_year.count,
        offseason=team_year.offseason,
        epa_breakdown=out_epa_breakdown,
    )


@alru_cache(ttl=timedelta(minutes=1))
async def get_team_year(
    team: int, year: int, no_cache: bool = False
) -> Optional[APITeamYear]:
    team_year_obj = _get_team_year(team=team, year=year)  # type: ignore

    # If invalid, do not cache
    if team_year_obj is None:
        return (False, None)  # type: ignore

    epa_breakdown = {}
    if year == 2023:
        epa_breakdown = get_epa_breakdown([team])

    # If valid, cache
    return (True, unpack_team_year(team_year_obj, epa_breakdown.get(team, None)))  # type: ignore


@alru_cache(ttl=timedelta(minutes=5))
async def get_team_years(
    team: Optional[int] = None,
    year: Optional[int] = None,
    limit: Optional[int] = None,
    metric: Optional[str] = None,
    no_cache: bool = False,
) -> List[APITeamYear]:
    team_year_objs: List[TeamYear] = _get_team_years(
        team=team, year=year, limit=limit, metric=metric
    )

    epa_breakdown = {}
    if year == 2023:
        epa_breakdown = get_epa_breakdown([x.team for x in team_year_objs])

    team_years = [
        unpack_team_year(x, epa_breakdown.get(x.team, None)) for x in team_year_objs
    ]

    return (True, sorted(team_years, key=lambda x: x.epa_rank))  # type: ignore
