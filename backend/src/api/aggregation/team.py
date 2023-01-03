from datetime import timedelta
from typing import List

from src.api.models.team import APITeam
from src.db.models.team import Team
from src.db.read.team import get_team as _get_team, get_teams as _get_teams
from src.utils.alru_cache import alru_cache


def unpack_team(team: Team) -> APITeam:
    return APITeam(
        num=team.team,
        team=team.name,
        state=team.state,
        country=team.country,
        district=team.district,
        rookie_year=team.rookie_year or 2002,
    )


@alru_cache(ttl=timedelta(minutes=5))
async def get_team(team_num: int) -> APITeam:
    team = _get_team(team_num)

    # If invalid, do not cache
    if team is None:
        return (False, None)  # type: ignore

    # If valid, cache
    return (True, unpack_team(team))  # type: ignore


@alru_cache(ttl=timedelta(minutes=5))
async def get_teams(no_cache: bool = False) -> List[APITeam]:
    team_objs: List[Team] = _get_teams()
    teams = [unpack_team(x) for x in team_objs]
    return (True, sorted(teams, key=lambda x: x.num))  # type: ignore
