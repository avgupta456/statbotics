import random
from typing import Any, Dict, List, Optional

from src.tba.main import get_tba

# 2023 Week 1 events
completed_mock_events = [
    "2023isde1",
    "2023isde2",
    "2023bcvi",
    "2023utwv",
    "2023txwac",
    "2023orore",
    "2023nhgrs",
    "2023mxmo",
    "2023mndu2",
    "2023mndu",
    "2023mimil",
    "2023miket",
    "2023mijac",
    "2023mifor",
    "2023miesc",
    "2023gaalb",
    "2023flwp",
    "2023arli",
    "2023wasno",
    "2023valba",
    "2023txdal",
    "2023tuis3",
    "2023pahat",
    "2023onnew",
    "2023onbar",
    "2023ncash",
    "2023mabri",
    "2023inmis",
    "2023caph",
]

# 2023 Week 2 events
ongoing_mock_events = [
    "2023txbel",
    "2023orwil",
    "2023okok",
    "2023ndgf",
    "2023mosl",
    "2023misjo",
    "2023milan",
    "2023mike2",
    "2023ilch",
    "2023gadal",
    "2023txcha",
    "2023tume",
    "2023scand",
    "2023rinsc",
    "2023njfla",
    "2023ncjoh",
    "2023midtr",
    "2023mdbet",
    "2023inpri",
    "2023ctwat",
    # So that some week 2 events are upcoming
    # "2023cave",
    # "2023caoc",
    # "2023cafr",
    # "2023ausc",
    # "2023isde3",
]

all_mock_events = completed_mock_events + ongoing_mock_events

# Mock index mapping:
# 0: Schedule Release
# 1-3: Qualification Matches
# 4: Alliance Selection
# 5: Elimination Schedule Release
# 6: Elimination Matches
# 7: Event Completed


# Copied and modified from read_tba.py to prevent circular dependency
def _get_event_teams(event: str) -> List[int]:
    query_str = "event/" + str(event) + "/teams/simple"
    data, _ = get_tba(query_str, etag=None, cache=True)
    if type(data) is bool:
        return []
    out = [int(x["team_number"]) for x in data]
    return out


# Copied and modified from clean_data.py
def _get_breakdown(score: int) -> Dict[str, Optional[int]]:
    if score == 0:
        return {
            "auto": None,
            "auto_movement": None,
            "auto_1": None,
            "auto_2": None,
            "auto_2_1": None,
            "auto_2_2": None,
            "teleop_1": None,
            "teleop_2": None,
            "teleop_2_1": None,
            "teleop_2_2": None,
            "1": None,
            "2": None,
            "teleop": None,
            "endgame": None,
            "no_fouls": None,
            "fouls": None,
            "rp1": None,
            "rp2": None,
        }

    auto = random.randint(0, 10)
    endgame = random.randint(0, 10)
    teleop = score - auto - endgame
    return {
        "auto": auto,
        "auto_movement": 0,
        "auto_1": auto,
        "auto_2": 0,
        "auto_2_1": 0,
        "auto_2_2": 0,
        "teleop_1": teleop,
        "teleop_2": 0,
        "teleop_2_1": 0,
        "teleop_2_2": 0,
        "1": auto + teleop,
        "2": 0,
        "teleop": teleop,
        "endgame": endgame,
        "no_fouls": score,
        "fouls": 0,
        "rp1": random.randint(0, 1),
        "rp2": random.randint(0, 1),
    }


def _create_match(
    event: str,
    event_time: int,
    teams: List[int],
    i: int,
    completed: bool,
    key: str,
    comp_level: str,
    set_number: int,
    match_number: int,
) -> Dict[str, Any]:
    red_score = 0
    blue_score = 0
    if completed:
        red_score = random.randint(10, 100)
        blue_score = random.randint(10, 100)

    red_breakdown = _get_breakdown(red_score)
    blue_breakdown = _get_breakdown(blue_score)

    winner = (
        "red"
        if red_score > blue_score
        else ("blue" if blue_score > red_score else "draw")
    )

    return {
        "event": event,
        "key": key,
        "comp_level": comp_level,
        "set_number": set_number,
        "match_number": match_number,
        "status": "Completed" if completed else "Upcoming",
        "video": None,
        "red_1": teams[(7 * i + 0) % len(teams)],
        "red_2": teams[(7 * i + 1) % len(teams)],
        "red_3": teams[(7 * i + 2) % len(teams)],
        "blue_1": teams[(7 * i + 3) % len(teams)],
        "blue_2": teams[(7 * i + 4) % len(teams)],
        "blue_3": teams[(7 * i + 5) % len(teams)],
        "red_dq": "",
        "blue_dq": "",
        "red_surrogate": "",
        "blue_surrogate": "",
        "winner": winner,
        "time": event_time + i + 1,
        "red_score": red_score,
        "blue_score": blue_score,
        "red_score_breakdown": red_breakdown,
        "blue_score_breakdown": blue_breakdown,
    }


def get_event_rankings(event: str, mock_index: int) -> Dict[int, int]:
    teams = _get_event_teams(event)
    rankings: Dict[int, int] = {}
    for i, team in enumerate(teams):
        rankings[team] = i + 1
    return rankings


def get_matches(
    year: int, event: str, event_time: int, mock_index: int
) -> List[Dict[str, Any]]:
    teams = _get_event_teams(event)

    """QUALS"""

    N = len(teams) * 2  # 12 matches per team (6 teams per match)
    n = N if event in completed_mock_events else round(N * min(1, mock_index / 4))

    # For testing incremental update
    if mock_index == 1:
        n = 1

    match_data: List[Dict[str, Any]] = []
    for i in range(N):
        match_data.append(
            _create_match(
                event, event_time, teams, i, i < n, f"{event}_qm{i+1}", "qm", 1, i + 1
            )
        )

    """ELIMS"""

    # Quarters
    completed_quarters = event in completed_mock_events or mock_index >= 6
    if event in completed_mock_events or mock_index >= 5:
        for i in range(4):
            for j in range(2):
                match_data.append(
                    _create_match(
                        event,
                        event_time,
                        teams,
                        300 + 10 * (i + 1) + j + 1,
                        completed_quarters,
                        f"{event}_qf{i + 1}m{j + 1}",
                        "qf",
                        i + 1,
                        j + 1,
                    )
                )

    # Semis
    completed_semis = event in completed_mock_events or mock_index >= 6
    if event in completed_mock_events or mock_index >= 6:
        for i in range(2):
            for j in range(2):
                match_data.append(
                    _create_match(
                        event,
                        event_time,
                        teams,
                        400 + 10 * (i + 1) + j + 1,
                        completed_semis,
                        f"{event}_sf{i + 1}m{j + 1}",
                        "sf",
                        i + 1,
                        j + 1,
                    )
                )

    # Finals
    completed_finals = event in completed_mock_events or mock_index >= 7
    if event in completed_mock_events or mock_index >= 6:
        for i in range(2):
            match_data.append(
                _create_match(
                    event,
                    event_time,
                    teams,
                    500 + i,
                    completed_finals,
                    f"{event}_f1m{i + 1}",
                    "f",
                    1,
                    i + 1,
                )
            )

    return match_data
