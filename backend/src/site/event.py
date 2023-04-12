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

        team_dict = {x.num: x for x in team_events}

        if event_id == "2023cacmp1":
            _matches = [
                [3128, 5026, 1148, 100, 8, 2485],
                [5104, 5274, 4159, 4322, 5924, 968],
                [6220, 4415, 4414, 5940, 5419, 599],
                [9271, 115, 8016, 8768, 4, 1323],
                [972, 4123, 846, 6995, 2073, 597],
                [8404, 6036, 5199, 687, 3473, 973],
                [1671, 294, 192, 649, 2584, 5171],
                [5507, 2659, 5458, 581, 3256, 2429],
                [2102, 9271, 597, 8793, 8, 968],
                [846, 1148, 2485, 599, 4415, 4159],
                [2584, 5199, 5924, 972, 973, 8404],
                [4123, 5274, 100, 8768, 649, 5104],
                [115, 2073, 3256, 1671, 5940, 687],
                [3473, 5507, 5419, 192, 5458, 8016],
                [2429, 8793, 294, 6995, 4322, 4414],
                [4, 6220, 2659, 2102, 6036, 3128],
                [5026, 5171, 968, 581, 1323, 649],
                [192, 846, 3473, 5924, 4415, 9271],
                [5199, 4123, 2429, 4414, 2584, 2485],
                [2659, 8, 973, 5274, 8016, 2073],
                [8404, 597, 5940, 1148, 5104, 6220],
                [5171, 8793, 115, 972, 100, 5419],
                [1323, 4159, 3256, 294, 2102, 581],
                [8768, 6995, 599, 5026, 6036, 5507],
                [1671, 5458, 4322, 4, 3128, 687],
                [968, 5419, 8404, 846, 2659, 100],
                [3473, 8793, 1323, 1148, 294, 2073],
                [2584, 9271, 973, 4415, 649, 6995],
                [5458, 6220, 4123, 1671, 8, 115],
                [2485, 5507, 687, 5274, 4, 972],
                [192, 5924, 5940, 5026, 8768, 2429],
                [597, 6036, 8016, 581, 3128, 4414],
                [599, 5104, 4322, 5199, 5171, 3256],
                [4159, 8404, 6995, 2102, 1671, 5419],
                [8793, 5026, 100, 6220, 2584, 687],
                [581, 846, 4, 1148, 4123, 973],
                [597, 192, 972, 3256, 294, 599],
                [115, 5199, 5274, 6036, 4159, 9271],
                [8768, 2485, 3473, 2659, 5104, 4414],
                [4415, 3128, 968, 5171, 2073, 5507],
                [5940, 2429, 4322, 8, 8016, 1323],
                [5924, 649, 1148, 5458, 2102, 5199],
                [4414, 5419, 846, 4, 5026, 3256],
                [100, 6036, 973, 2485, 9271, 294],
                [968, 192, 2659, 4123, 6995, 115],
                [972, 5104, 687, 8, 2102, 2429],
                [8016, 8768, 1671, 8793, 4322, 4415],
                [649, 6220, 599, 2073, 581, 5924],
                [3128, 5507, 2584, 3473, 4159, 5940],
                [1323, 5171, 597, 5274, 5458, 8404],
                [4414, 1148, 2429, 1671, 973, 968],
                [2102, 100, 2073, 6036, 192, 4322],
                [5104, 581, 8, 115, 294, 5419],
                [972, 3128, 5199, 4415, 1323, 4123],
                [599, 5458, 9271, 8404, 2584, 5026],
                [687, 5171, 5274, 5940, 8016, 846],
                [3256, 3473, 6995, 6220, 5924, 2485],
                [4159, 5507, 649, 8793, 2659, 597],
                [8768, 5199, 2073, 4, 5419, 5458],
                [294, 4414, 5026, 4123, 8404, 8016],
                [2102, 6995, 5274, 115, 599, 3128],
                [5104, 1323, 973, 5507, 192, 6220],
                [2485, 6036, 5940, 8793, 5924, 1671],
                [2659, 3256, 687, 5171, 9271, 1148],
                [8768, 968, 581, 2584, 8, 3473],
                [4415, 2429, 4, 597, 100, 4159],
                [4322, 972, 6220, 846, 649, 5458],
                [687, 5924, 5419, 3128, 1323, 294],
                [4414, 2073, 1671, 9271, 5104, 5507],
                [581, 6995, 2659, 100, 5199, 5940],
                [4123, 4, 8793, 599, 3473, 5274],
                [4159, 115, 4322, 973, 597, 5026],
                [2102, 8016, 2485, 846, 968, 2584],
                [8768, 1148, 6036, 5171, 972, 2429],
                [4415, 8, 8404, 192, 3256, 649],
                [599, 1323, 5026, 3473, 1671, 2659],
                [5940, 6220, 294, 968, 9271, 5199],
                [8016, 100, 4414, 5458, 972, 4159],
                [2584, 192, 5419, 4322, 1148, 5274],
                [8, 4, 5171, 5507, 6995, 5924],
                [3256, 2102, 973, 3128, 4123, 8768],
                [649, 2073, 8404, 2429, 2485, 115],
                [5104, 846, 4415, 6036, 8793, 581],
                [687, 192, 5199, 597, 5924, 4414],
            ]
        elif event_id == "2023cacmp2":
            _matches = [
                [1622, 254, 3669, 1351, 9038, 399],
                [1538, 6560, 2637, 8048, 2813, 5851],
                [1138, 7137, 604, 2551, 2839, 114],
                [7447, 9084, 4255, 3647, 4014, 668],
                [3749, 9125, 696, 3512, 7157, 8033],
                [971, 3255, 4738, 4276, 5089, 4419],
                [1868, 670, 4201, 4135, 1072, 3476],
                [1678, 3970, 6657, 3859, 9143, 1160],
                [1388, 7447, 8033, 766, 9038, 5851],
                [696, 3669, 399, 114, 7137, 2637],
                [1072, 4738, 2813, 3749, 4419, 971],
                [9125, 6560, 1351, 3647, 4135, 1538],
                [9084, 7157, 9143, 1868, 2551, 4276],
                [5089, 1678, 2839, 4201, 6657, 4255],
                [1160, 766, 670, 3512, 8048, 604],
                [4014, 1138, 3970, 1388, 3255, 1622],
                [254, 3476, 5851, 3859, 668, 4135],
                [4201, 696, 5089, 2813, 7137, 7447],
                [4738, 9125, 1160, 604, 1072, 399],
                [3970, 9038, 4419, 6560, 4255, 7157],
                [971, 8033, 2551, 3669, 1538, 1138],
                [3476, 766, 9084, 3749, 1351, 2839],
                [668, 2637, 9143, 670, 1388, 3859],
                [3647, 3512, 114, 254, 3255, 1678],
                [1868, 6657, 8048, 4014, 1622, 4276],
                [5851, 2839, 971, 696, 3970, 1351],
                [5089, 766, 668, 3669, 670, 7157],
                [1072, 7447, 4419, 7137, 4135, 3512],
                [6657, 1138, 9125, 1868, 9038, 9084],
                [399, 1678, 4276, 6560, 4014, 3749],
                [4201, 2813, 2551, 254, 3647, 1160],
                [8033, 3255, 4255, 3859, 1622, 604],
                [114, 1538, 8048, 4738, 3476, 9143],
                [2637, 971, 3512, 1388, 1868, 2839],
                [766, 254, 1351, 1138, 1072, 4276],
                [3859, 696, 4014, 3669, 9125, 4419],
                [8033, 4201, 3749, 9143, 670, 114],
                [9084, 4738, 6560, 3255, 2637, 7447],
                [3647, 399, 5089, 3970, 1538, 604],
                [7137, 1622, 5851, 3476, 7157, 1678],
                [2551, 1160, 8048, 9038, 4255, 668],
                [2813, 4135, 3669, 6657, 1388, 4738],
                [604, 2839, 696, 4014, 254, 9143],
                [1351, 3255, 4419, 399, 7447, 670],
                [5851, 4201, 3970, 9125, 3512, 9084],
                [3749, 1538, 4276, 9038, 1388, 1160],
                [4255, 3647, 1868, 766, 8048, 7137],
                [4135, 1138, 114, 7157, 3859, 2813],
                [1622, 1678, 1072, 5089, 2637, 2551],
                [668, 3476, 8033, 6560, 6657, 971],
                [604, 3669, 1160, 1868, 4419, 5851],
                [1388, 1351, 7157, 3255, 4201, 8048],
                [1538, 3859, 9038, 9084, 670, 2839],
                [3749, 1622, 4738, 7137, 668, 9125],
                [114, 6657, 7447, 971, 1072, 254],
                [4276, 3476, 6560, 2551, 4255, 696],
                [9143, 5089, 3512, 1138, 2813, 399],
                [2637, 1678, 4135, 766, 3970, 8033],
                [3647, 4738, 7157, 4014, 2839, 6657],
                [670, 604, 254, 9125, 971, 4255],
                [1388, 3512, 6560, 9084, 114, 1622],
                [1538, 668, 4419, 1678, 4201, 1138],
                [399, 3255, 2551, 766, 2813, 1868],
                [3970, 9143, 4276, 3476, 7447, 3669],
                [3647, 5851, 3859, 1072, 9038, 5089],
                [7137, 1160, 4014, 8033, 1351, 2637],
                [8048, 3749, 1138, 696, 4135, 6657],
                [4276, 2813, 2839, 1622, 668, 670],
                [604, 7157, 1868, 7447, 1538, 1678],
                [3859, 3512, 3970, 1351, 4738, 2551],
                [9125, 4014, 766, 114, 5089, 6560],
                [2637, 9084, 8048, 4419, 8033, 254],
                [1388, 4255, 399, 696, 5851, 1072],
                [3647, 3669, 3255, 3476, 3749, 1160],
                [7137, 9038, 971, 4201, 9143, 4135],
                [114, 668, 254, 5089, 1868, 3970],
                [2551, 1138, 670, 5851, 7447, 4738],
                [4255, 1351, 604, 6657, 3749, 2637],
                [1072, 4201, 2839, 8048, 3669, 6560],
                [9038, 4014, 3476, 1678, 3512, 2813],
                [9143, 1388, 4419, 1622, 9125, 3647],
                [4135, 7157, 971, 1160, 399, 9084],
                [1538, 696, 7137, 3255, 766, 3859],
                [4276, 4201, 4738, 8033, 2813, 604],
            ]

        def win_prob(a: float, b: float) -> float:
            return 1 / (1 + (10 ** (((-5 / 8) * (a - b)) / 29.36)))

        def rp_prob(a: float) -> float:
            return 1 / (1 + 2.71828 ** (-4 * (a - 0.5)))

        matches = []
        for i, x in enumerate(_matches):
            red_epa_pred = sum(team_dict[a].total_epa for a in x[0:3])
            blue_epa_pred = sum(team_dict[a].total_epa for a in x[3:6])
            curr_win_prob = win_prob(red_epa_pred, blue_epa_pred)
            pred_winner = "red" if curr_win_prob > 0.5 else "blue"

            matches.append(
                APIMatch(
                    year=year.year,
                    event=event.key,
                    time=0,
                    predicted_time=0,
                    key=f"qm{i+1}",
                    match_name=f"Qual {i+1}",
                    status="Upcoming",
                    video=None,
                    comp_level="qm",
                    set_number=1,
                    match_number=i + 1,
                    playoff=False,
                    red=[x[0], x[1], x[2]],
                    blue=[x[3], x[4], x[5]],
                    red_surrogates=[x[0]] if i == 17 or i == 18 else [],
                    blue_surrogates=[x[3]] if i == 17 or i == 18 else [],
                    red_dqs=[],
                    blue_dqs=[],
                    red_score=0,
                    red_auto=0,
                    red_teleop=0,
                    red_endgame=0,
                    red_1=0,
                    red_2=0,
                    red_fouls=0,
                    red_rp_1=0,
                    red_rp_2=0,
                    red_tiebreaker=0,
                    blue_score=0,
                    blue_auto=0,
                    blue_teleop=0,
                    blue_endgame=0,
                    blue_1=0,
                    blue_2=0,
                    blue_fouls=0,
                    blue_rp_1=0,
                    blue_rp_2=0,
                    blue_tiebreaker=0,
                    winner="",
                    red_epa_pred=red_epa_pred,
                    red_auto_epa_pred=sum(team_dict[a].auto_epa for a in x[0:3]),
                    red_teleop_epa_pred=sum(team_dict[a].teleop_epa for a in x[0:3]),
                    red_endgame_epa_pred=sum(team_dict[a].endgame_epa for a in x[0:3]),
                    red_rp_1_pred=rp_prob(sum(team_dict[a].rp_1_epa for a in x[0:3])),
                    red_rp_2_pred=rp_prob(sum(team_dict[a].rp_2_epa for a in x[0:3])),
                    blue_epa_pred=blue_epa_pred,
                    blue_auto_epa_pred=sum(team_dict[a].auto_epa for a in x[3:6]),
                    blue_teleop_epa_pred=sum(team_dict[a].teleop_epa for a in x[3:6]),
                    blue_endgame_epa_pred=sum(team_dict[a].endgame_epa for a in x[3:6]),
                    blue_rp_1_pred=rp_prob(sum(team_dict[a].rp_1_epa for a in x[3:6])),
                    blue_rp_2_pred=rp_prob(sum(team_dict[a].rp_2_epa for a in x[3:6])),
                    epa_win_prob=curr_win_prob,
                    pred_winner=pred_winner,
                )
            )

        team_matches: List[APITeamMatch] = []
        for i, x in enumerate(_matches):
            for j, y in enumerate(x):
                team_matches.append(
                    APITeamMatch(
                        num=y,
                        alliance="red" if j < 3 else "blue",
                        match=matches[i].key,
                        time=0,
                        playoff=False,
                        match_number=i + 1,
                        total_epa=team_dict[y].total_epa,
                        auto_epa=team_dict[y].auto_epa,
                        teleop_epa=team_dict[y].teleop_epa,
                        endgame_epa=team_dict[y].endgame_epa,
                        rp_1_epa=team_dict[y].rp_1_epa,
                        rp_2_epa=team_dict[y].rp_2_epa,
                        post_epa=None,
                        offseason=False,
                        status="Upcoming",
                    )
                )

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
