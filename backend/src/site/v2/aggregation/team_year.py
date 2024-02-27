from datetime import timedelta
from typing import List, Optional, Tuple

from src.api.v2.utils import format_team, inv_format_team
from src.constants import CURR_WEEK
from src.db.models import TeamYear
from src.db.read import (
    get_team_year as _get_team_year,
    get_team_years as _get_team_years,
)
from src.site.v2.models import APITeamYear
from src.utils.alru_cache import alru_cache


def unpack_team_year(team_year: TeamYear) -> APITeamYear:
    return APITeamYear(
        year=team_year.year,
        num=format_team(team_year.team),
        team=team_year.name or str(team_year.team),
        state=team_year.state,
        country=team_year.country,
        district=team_year.district,
        is_competing=team_year.next_event_week == CURR_WEEK,
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
        total_epa=team_year.epa or 0,
        unitless_epa=team_year.unitless_epa or 0,
        norm_epa=team_year.norm_epa or 0,
        auto_epa=team_year.auto_epa or 0,
        teleop_epa=team_year.teleop_epa or 0,
        endgame_epa=team_year.endgame_epa or 0,
        rp_1_epa=team_year.rp_1_epa or 0,
        rp_2_epa=team_year.rp_2_epa or 0,
        wins=team_year.wins,
        losses=team_year.losses,
        ties=team_year.ties,
        count=team_year.count,
        offseason=team_year.offseason,
    )


@alru_cache(ttl=timedelta(minutes=1))
async def get_team_year(
    team: int, year: int, no_cache: bool = False
) -> Tuple[bool, Optional[APITeamYear]]:
    team_year_obj = _get_team_year(team=inv_format_team(team), year=year)

    # If invalid, do not cache
    if team_year_obj is None:
        return (False, None)

    # If valid, cache
    return (True, unpack_team_year(team_year_obj))


@alru_cache(ttl=timedelta(minutes=5))
async def get_team_years(
    team: Optional[int] = None,
    teams: Optional[List[int]] = None,
    year: Optional[int] = None,
    limit: Optional[int] = None,
    metric: Optional[str] = None,
    no_cache: bool = False,
) -> Tuple[bool, List[APITeamYear]]:
    if metric is not None and metric.endswith("_end"):
        metric = metric[:-4]

    team_year_objs: List[TeamYear] = _get_team_years(
        team=None if team is None else inv_format_team(team),
        teams=None if teams is None else [inv_format_team(team) for team in teams],
        year=year,
        limit=limit,
        metric=metric,
    )

    team_years = [unpack_team_year(x) for x in team_year_objs]

    return (True, sorted(team_years, key=lambda x: x.epa_rank or 0))
