from typing import Any, Dict, List, Tuple, cast, Optional

from src.db.models.alliance import Alliance
from src.db.models.match import Match, create_match_obj
from src.db.models.team_match import TeamMatch, create_team_match_obj
from src.tba.breakdown import Breakdown


def match_dict_to_objs(
    data: Dict[str, Any]
) -> Tuple[Match, List[Alliance], List[TeamMatch]]:
    data["playoff"] = data["comp_level"] != "qm"

    red_no_foul_points = data["red_score_breakdown"]["no_foul_points"]
    red_rp_1 = data["red_score_breakdown"]["rp1"]
    red_rp_2 = data["red_score_breakdown"]["rp2"]
    red_tiebreaker = data["red_score_breakdown"]["tiebreaker"]

    blue_no_foul_points = data["blue_score_breakdown"]["no_foul_points"]
    blue_rp_1 = data["blue_score_breakdown"]["rp1"]
    blue_rp_2 = data["blue_score_breakdown"]["rp2"]
    blue_tiebreaker = data["blue_score_breakdown"]["tiebreaker"]

    match = create_match_obj(
        key=data["key"],
        year=data["year"],
        event=data["event"],
        offseason=data["offseason"],
        week=data["week"],
        playoff=data["playoff"],
        comp_level=data["comp_level"],
        set_number=data["set_number"],
        match_number=data["match_number"],
        time=data["time"],
        predicted_time=data["predicted_time"],
        status=data["status"],
        video=data["video"],
        red_1=data["red_1"],
        red_2=data["red_2"],
        red_3=data["red_3"],
        red_dq=data["red_dq"],
        red_surrogate=data["red_surrogate"],
        blue_1=data["blue_1"],
        blue_2=data["blue_2"],
        blue_3=data["blue_3"],
        blue_dq=data["blue_dq"],
        blue_surrogate=data["blue_surrogate"],
        winner=data["winner"],
        red_score=data["red_score"],
        red_no_foul=red_no_foul_points,
        red_rp_1=red_rp_1,
        red_rp_2=red_rp_2,
        red_tiebreaker=red_tiebreaker,
        blue_score=data["blue_score"],
        blue_no_foul=blue_no_foul_points,
        blue_rp_1=blue_rp_1,
        blue_rp_2=blue_rp_2,
        blue_tiebreaker=blue_tiebreaker,
    )

    alliances: List[Alliance] = []
    team_matches: List[TeamMatch] = []

    for alliance in ["red", "blue"]:
        breakdown: Breakdown = data[f"{alliance}_score_breakdown"]

        alliances.append(
            Alliance(
                id=None,
                alliance=alliance,
                match=cast(str, data["key"]),
                year=cast(int, data["year"]),
                event=cast(str, data["event"]),
                offseason=cast(bool, data["offseason"]),
                week=cast(int, data["week"]),
                playoff=cast(bool, data["playoff"]),
                comp_level=cast(str, data["comp_level"]),
                set_number=cast(int, data["set_number"]),
                match_number=cast(int, data["match_number"]),
                time=cast(int, data["time"]),
                status=cast(str, data["status"]),
                team_1=cast(str, data[f"{alliance}_1"]),
                team_2=cast(str, data[f"{alliance}_2"]),
                team_3=cast(Optional[str], data[f"{alliance}_3"]),
                dq=cast(str, data[f"{alliance}_dq"]),
                surrogate=cast(str, data[f"{alliance}_surrogate"]),
                winner=cast(Optional[str], data["winner"]),
                score=cast(Optional[int], data[f"{alliance}_score"]),
                no_foul_points=breakdown["no_foul_points"],
                foul_points=breakdown["foul_points"],
                auto_points=breakdown["auto_points"],
                teleop_points=breakdown["teleop_points"],
                endgame_points=breakdown["endgame_points"],
                rp_1=breakdown["rp1"],
                rp_2=breakdown["rp2"],
                tiebreaker=breakdown["tiebreaker"],
                comp_1=breakdown["comp_1"],
                comp_2=breakdown["comp_2"],
                comp_3=breakdown["comp_3"],
                comp_4=breakdown["comp_4"],
                comp_5=breakdown["comp_5"],
                comp_6=breakdown["comp_6"],
                comp_7=breakdown["comp_7"],
                comp_8=breakdown["comp_8"],
                comp_9=breakdown["comp_9"],
                comp_10=breakdown["comp_10"],
            )
        )

        teams = [data[f"{alliance}_1"], data[f"{alliance}_2"], data[f"{alliance}_3"]]
        teams = [team for team in teams if team is not None]
        for team in teams:
            team = team
            dq = team in data[f"{alliance}_dq"].split(",")
            surrogate = team in data[f"{alliance}_surrogate"].split(",")
            team_matches.append(
                create_team_match_obj(
                    team=team,
                    year=data["year"],
                    event=data["event"],
                    match=data["key"],
                    alliance=alliance,
                    time=data["time"],
                    offseason=data["offseason"],
                    week=data["week"],
                    playoff=data["playoff"],
                    dq=dq,
                    surrogate=surrogate,
                    status=data["status"],
                )
            )

    return (match, alliances, team_matches)
