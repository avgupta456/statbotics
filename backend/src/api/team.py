from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Response

from src.api.aggregation.team_match import get_team_matches
from src.api.db.team import get_team, get_teams
from src.api.db.team_year import get_team_year
from src.api.db.team_event import get_team_events
from src.api.db.match import get_matches
from src.db.models.team import Team
from src.db.models.team_year import TeamYear
from src.db.models.team_event import TeamEvent
from src.db.models.match import Match
from src.data.nepa import get_epa_to_norm_epa_func
from src.utils.decorators import async_fail_gracefully

router = APIRouter()


@router.get("/")
async def read_root():
    return {"name": "Team Router"}


@router.get("/teams/all")
@async_fail_gracefully
async def read_all_teams(response: Response) -> List[Dict[str, Any]]:
    return [{"num": x.team, "team": x.name} for x in await get_teams()]


@router.get("/team/{team_num}")
@async_fail_gracefully
async def read_team(response: Response, team_num: int) -> Dict[str, Any]:
    team: Optional[Team] = await get_team(team_num)

    if team is None:
        raise Exception("Team not found")

    return {
        "num": team_num,
        "team": team.name,
        "country": team.country,
        "state": team.state,
        "district": team.district,
        "rookie_year": 2008,  # TODO: Add to, get from DB
    }


@router.get("/team/{team_num}/{year}")
@async_fail_gracefully
async def read_team_year(
    response: Response, team_num: int, year: int
) -> Dict[str, Any]:
    epa_to_norm_epa = get_epa_to_norm_epa_func(year)

    team_year: Optional[TeamYear] = await get_team_year(team_num, year)

    if team_year is None:
        raise Exception("TeamYear not found")

    team_event_objs: List[TeamEvent] = await get_team_events(year=year, team=team_num)
    match_objs: List[Match] = await get_matches(team_num, year)

    team_events: List[Dict[str, Any]] = []
    for x in team_event_objs:
        team_event_matches = [
            {
                "time": m.time,
                "comp_level": m.comp_level,
                "set_number": m.set_number,
                "match_number": m.match_number,
                "alliance": "red" if team_num in m.get_red() else "blue",
                "red": m.get_red(),
                "blue": m.get_blue(),
                "red_score": m.red_score,
                "blue_score": m.blue_score,
                "red_rp_1": m.red_rp_1,
                "red_rp_2": m.red_rp_2,
                "blue_rp_1": m.blue_rp_1,
                "blue_rp_2": m.blue_rp_2,
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
        },
        "team_events": team_events,
        "team_matches": team_matches,
    }

    return out
