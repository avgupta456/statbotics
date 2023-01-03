from datetime import timedelta
from typing import List, Optional

from src.api.models.team_year import APITeamYear
from src.db.models.team_year import TeamYear
from src.db.read.team_year import (
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
        epa_rank=team_year.total_epa_rank or -1,
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
    )


@alru_cache(ttl=timedelta(minutes=5))
async def get_team_year(
    team_num: Optional[int] = None, year: Optional[int] = None, no_cache: bool = False
) -> Optional[APITeamYear]:
    team_year = _get_team_year(team_num, year)  # type: ignore

    # If invalid, do not cache
    if team_year is None:
        return (False, None)  # type: ignore

    # If valid, cache
    return (True, unpack_team_year(team_year))  # type: ignore


@alru_cache(ttl=timedelta(minutes=5))
async def get_team_years(
    year: Optional[int] = None, no_cache: bool = False
) -> List[APITeamYear]:
    team_year_objs: List[TeamYear] = _get_team_years(year)  # type: ignore

    team_years = [unpack_team_year(x) for x in team_year_objs]
    return (True, sorted(team_years, key=lambda x: x.epa_rank))  # type: ignore
