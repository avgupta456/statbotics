from typing import List, Tuple

from src.db.models.match import Match
from src.db.models.team_match import TeamMatch
from src.tba.read_tba import MatchDict
from src.types.enums import CompLevel


def match_dict_to_objs(
    data: MatchDict, year: int, week: int
) -> Tuple[Match, List[TeamMatch]]:
    elim = data["comp_level"] != CompLevel.QUAL

    red_breakdown = data["red_score_breakdown"]
    blue_breakdown = data["blue_score_breakdown"]

    match = Match(
        key=data["key"],
        year=year,
        event=data["event"],
        week=week,
        elim=elim,
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
        red_no_foul=red_breakdown["no_foul_points"],
        red_foul=red_breakdown["foul_points"],
        red_auto=red_breakdown["auto_points"],
        red_teleop=red_breakdown["teleop_points"],
        red_endgame=red_breakdown["endgame_points"],
        red_rp_1=red_breakdown["rp_1"],
        red_rp_2=red_breakdown["rp_2"],
        red_rp_3=red_breakdown["rp_3"],
        red_tiebreaker=red_breakdown["tiebreaker"],
        red_comp_1=red_breakdown["comp_1"],
        red_comp_2=red_breakdown["comp_2"],
        red_comp_3=red_breakdown["comp_3"],
        red_comp_4=red_breakdown["comp_4"],
        red_comp_5=red_breakdown["comp_5"],
        red_comp_6=red_breakdown["comp_6"],
        red_comp_7=red_breakdown["comp_7"],
        red_comp_8=red_breakdown["comp_8"],
        red_comp_9=red_breakdown["comp_9"],
        red_comp_10=red_breakdown["comp_10"],
        red_comp_11=red_breakdown["comp_11"],
        red_comp_12=red_breakdown["comp_12"],
        red_comp_13=red_breakdown["comp_13"],
        red_comp_14=red_breakdown["comp_14"],
        red_comp_15=red_breakdown["comp_15"],
        red_comp_16=red_breakdown["comp_16"],
        red_comp_17=red_breakdown["comp_17"],
        red_comp_18=red_breakdown["comp_18"],
        blue_score=data["blue_score"],
        blue_no_foul=blue_breakdown["no_foul_points"],
        blue_foul=blue_breakdown["foul_points"],
        blue_auto=blue_breakdown["auto_points"],
        blue_teleop=blue_breakdown["teleop_points"],
        blue_endgame=blue_breakdown["endgame_points"],
        blue_rp_1=blue_breakdown["rp_1"],
        blue_rp_2=blue_breakdown["rp_2"],
        blue_rp_3=blue_breakdown["rp_3"],
        blue_tiebreaker=blue_breakdown["tiebreaker"],
        blue_comp_1=blue_breakdown["comp_1"],
        blue_comp_2=blue_breakdown["comp_2"],
        blue_comp_3=blue_breakdown["comp_3"],
        blue_comp_4=blue_breakdown["comp_4"],
        blue_comp_5=blue_breakdown["comp_5"],
        blue_comp_6=blue_breakdown["comp_6"],
        blue_comp_7=blue_breakdown["comp_7"],
        blue_comp_8=blue_breakdown["comp_8"],
        blue_comp_9=blue_breakdown["comp_9"],
        blue_comp_10=blue_breakdown["comp_10"],
        blue_comp_11=blue_breakdown["comp_11"],
        blue_comp_12=blue_breakdown["comp_12"],
        blue_comp_13=blue_breakdown["comp_13"],
        blue_comp_14=blue_breakdown["comp_14"],
        blue_comp_15=blue_breakdown["comp_15"],
        blue_comp_16=blue_breakdown["comp_16"],
        blue_comp_17=blue_breakdown["comp_17"],
        blue_comp_18=blue_breakdown["comp_18"],
    )

    team_matches: List[TeamMatch] = []
    for alliance in ["red", "blue"]:
        team_1 = data["red_1"] if alliance == "red" else data["blue_1"]
        team_2 = data["red_2"] if alliance == "red" else data["blue_2"]
        team_3 = data["red_3"] if alliance == "red" else data["blue_3"]
        dq = data["red_dq"] if alliance == "red" else data["blue_dq"]
        surrogate = (
            data["red_surrogate"] if alliance == "red" else data["blue_surrogate"]
        )

        teams = [team_1, team_2, team_3]
        teams = [team for team in teams if team is not None]
        for team in teams:
            team_matches.append(
                TeamMatch(
                    id=None,
                    team=team,
                    year=year,
                    event=data["event"],
                    match=data["key"],
                    alliance=alliance,
                    time=data["time"],
                    week=week,
                    elim=elim,
                    dq=team in dq.split(","),
                    surrogate=team in surrogate.split(","),
                    status=data["status"],
                )
            )

    return (match, team_matches)
