from datetime import timedelta
from typing import List, Optional

from src.api.models import APITeamYear
from src.db.models import TeamYear
from src.db.read import (
    get_team_year as _get_team_year,
    get_team_years as _get_team_years,
)
from src.utils.alru_cache import alru_cache


def unpack_team_year(team_year: TeamYear) -> APITeamYear:
    return APITeamYear(
        num=team_year.team,
        team=team_year.name or str(team_year.team),
        state=team_year.state,
        country=team_year.country,
        district=team_year.district,
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
        norm_epa=team_year.norm_epa_end or 0,
        total_epa=team_year.epa_end or 0,
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
    )


@alru_cache(ttl=timedelta(minutes=5))
async def get_team_year(
    team: Optional[int] = None, year: Optional[int] = None, no_cache: bool = False
) -> Optional[APITeamYear]:
    team_year_obj = _get_team_year(team=team, year=year)  # type: ignore

    # If invalid, do not cache
    if team_year_obj is None:
        return (False, None)  # type: ignore

    # If valid, cache
    return (True, unpack_team_year(team_year_obj))  # type: ignore


@alru_cache(ttl=timedelta(minutes=5))
async def get_team_years(
    year: Optional[int] = None, no_cache: bool = False
) -> List[APITeamYear]:
    team_year_objs: List[TeamYear] = _get_team_years(year)  # type: ignore

    team_years = [unpack_team_year(x) for x in team_year_objs]
    return (True, sorted(team_years, key=lambda x: x.epa_rank))  # type: ignore
