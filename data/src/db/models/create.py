from typing import Any, Dict, List, Tuple

from db.models.event import Event
from db.models.match import Match
from db.models.team import Team
from db.models.team_event import TeamEvent
from db.models.team_match import TeamMatch
from db.models.team_year import TeamYear
from db.models.year import Year


def create_team_obj(data: Dict[str, Any]) -> Team:
    return Team.from_dict(data)


def create_year_obj(data: Dict[str, Any]) -> Year:
    return Year.from_dict(data)


def create_team_year_obj(data: Dict[str, Any]) -> TeamYear:
    return TeamYear.from_dict(data)


def create_event_obj(data: Dict[str, Any]) -> Event:
    return Event.from_dict(data)


def create_team_event_obj(data: Dict[str, Any]) -> TeamEvent:
    return TeamEvent.from_dict(data)


def create_match_obj(data: Dict[str, Any]) -> Tuple[Match, List[TeamMatch]]:
    data["playoff"] = 0 if data["comp_level"] == "qm" else 1
    data["red_auto"] = data["red_score_breakdown"]["auto"]
    data["red_auto_movement"] = data["red_score_breakdown"]["auto_movement"]
    data["red_auto_1"] = data["red_score_breakdown"]["auto_1"]
    data["red_auto_2"] = data["red_score_breakdown"]["auto_2"]
    data["red_teleop_1"] = data["red_score_breakdown"]["teleop_1"]
    data["red_teleop_2"] = data["red_score_breakdown"]["teleop_2"]
    data["red_1"] = data["red_score_breakdown"]["1"]
    data["red_2"] = data["red_score_breakdown"]["2"]
    data["red_teleop"] = data["red_score_breakdown"]["teleop"]
    data["red_endgame"] = data["red_score_breakdown"]["endgame"]
    data["red_no_fouls"] = data["red_score_breakdown"]["no_fouls"]
    data["red_fouls"] = data["red_score_breakdown"]["fouls"]
    data["red_rp_1"] = data["red_score_breakdown"]["rp1"]
    data["red_rp_2"] = data["red_score_breakdown"]["rp2"]
    data["blue_auto"] = data["blue_score_breakdown"]["auto"]
    data["blue_auto_movement"] = data["blue_score_breakdown"]["auto_movement"]
    data["blue_auto_1"] = data["blue_score_breakdown"]["auto_1"]
    data["blue_auto_2"] = data["blue_score_breakdown"]["auto_2"]
    data["blue_teleop_1"] = data["blue_score_breakdown"]["teleop_1"]
    data["blue_teleop_2"] = data["blue_score_breakdown"]["teleop_2"]
    data["blue_1"] = data["blue_score_breakdown"]["1"]
    data["blue_2"] = data["blue_score_breakdown"]["2"]
    data["blue_teleop"] = data["blue_score_breakdown"]["teleop"]
    data["blue_endgame"] = data["blue_score_breakdown"]["endgame"]
    data["blue_no_fouls"] = data["blue_score_breakdown"]["no_fouls"]
    data["blue_fouls"] = data["blue_score_breakdown"]["fouls"]
    data["blue_rp_1"] = data["blue_score_breakdown"]["rp1"]
    data["blue_rp_2"] = data["blue_score_breakdown"]["rp2"]
    match = Match.from_dict(data)

    team_matches: List[TeamMatch] = []
    new_data = {"match": data["key"], **data}

    for alliance in ["red", "blue"]:
        new_data["alliance"] = alliance
        for team in data[alliance].split(","):
            new_data["team"] = int(team)
            team_matches.append(create_team_match_obj(new_data))

    return (match, team_matches)


def create_team_match_obj(data: Dict[str, Any]) -> TeamMatch:
    return TeamMatch.from_dict(data)
