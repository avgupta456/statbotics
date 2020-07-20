from rankings.models import Match, TeamEvent, TeamMatch, Year


def getYearDict(year):
    data = Year.objects.values("score_sd", "score_mean").get(year=year)
    return data["score_sd"], data["score_mean"]


def getTeamsDict(event_key):
    data = (
        TeamEvent.objects.values(
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

    out, stats = [], {}
    for entry in data:
        out.append(entry["team"])
        stats[entry["team"]] = entry
    return out, stats


def getMatchesDict(event_key):
    data = Match.objects.values(
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
    ).filter(event=event_key, playoff=0)

    out = []
    for entry in data:
        out.append(entry)
        out[-1]["red"] = [int(x) for x in out[-1]["red"].split(",")]
        out[-1]["blue"] = [int(x) for x in out[-1]["blue"].split(",")]
    return out


def getTeamMatchesDict(event_key):
    data = TeamMatch.objects.values("team", "match", "elo").filter(
        event=event_key
    )  # noqa 502

    out = {}
    for entry in data:
        if entry["match"] not in out:
            out[entry["match"]] = {}
        if entry["team"] not in out[entry["match"]]:
            out[entry["match"]][entry["team"]] = entry["elo"]
    return out
