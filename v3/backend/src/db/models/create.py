from typing import List, Tuple

from src.db.models.alliance import Alliance
from src.db.models.match import Match
from src.db.models.team_match import TeamMatch
from src.tba.read_tba import MatchDict


def match_dict_to_objs(
    data: MatchDict, year: int, week: int, offseason: bool
) -> Tuple[Match, List[Alliance], List[TeamMatch]]:
    elim = data["comp_level"] != "qm"

    red_breakdown = data["red_score_breakdown"]
    blue_breakdown = data["blue_score_breakdown"]

    match = Match(
        key=data["key"],
        year=year,
        event=data["event"],
        offseason=offseason,
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
        red_rp_1=red_breakdown["rp_1"],
        red_rp_2=red_breakdown["rp_2"],
        red_tiebreaker=red_breakdown["tiebreaker"],
        blue_score=data["blue_score"],
        blue_no_foul=blue_breakdown["no_foul_points"],
        blue_rp_1=blue_breakdown["rp_1"],
        blue_rp_2=blue_breakdown["rp_2"],
        blue_tiebreaker=blue_breakdown["tiebreaker"],
    )

    alliances: List[Alliance] = []
    team_matches: List[TeamMatch] = []

    for alliance in ["red", "blue"]:
        breakdown = (
            data["red_score_breakdown"]
            if alliance == "red"
            else data["blue_score_breakdown"]
        )

        team_1 = data["red_1"] if alliance == "red" else data["blue_1"]
        team_2 = data["red_2"] if alliance == "red" else data["blue_2"]
        team_3 = data["red_3"] if alliance == "red" else data["blue_3"]
        dq = data["red_dq"] if alliance == "red" else data["blue_dq"]
        surrogate = (
            data["red_surrogate"] if alliance == "red" else data["blue_surrogate"]
        )
        score = data["red_score"] if alliance == "red" else data["blue_score"]

        alliances.append(
            Alliance(
                id=None,
                alliance=alliance,
                match=data["key"],
                year=year,
                event=data["event"],
                offseason=offseason,
                week=week,
                elim=elim,
                time=data["time"],
                status=data["status"],
                team_1=team_1,
                team_2=team_2,
                team_3=team_3,
                dq=dq,
                surrogate=surrogate,
                official_winner=data["official_winner"],
                winner=data["winner"],
                score=score,
                no_foul=breakdown["no_foul_points"],
                foul=breakdown["foul_points"],
                auto=breakdown["auto_points"],
                teleop=breakdown["teleop_points"],
                endgame=breakdown["endgame_points"],
                rp_1=breakdown["rp_1"],
                rp_2=breakdown["rp_2"],
                tiebreaker=breakdown["tiebreaker"],
                match_comp_1=breakdown["match_comp_1"],
                match_comp_2=breakdown["match_comp_2"],
                match_comp_3=breakdown["match_comp_3"],
                match_comp_4=breakdown["match_comp_4"],
                match_comp_5=breakdown["match_comp_5"],
                match_comp_6=breakdown["match_comp_6"],
                match_comp_7=breakdown["match_comp_7"],
                match_comp_8=breakdown["match_comp_8"],
                match_comp_9=breakdown["match_comp_9"],
                match_comp_10=breakdown["match_comp_10"],
                match_comp_11=breakdown["match_comp_11"],
                match_comp_12=breakdown["match_comp_12"],
            )
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
                    offseason=offseason,
                    week=week,
                    elim=elim,
                    dq=team in dq.split(","),
                    surrogate=team in surrogate.split(","),
                    status=data["status"],
                )
            )

    return (match, alliances, team_matches)
