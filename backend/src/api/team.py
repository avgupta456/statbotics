from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Response

from src.api.aggregation.team_match import get_team_matches
from src.api.aggregation.year import get_year
from src.api.db.team import get_team, get_teams
from src.api.db.team_year import get_team_year
from src.api.db.team_event import get_team_events
from src.api.db.match import get_matches
from src.db.models.team import Team
from src.db.models.team_year import TeamYear
from src.db.models.team_event import TeamEvent
from src.db.models.match import Match
from src.api.utils import unpack_match
from src.data.nepa import get_epa_to_norm_epa_func
from src.utils.decorators import async_fail_gracefully

router = APIRouter()


@router.get("/")
async def read_root():
    return {"name": "Team Router"}


@router.get("/teams/all")
@async_fail_gracefully
async def read_all_teams(response: Response) -> List[Dict[str, Any]]:
    teams: List[Team] = await get_teams()
    return [{"num": x.team, "team": x.name} for x in teams if not x.offseason]


@router.get("/team/{team_num}")
@async_fail_gracefully
async def read_team(response: Response, team_num: int) -> Dict[str, Any]:
    team: Optional[Team] = await get_team(team_num)

    if team is None or team.offseason:
        raise Exception("Team not found")

    return {
        "num": team_num,
        "team": team.name,
        "country": team.country,
        "state": team.state,
        "district": team.district,
        "rookie_year": max(2002, team.rookie_year or 0),
    }


@router.get("/team/{team_num}/{year}")
@async_fail_gracefully
async def read_team_year(
    response: Response, team_num: int, year: int
) -> Dict[str, Any]:
    epa_to_norm_epa = get_epa_to_norm_epa_func(year)

    foul_rate = (await get_year(year)).foul_rate
    team_year: Optional[TeamYear] = await get_team_year(team_num, year)

    if team_year is None or team_year.offseason:
        raise Exception("TeamYear not found")

    team_event_objs: List[TeamEvent] = await get_team_events(year=year, team=team_num)
    match_objs: List[Match] = await get_matches(team_num, year)

    team_events: List[Dict[str, Any]] = []
    for x in team_event_objs:
        team_event_matches = [
            {
                **unpack_match(m),
                "alliance": "red" if team_num in m.get_red() else "blue",
            }
            for m in match_objs
            if m.event == x.event
        ]

        team_event_matches.sort(key=lambda x: x["time"] or 0)

        team_events.append(
            {
                "time": x.time,
                "event": x.event,
                "event_name": x.event_name,
                "week": x.week,
                "epa": x.epa_end,
                "norm_epa": epa_to_norm_epa(x.epa_end or 0),
                "auto_epa": x.auto_epa_end,
                "teleop_epa": x.teleop_epa_end,
                "endgame_epa": x.endgame_epa_end,
                "rp_1_epa": x.rp_1_epa_end,
                "rp_2_epa": x.rp_2_epa_end,
                "wins": x.wins,
                "losses": x.losses,
                "ties": x.ties,
                "count": x.count,
                "rank": x.rank,
                "num_teams": x.num_teams,
                "matches": team_event_matches,
            }
        )

    team_events.sort(key=lambda x: x["time"] or 0)

    team_matches = await get_team_matches(team_num, year, epa_to_norm_epa)

    out = {
        "num": team_num,
        "team": team_year.name,
        "year": year,
        "team_year": {
            "epa_rank": team_year.total_epa_rank,
            "epa_count": team_year.total_team_count,
            "country_epa_rank": team_year.country_epa_rank,
            "country_count": team_year.country_team_count,
            "state_epa_rank": team_year.state_epa_rank,
            "state_count": team_year.state_team_count,
            "district_epa_rank": team_year.district_epa_rank,
            "district_count": team_year.district_team_count,
            "wins": team_year.wins,
            "losses": team_year.losses,
            "ties": team_year.ties,
            "count": team_year.count,
            "epa": team_year.epa_end,
            "norm_epa": team_year.norm_epa_end,
            "auto_epa": team_year.auto_epa_end,
            "teleop_epa": team_year.teleop_epa_end,
            "endgame_epa": team_year.endgame_epa_end,
            "rp_1_epa": team_year.rp_1_epa_end,
            "rp_2_epa": team_year.rp_2_epa_end,
            "foul_rate": foul_rate,
        },
        "team_events": team_events,
        "team_matches": team_matches,
    }

    return out
