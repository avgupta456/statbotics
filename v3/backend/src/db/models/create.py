from typing import Any, Dict, List, Tuple

from src.db.models.alliance import Alliance, create_alliance_obj
from src.db.models.match import Match, create_match_obj
from src.db.models.team_match import TeamMatch, create_team_match_obj


def match_dict_to_objs(
    data: Dict[str, Any]
) -> Tuple[Match, List[Alliance], List[TeamMatch]]:
    data["playoff"] = data["comp_level"] != "qm"

    data["red_no_foul"] = data["red_score_breakdown"]["no_foul_points"]
    data["red_rp_1"] = data["red_score_breakdown"]["rp1"]
    data["red_rp_2"] = data["red_score_breakdown"]["rp2"]
    data["red_tiebreaker"] = data["red_score_breakdown"]["tiebreaker"]

    data["blue_no_foul"] = data["blue_score_breakdown"]["no_foul_points"]
    data["blue_rp_1"] = data["blue_score_breakdown"]["rp1"]
    data["blue_rp_2"] = data["blue_score_breakdown"]["rp2"]
    data["blue_tiebreaker"] = data["blue_score_breakdown"]["tiebreaker"]

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
    )

    alliances: List[Alliance] = []
    team_matches: List[TeamMatch] = []

    for alliance in ["red", "blue"]:
        alliances.append(
            create_alliance_obj(
                alliance=alliance,
                match=data["key"],
                year=data["year"],
                event=data["event"],
                offseason=data["offseason"],
                week=data["week"],
                playoff=data["playoff"],
                comp_level=data["comp_level"],
                set_number=data["set_number"],
                match_number=data["match_number"],
                time=data["time"],
                status=data["status"],
                team_1=data[f"{alliance}_1"],
                team_2=data[f"{alliance}_2"],
                team_3=data[f"{alliance}_3"],
                dq=data[f"{alliance}_dq"],
                surrogate=data[f"{alliance}_surrogate"],
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
