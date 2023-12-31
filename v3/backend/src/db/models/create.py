from typing import List, Tuple

from src.db.models.alliance import Alliance
from src.db.models.match import Match
from src.db.models.team_match import TeamMatch
from src.tba.read_tba import MatchDict
from src.types.enums import AllianceColor, CompLevel


def match_dict_to_objs(
    data: MatchDict, year: int, week: int, offseason: bool
) -> Tuple[Match, List[Alliance], List[TeamMatch]]:
    elim = data["comp_level"] != CompLevel.QUAL

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
        blue_score=data["blue_score"],
        blue_no_foul=blue_breakdown["no_foul_points"],
        blue_rp_1=blue_breakdown["rp_1"],
        blue_rp_2=blue_breakdown["rp_2"],
    )

    alliances: List[Alliance] = []
    team_matches: List[TeamMatch] = []

    for alliance in [AllianceColor.RED, AllianceColor.BLUE]:
        breakdown = data["red_score_breakdown"]
        team_1, team_2, team_3 = data["red_1"], data["red_2"], data["red_3"]
        dq, surrogate = data["red_dq"], data["red_surrogate"]
        score = data["red_score"]

        if alliance == AllianceColor.BLUE:
            breakdown = data["blue_score_breakdown"]
            team_1, team_2, team_3 = data["blue_1"], data["blue_2"], data["blue_3"]
            dq, surrogate = data["blue_dq"], data["blue_surrogate"]
            score = data["blue_score"]

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
                comp_11=breakdown["comp_11"],
                comp_12=breakdown["comp_12"],
                comp_13=breakdown["comp_13"],
                comp_14=breakdown["comp_14"],
                comp_15=breakdown["comp_15"],
                comp_16=breakdown["comp_16"],
                comp_17=breakdown["comp_17"],
                comp_18=breakdown["comp_18"],
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
