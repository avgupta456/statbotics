from typing import Any, Dict, List, Tuple

from db.models.event import Event
from db.models.match import Match
from db.models.team import Team
from db.models.team_event import TeamEvent
from db.models.team_match import TeamMatch
from db.models.team_year import TeamYear
from db.models.year import Year
from db.read.event import get_num_events
from db.read.match import get_num_matches
from helper.utils import get_team_event_id, get_team_match_id, get_team_year_id

event_id = -1
match_id = -1


def create_team_obj(data: Dict[str, Any]) -> Team:
    data["team"] = data["number"]
    return Team.from_dict(data)


def create_year_obj(data: Dict[str, Any]) -> Year:
    return Year.from_dict(data)


def create_team_year_obj(data: Dict[str, Any]) -> TeamYear:
    team, year = data["team"], data["year"]
    id = get_team_year_id(team, year)
    return TeamYear.from_dict({"id": id, "year": year, "team": team, **data})


def create_event_obj(data: Dict[str, Any]) -> Event:
    global event_id
    if event_id < 0:
        event_id = get_num_events()
    event_id += 1

    data["id"] = event_id
    data["district"] = data["district"] or "None"
    return Event.from_dict(data)


def create_team_event_obj(data: Dict[str, Any]) -> TeamEvent:
    data["id"] = get_team_event_id(data["team"], data["event_id"])
    data["team_year_id"] = get_team_year_id(data["team"], data["year"])
    return TeamEvent.from_dict(data)


def create_match_obj(data: Dict[str, Any]) -> Tuple[Match, List[TeamMatch]]:
    global match_id
    if match_id < 0:
        match_id = get_num_matches()
    match_id += 1

    data["id"] = match_id
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
    new_data = {
        "year": data["year"],
        "event_id": data["event_id"],
        "match_id": match_id,
        "time": data["time"],
        "playoff": data["playoff"],
    }

    for alliance in ["red", "blue"]:
        new_data["alliance"] = alliance
        for team in data[alliance].split(","):
            new_data["team"] = int(team)
            new_data["team_year_id"] = get_team_year_id(team, data["year"])
            new_data["team_event_id"] = get_team_event_id(team, data["event_id"])
            team_matches.append(create_team_match_obj(new_data))

    return (match, team_matches)


def create_team_match_obj(data: Dict[str, Any]) -> TeamMatch:
    data["id"] = get_team_match_id(data["team"], data["match_id"])
    return TeamMatch.from_dict(data)
