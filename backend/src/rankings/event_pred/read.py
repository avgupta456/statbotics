from typing import Any, Dict, List, Tuple, Union

from rankings.models import Match, TeamEvent, TeamMatch, Year


def get_year_dict(year: int) -> Tuple[float, float]:
    data: Dict[str, float] = Year.objects.values("score_sd", "score_mean").get(  # type: ignore
        year=year
    )
    return data["score_sd"], data["score_mean"]


def get_teams_dict(
    event_key: str,
) -> Tuple[List[int], Dict[int, Dict[str, Union[int, float]]]]:
    data: List[Dict[str, Union[int, float]]] = (
        TeamEvent.objects.values(  # type: ignore
            "team",
            "elo_start",
            "opr_start",
            "opr_auto",
            "opr_teleop",
            "opr_1",
            "opr_2",
            "opr_endgame",
            "opr_fouls",
            "opr_no_fouls",
            "ils_1_start",
            "ils_2_start",
        )
        .filter(event=event_key)
        .all()
    )

    out: List[int] = []
    stats: Dict[int, Dict[str, Union[int, float]]] = {}
    for entry in data:
        team: int = int(entry["team"])
        out.append(team)
        stats[team] = entry
    return out, stats


def get_matches_dict(event_key: str) -> List[Dict[str, Any]]:
    data: List[Dict[str, Any]] = (
        Match.objects.values(  # type: ignore
            "key",
            "winner",
            "elo_win_prob",
            "opr_win_prob",
            "mix_win_prob",
            "red_rp_1_prob",
            "red_rp_2_prob",
            "blue_rp_1_prob",
            "blue_rp_2_prob",
            "red_score",
            "blue_score",
            "red_rp_1",
            "red_rp_2",
            "blue_rp_1",
            "blue_rp_2",
            "red_1",
            "blue_1",
            "red_2",
            "blue_2",
            "red_auto",
            "blue_auto",
            "red_teleop",
            "blue_teleop",
            "red_endgame",
            "blue_endgame",
            "red_fouls",
            "blue_fouls",
            "red_no_fouls",
            "blue_no_fouls",
            "red",
            "blue",
        )
        .filter(event=event_key, playoff=0)
        .order_by("time")
    )

    out: List[Dict[str, Any]] = []
    for entry in data:
        out.append(entry)
        out[-1]["red"] = [int(x) for x in out[-1]["red"].split(",")]
        out[-1]["blue"] = [int(x) for x in out[-1]["blue"].split(",")]
    return out


def get_team_matches_dict(event_key: str) -> Dict[str, Dict[int, float]]:
    data: List[Dict[str, Any]] = (
        TeamMatch.objects.values("team", "match", "elo")  # type: ignore
        .filter(event=event_key, playoff=0)
        .order_by("time")
    )

    out: Dict[str, Dict[int, float]] = {}
    for entry in data:
        if entry["match"] not in out:
            out[entry["match"]] = {}
        if entry["team"] not in out[entry["match"]]:
            out[entry["match"]][entry["team"]] = entry["elo"]
    return out
