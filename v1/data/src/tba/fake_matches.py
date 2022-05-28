import random
from typing import Any, Dict, List


def generate_match(
    event: str,
    comp_level: str,
    set_number: int,
    match_number: int,
    red_teams: List[int],
    blue_teams: List[int],
) -> Dict[str, Any]:
    key = f"{event}_{comp_level}{set_number}m{match_number}"
    if comp_level == "qm":
        key = f"{event}_{comp_level}{match_number}"
    match = {
        "key": key,
        "event": event,
        "comp_level": comp_level,
        "set_number": set_number,
        "match_number": match_number,
        "score_breakdown": {"red": None, "blue": None},
        "alliances": {
            "red": {
                "team_keys": [f"frc{t}" for t in red_teams],
                "score": -1,
            },
            "blue": {
                "team_keys": [f"frc{t}" for t in blue_teams],
                "score": -1,
            },
        },
    }

    return match


def generate_schedule(
    event: str, teams: List[int], matches_per_team: int = 12
) -> List[Dict[str, Any]]:
    num_matches = round(len(teams) * matches_per_team / 6)
    matches: List[Dict[str, Any]] = []
    for i in range(num_matches):
        _match_teams = random.sample(teams, 6)
        match = generate_match(
            event, "qm", 1, i + 1, _match_teams[:3], _match_teams[3:]
        )
        matches.append(match)
    return matches


def generate_elim_schedule(event: str, teams: List[int]) -> List[Dict[str, Any]]:
    elim_teams = random.sample(teams, 24)
    elim_alliances = [elim_teams[3 * i : 3 * (i + 1)] for i in range(8)]
    matches: List[Dict[str, Any]] = []
    for i in range(4):
        _match_teams = elim_alliances[2 * i] + elim_alliances[2 * i + 1]
        match = generate_match(event, "qf", i, 1, _match_teams[:3], _match_teams[3:])
        matches.append(match)
        match = generate_match(event, "qf", i, 2, _match_teams[:3], _match_teams[3:])
        matches.append(match)

    for i in range(2):
        _match_teams = elim_alliances[4 * i] + elim_alliances[4 * i + 2]
        match = generate_match(event, "sf", i, 1, _match_teams[:3], _match_teams[3:])
        matches.append(match)
        match = generate_match(event, "sf", i, 2, _match_teams[:3], _match_teams[3:])
        matches.append(match)

    _match_teams = elim_alliances[0] + elim_alliances[4]
    matches.append(generate_match(event, "f", 1, 1, _match_teams[:3], _match_teams[3:]))
    matches.append(generate_match(event, "f", 1, 2, _match_teams[:3], _match_teams[3:]))
    matches.append(generate_match(event, "f", 1, 3, _match_teams[:3], _match_teams[3:]))

    return matches


def fake_scores(match: Dict[str, Any]):
    match["alliances"]["red"]["score"] = random.randint(20, 40)
    match["alliances"]["blue"]["score"] = random.randint(20, 40)
    red_auto, red_endgame = random.randint(0, 10), random.randint(0, 10)
    red_teleop = match["alliances"]["red"]["score"] - red_auto - red_endgame
    blue_auto, blue_endgame = random.randint(0, 10), random.randint(0, 10)
    blue_teleop = match["alliances"]["blue"]["score"] - blue_auto - blue_endgame
    match["score_breakdown"] = {
        "red": {
            "autoPoints": red_auto,
            "teleop1Points": red_teleop,
            "endgamePoints": red_endgame,
        },
        "blue": {
            "autoPoints": blue_auto,
            "teleop1Points": blue_teleop,
            "endgamePoints": blue_endgame,
        },
    }
    return match


def schedule_release(event: str, teams: List[int], matches_per_team: int = 12):
    return generate_schedule(event, teams, matches_per_team)


def quals_in_progress(
    event: str, teams: List[int], matches_per_team: int = 12, last_qual: int = 0
):
    matches = generate_schedule(event, teams, matches_per_team)
    for i in range(0, last_qual):
        matches[i] = fake_scores(matches[i])
    return matches


def quals_complete(event: str, teams: List[int], matches_per_team: int = 12):
    matches = quals_in_progress(
        event, teams, matches_per_team, round(len(teams) * matches_per_team / 6)
    )
    matches.extend(generate_elim_schedule(event, teams))
    return matches


def elims_in_progress(
    event: str, teams: List[int], matches_per_team: int = 12, last_elim: int = 0
):
    matches = quals_complete(event, teams, matches_per_team)
    num_quals = round(len(teams) * matches_per_team / 6)
    for i in range(num_quals, num_quals + last_elim):
        matches[i] = fake_scores(matches[i])
    return matches


def elims_complete(event: str, teams: List[int], matches_per_team: int = 12):
    return elims_in_progress(event, teams, matches_per_team, 15)
