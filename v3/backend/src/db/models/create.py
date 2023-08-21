from typing import Any, Dict, List, Optional, Tuple

from src.db.models.alliance import Alliance
from src.db.models.etag import ETag
from src.db.models.event import Event
from src.db.models.match import Match
from src.db.models.team import Team
from src.db.models.team_event import TeamEvent
from src.db.models.team_match import TeamMatch
from src.db.models.team_year import TeamYear
from src.db.models.year import Year


def create_team_obj(
    team: str,
    name: str,
    country: Optional[str],
    state: Optional[str],
    rookie_year: Optional[int],
) -> Team:
    return Team(
        team=team,
        name=name,
        offseason=True,  # overwritten later
        country=country,
        district=None,  # overwritten later
        state=state,
        rookie_year=rookie_year,
        active=False,  # overwritten later
        norm_epa=None,
        norm_epa_recent=None,
        norm_epa_mean=None,
        norm_epa_max=None,
        wins=0,
        losses=0,
        ties=0,
        count=0,
        winrate=0,
        full_wins=0,
        full_losses=0,
        full_ties=0,
        full_count=0,
        full_winrate=0,
    )


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


def create_match_obj(
    data: Dict[str, Any]
) -> Tuple[Match, List[Alliance], List[TeamMatch]]:
    data["playoff"] = data["comp_level"] != "qm"

    data["red_no_foul"] = data["red_score_breakdown"]["no_foul_points"]
    data["red_rp_1"] = data["red_score_breakdown"]["rp1"]
    data["red_rp_2"] = data["red_score_breakdown"]["rp2"]
    data["red_tiebreaker"] = data["red_score_breakdown"]["tiebreaker"]
    """
    data["red_foul_points"] = data["red_score_breakdown"]["foul_points"]
    data["red_auto_points"] = data["red_score_breakdown"]["auto_points"]
    data["red_teleop_points"] = data["red_score_breakdown"]["teleop_points"]
    data["red_endgame_points"] = data["red_score_breakdown"]["endgame_points"]
    data["red_comp_1"] = data["red_score_breakdown"]["comp_1"]
    data["red_comp_2"] = data["red_score_breakdown"]["comp_2"]
    data["red_comp_3"] = data["red_score_breakdown"]["comp_3"]
    data["red_comp_4"] = data["red_score_breakdown"]["comp_4"]
    data["red_comp_5"] = data["red_score_breakdown"]["comp_5"]
    data["red_comp_6"] = data["red_score_breakdown"]["comp_6"]
    data["red_comp_7"] = data["red_score_breakdown"]["comp_7"]
    data["red_comp_8"] = data["red_score_breakdown"]["comp_8"]
    data["red_comp_9"] = data["red_score_breakdown"]["comp_9"]
    data["red_comp_10"] = data["red_score_breakdown"]["comp_10"]
    """

    data["blue_no_foul"] = data["blue_score_breakdown"]["no_foul_points"]
    data["blue_rp_1"] = data["blue_score_breakdown"]["rp1"]
    data["blue_rp_2"] = data["blue_score_breakdown"]["rp2"]
    data["blue_comp_10"] = data["blue_score_breakdown"]["comp_10"]
    """
    data["blue_foul_points"] = data["blue_score_breakdown"]["foul_points"]
    data["blue_auto_points"] = data["blue_score_breakdown"]["auto_points"]
    data["blue_teleop_points"] = data["blue_score_breakdown"]["teleop_points"]
    data["blue_endgame_points"] = data["blue_score_breakdown"]["endgame_points"]
    data["blue_comp_1"] = data["blue_score_breakdown"]["comp_1"]
    data["blue_comp_2"] = data["blue_score_breakdown"]["comp_2"]
    data["blue_comp_3"] = data["blue_score_breakdown"]["comp_3"]
    data["blue_comp_4"] = data["blue_score_breakdown"]["comp_4"]
    data["blue_comp_5"] = data["blue_score_breakdown"]["comp_5"]
    data["blue_comp_6"] = data["blue_score_breakdown"]["comp_6"]
    data["blue_comp_7"] = data["blue_score_breakdown"]["comp_7"]
    data["blue_comp_8"] = data["blue_score_breakdown"]["comp_8"]
    data["blue_comp_9"] = data["blue_score_breakdown"]["comp_9"]
    """

    match = Match.from_dict(data)

    alliances: List[Alliance] = []
    team_matches: List[TeamMatch] = []
    new_data = {"match": data["key"], **data}

    for alliance in ["red", "blue"]:
        new_data["alliance"] = alliance
        teams = [data[f"{alliance}_1"], data[f"{alliance}_2"], data[f"{alliance}_3"]]
        teams = [team for team in teams if team is not None]
        alliances.append(create_alliance_obj(data, alliance))
        for team in teams:
            new_data["team"] = team
            new_data["dq"] = team in data[f"{alliance}_dq"].split(",")
            new_data["surrogate"] = team in data[f"{alliance}_surrogate"].split(",")
            team_matches.append(create_team_match_obj(new_data))

    return (match, alliances, team_matches)


def create_alliance_obj(data: Dict[str, Any], alliance: str) -> Alliance:
    data["match"] = data["key"]
    data["alliance"] = alliance
    data["score"] = data[f"{alliance}_score"]
    data["team_1"] = data[f"{alliance}_1"]
    data["team_2"] = data[f"{alliance}_2"]
    data["team_3"] = data[f"{alliance}_3"]
    data["dq"] = data[f"{alliance}_dq"]
    data["surrogate"] = data[f"{alliance}_surrogate"]
    data["winner"] = data["winner"] == alliance
    return Alliance.from_dict(data)


def create_team_match_obj(data: Dict[str, Any]) -> TeamMatch:
    return TeamMatch.from_dict(data)


def create_etag_obj(path: str, etag: str) -> ETag:
    return ETag.from_dict({"path": path, "etag": etag})
