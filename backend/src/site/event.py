from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Response

from src.site.aggregation import (
    get_event,
    get_events,
    get_matches,
    get_team_events,
    get_team_matches,
    get_team_years,
    get_year,
)
from src.site.models import (
    APIEvent,
    APIMatch,
    APITeamEvent,
    APITeamMatch,
    APITeamYear,
    APIYear,
)
from src.utils.decorators import async_fail_gracefully

router = APIRouter()


@router.get("/events/all")
@async_fail_gracefully
async def read_all_events(response: Response) -> List[Dict[str, Any]]:
    events: List[APIEvent] = await get_events()
    return [{"key": event.key, "name": event.name} for event in events]


@router.get("/events/{year}")
@async_fail_gracefully
async def read_events(response: Response, year: int) -> Dict[str, Any]:
    year_obj: Optional[APIYear] = await get_year(year=year)
    if year_obj is None:
        raise Exception("Year not found")

    events: List[APIEvent] = await get_events(year=year)
    return {"year": year_obj.to_dict(), "events": [x.to_dict() for x in events]}


@router.get("/event/{event_id}")
@async_fail_gracefully
async def read_event(response: Response, event_id: str) -> Dict[str, Any]:
    if event_id == "2023cacmp1" or event_id == "2023cacmp2":
        event = APIEvent(
            event_id,
            "2023 California Champs - "
            + ("Shoreline" if event_id == "2023cacmp1" else "Redwood")
            + " Division",
            2023,
            6,
            "",
            "",
            "USA",
            "CA",
            None,
            False,
            "Upcoming",
            "",
            84,
            -1,
            None,
            None,
            None,
            None,
            None,
            None,
        )

        year: Optional[APIYear] = await get_year(year=event.year)
        if year is None:
            raise Exception("Year not found")

        if event_id == "2023cacmp1":
            teams = [
                4,
                8,
                100,
                115,
                192,
                294,
                581,
                597,
                599,
                649,
                687,
                846,
                968,
                972,
                973,
                1148,
                1323,
                1671,
                2073,
                2102,
                2429,
                2485,
                2584,
                2659,
                3128,
                3256,
                3473,
                4123,
                4159,
                4322,
                4414,
                4415,
                5026,
                5104,
                5171,
                5199,
                5274,
                5419,
                5458,
                5507,
                5924,
                5940,
                6036,
                6220,
                6995,
                8016,
                8404,
                8768,
                8793,
                9271,
            ]
        else:
            teams = [
                114,
                254,
                399,
                604,
                668,
                670,
                696,
                766,
                971,
                1072,
                1138,
                1160,
                1351,
                1388,
                1538,
                1622,
                1678,
                1868,
                2551,
                2637,
                2813,
                2839,
                3255,
                3476,
                3512,
                3647,
                3669,
                3749,
                3859,
                3970,
                4014,
                4135,
                4201,
                4255,
                4276,
                4419,
                4738,
                5089,
                5851,
                6560,
                6657,
                7137,
                7157,
                7447,
                8033,
                8048,
                9038,
                9084,
                9125,
                9143,
            ]

        team_years: List[APITeamYear] = await get_team_years(
            year=year.year, teams=frozenset(teams)
        )
        team_events: List[APITeamEvent] = [
            APITeamEvent(
                x.num,
                x.team,
                event.key,
                event.name,
                event.week,
                0,
                False,
                len(team_years),
                x.total_epa,
                x.rp_1_epa,
                x.rp_2_epa,
                x.total_epa,
                x.unitless_epa,
                x.norm_epa,
                x.auto_epa,
                x.teleop_epa,
                x.endgame_epa,
                x.rp_1_epa,
                x.rp_2_epa,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                -1,
                0,
                0,
                False,
            )
            for x in team_years
        ]

        matches: List[APIMatch] = []
        team_matches: List[APITeamMatch] = []

        out = {
            "event": event.to_dict(),
            "matches": [x.to_dict() for x in matches],
            "team_events": [x.to_dict() for x in team_events],
            "team_matches": [x.to_dict() for x in team_matches],
            "year": year.to_dict(),
        }

        return out

    event: Optional[APIEvent] = await get_event(event=event_id)
    if event is None:
        raise Exception("Event not found")

    year: Optional[APIYear] = await get_year(year=event.year)
    if year is None:
        raise Exception("Year not found")

    team_events: List[APITeamEvent] = await get_team_events(
        year=year.year,
        score_mean=year.score_mean,
        score_sd=year.score_sd,
        event=event_id,
    )
    matches: List[APIMatch] = await get_matches(event=event_id)
    team_matches: List[APITeamMatch] = await get_team_matches(event=event_id)

    out = {
        "event": event.to_dict(),
        "matches": [x.to_dict() for x in matches],
        "team_events": [x.to_dict() for x in team_events],
        "team_matches": [x.to_dict() for x in team_matches],
        "year": year.to_dict(),
    }

    return out


@router.get("/event/{event_id}/team_matches/{team}")
@async_fail_gracefully
async def read_team_matches(
    response: Response, event_id: str, team: int
) -> List[Dict[str, Any]]:
    team_matches: List[APITeamMatch] = await get_team_matches(event=event_id, team=team)
    return [x.to_dict() for x in team_matches]
