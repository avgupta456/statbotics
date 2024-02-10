from datetime import timedelta
from typing import List

from src.db.models import Team
from src.db.read import get_team as _get_team, get_teams as _get_teams
from src.site.models import APITeam
from src.utils.alru_cache import alru_cache


def unpack_team(team: Team) -> APITeam:
    return APITeam(
        num=team.team,
        team=team.name,
        active=team.active or False,
        state=team.state,
        country=team.country,
        district=team.district,
        rookie_year=team.rookie_year or 2002,
        offseason=team.offseason,
    )


@alru_cache(ttl=timedelta(minutes=1))
async def get_team(team: int, no_cache: bool = False) -> APITeam:
    team_obj = _get_team(team=team)

    # If invalid, do not cache
    if team_obj is None:
        return (False, None)  # type: ignore

    # If valid, cache
    return (True, unpack_team(team_obj))  # type: ignore


@alru_cache(ttl=timedelta(minutes=5))
async def get_teams(no_cache: bool = False) -> List[APITeam]:
    team_objs: List[Team] = _get_teams()
    teams = [unpack_team(x) for x in team_objs]
    return (True, sorted(teams, key=lambda x: x.num or 0))  # type: ignore
