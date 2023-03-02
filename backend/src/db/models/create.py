from typing import Any, Dict, List, Tuple

from src.db.models.etag import ETag
from src.db.models.event import Event
from src.db.models.match import Match
from src.db.models.team import Team
from src.db.models.team_event import TeamEvent
from src.db.models.team_match import TeamMatch
from src.db.models.team_year import TeamYear
from src.db.models.year import Year


def create_team_obj(data: Dict[str, Any]) -> Team:
    data["wins"] = 0
    data["losses"] = 0
    data["ties"] = 0
    data["count"] = 0
    data["full_wins"] = 0
    data["full_losses"] = 0
    data["full_ties"] = 0
    data["full_count"] = 0
    return Team.from_dict(data)


def create_year_obj(data: Dict[str, Any]) -> Year:
    return Year.from_dict(data)


def create_team_year_obj(data: Dict[str, Any]) -> TeamYear:
    data["wins"] = 0
    data["losses"] = 0
    data["ties"] = 0
    data["count"] = 0
    data["full_wins"] = 0
    data["full_losses"] = 0
    data["full_ties"] = 0
    data["full_count"] = 0
    return TeamYear.from_dict(data)


def create_event_obj(data: Dict[str, Any]) -> Event:
    data["offseason"] = data["type"] > 10
    return Event.from_dict(data)


def create_team_event_obj(data: Dict[str, Any]) -> TeamEvent:
    data["wins"] = 0
    data["losses"] = 0
    data["ties"] = 0
    data["count"] = 0
    data["qual_wins"] = 0
    data["qual_losses"] = 0
    data["qual_ties"] = 0
    data["qual_count"] = 0
    return TeamEvent.from_dict(data)


def create_match_obj(data: Dict[str, Any]) -> Tuple[Match, List[TeamMatch]]:
    data["playoff"] = data["comp_level"] != "qm"
    data["red_auto"] = data["red_score_breakdown"]["auto"]
    data["red_auto_movement"] = data["red_score_breakdown"]["auto_movement"]
    data["red_auto_1"] = data["red_score_breakdown"]["auto_1"]
    data["red_auto_2"] = data["red_score_breakdown"]["auto_2"]
    data["red_auto_2_1"] = data["red_score_breakdown"]["auto_2_1"]
    data["red_auto_2_2"] = data["red_score_breakdown"]["auto_2_2"]
    data["red_teleop_1"] = data["red_score_breakdown"]["teleop_1"]
    data["red_teleop_2"] = data["red_score_breakdown"]["teleop_2"]
    data["red_teleop_2_1"] = data["red_score_breakdown"]["teleop_2_1"]
    data["red_teleop_2_2"] = data["red_score_breakdown"]["teleop_2_2"]
    data["red_teleop"] = data["red_score_breakdown"]["teleop"]
    data["red_endgame"] = data["red_score_breakdown"]["endgame"]
    data["red_no_fouls"] = data["red_score_breakdown"]["no_fouls"]
    data["red_fouls"] = data["red_score_breakdown"]["fouls"]
    data["red_rp_1"] = data["red_score_breakdown"]["rp1"]
    data["red_rp_2"] = data["red_score_breakdown"]["rp2"]
    data["red_tiebreaker"] = data["red_score_breakdown"]["tiebreaker"]
    data["blue_auto"] = data["blue_score_breakdown"]["auto"]
    data["blue_auto_movement"] = data["blue_score_breakdown"]["auto_movement"]
    data["blue_auto_1"] = data["blue_score_breakdown"]["auto_1"]
    data["blue_auto_2"] = data["blue_score_breakdown"]["auto_2"]
    data["blue_auto_2_1"] = data["blue_score_breakdown"]["auto_2_1"]
    data["blue_auto_2_2"] = data["blue_score_breakdown"]["auto_2_2"]
    data["blue_teleop_1"] = data["blue_score_breakdown"]["teleop_1"]
    data["blue_teleop_2"] = data["blue_score_breakdown"]["teleop_2"]
    data["blue_teleop_2_1"] = data["blue_score_breakdown"]["teleop_2_1"]
    data["blue_teleop_2_2"] = data["blue_score_breakdown"]["teleop_2_2"]
    data["blue_teleop"] = data["blue_score_breakdown"]["teleop"]
    data["blue_endgame"] = data["blue_score_breakdown"]["endgame"]
    data["blue_no_fouls"] = data["blue_score_breakdown"]["no_fouls"]
    data["blue_fouls"] = data["blue_score_breakdown"]["fouls"]
    data["blue_rp_1"] = data["blue_score_breakdown"]["rp1"]
    data["blue_rp_2"] = data["blue_score_breakdown"]["rp2"]
    data["blue_tiebreaker"] = data["blue_score_breakdown"]["tiebreaker"]
    match = Match.from_dict(data)

    team_matches: List[TeamMatch] = []
    new_data = {"match": data["key"], **data}

    for alliance in ["red", "blue"]:
        new_data["alliance"] = alliance
        teams = [data[f"{alliance}_1"], data[f"{alliance}_2"], data[f"{alliance}_3"]]
        teams = [team for team in teams if team is not None]
        for team in teams:
            new_data["team"] = team
            new_data["dq"] = team in data[f"{alliance}_dq"].split(",")
            new_data["surrogate"] = team in data[f"{alliance}_surrogate"].split(",")
            team_matches.append(create_team_match_obj(new_data))

    return (match, team_matches)


def create_team_match_obj(data: Dict[str, Any]) -> TeamMatch:
    return TeamMatch.from_dict(data)


def create_etag_obj(path: str, etag: str) -> ETag:
    return ETag.from_dict({"path": path, "etag": etag})
