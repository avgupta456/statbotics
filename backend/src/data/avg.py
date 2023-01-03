import statistics
from typing import List

from src.db.models import Event, Match, Year


def process_year(year: Year, events: List[Event], matches: List[Match]) -> Year:
    week_one_events = set([e.key for e in events if e.week == 1])
    week_one_matches = [m for m in matches if m.event in week_one_events]
    week_one_matches = [m for m in week_one_matches if m.status == "Completed"]

    scores: List[int] = []
    autos: List[int] = []
    teleops: List[int] = []
    endgames: List[int] = []
    fouls: List[int] = []
    no_fouls: List[int] = []
    rp_1s: List[int] = []
    rp_2s: List[int] = []

    # TODO: investigate discrepancy between scores and fouls + no_fouls
    for match in week_one_matches:
        scores.extend([match.red_score or 0, match.blue_score or 0])
        autos.extend([match.red_auto or 0, match.blue_auto or 0])
        teleops.extend([match.red_teleop or 0, match.blue_teleop or 0])
        endgames.extend([match.red_endgame or 0, match.blue_endgame or 0])
        fouls.extend([match.red_fouls or 0, match.blue_fouls or 0])
        no_fouls.extend([match.red_no_fouls or 0, match.blue_no_fouls or 0])
        rp_1s.extend([match.red_rp_1 or 0, match.blue_rp_1 or 0])
        rp_2s.extend([match.red_rp_2 or 0, match.blue_rp_2 or 0])

    if year.year == 2023:
        year.score_mean = 30
        year.score_sd = 10
        year.auto_mean = 10
        year.teleop_mean = 10
        year.endgame_mean = 10
        year.fouls_mean = 0
        year.no_fouls_mean = 30
        year.rp_1_mean = 0.2
        year.rp_2_mean = 0.1

    if len(scores) > 0:
        year.score_mean = round(sum(scores) / len(scores), 2)
        year.score_sd = round(statistics.pstdev(scores), 2)
        year.auto_mean = round(sum(autos) / len(autos), 2)
        year.teleop_mean = round(sum(teleops) / len(teleops), 2)
        year.endgame_mean = round(sum(endgames) / len(endgames), 2)
        year.fouls_mean = round(sum(fouls) / len(fouls), 2)
        year.no_fouls_mean = round(sum(no_fouls) / len(no_fouls), 2)
        year.rp_1_mean = round(sum(rp_1s) / len(rp_1s), 2)
        year.rp_2_mean = round(sum(rp_2s) / len(rp_2s), 2)

    if year.year < 2016:
        year.auto_mean = None
        year.teleop_mean = None
        year.endgame_mean = None
        year.fouls_mean = None
        year.no_fouls_mean = None
        year.rp_1_mean = None
        year.rp_2_mean = None

    return year
