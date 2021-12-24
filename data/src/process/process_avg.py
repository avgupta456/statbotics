import statistics
from typing import List

from db.models.year import Year
from db.models.match import Match
from db.models.event import Event


def process_year(year: Year, events: List[Event], matches: List[Match]) -> Year:
    week_one_events = set([e.id for e in events if e.week == 1])
    week_one_matches = [m for m in matches if m.event_id in week_one_events]

    scores: List[int] = []
    autos: List[int] = []
    teleops: List[int] = []
    ones: List[int] = []
    twos: List[int] = []
    endgames: List[int] = []
    fouls: List[int] = []
    no_fouls: List[int] = []
    rp_1s: List[int] = []
    rp_2s: List[int] = []

    for match in week_one_matches:
        scores.extend([match.red_score, match.blue_score])
        autos.extend([match.red_auto, match.blue_auto])
        teleops.extend([match.red_teleop, match.blue_teleop])
        ones.extend([match.red_1, match.blue_1])
        twos.extend([match.red_2, match.blue_2])
        endgames.extend([match.red_endgame, match.blue_endgame])
        fouls.extend([match.red_fouls, match.blue_fouls])
        no_fouls.extend([match.red_no_fouls, match.blue_no_fouls])
        rp_1s.extend([match.red_rp_1, match.blue_rp_1])
        rp_2s.extend([match.red_rp_2, match.blue_rp_2])

    year.score_mean = round(sum(scores) / len(scores), 2)
    year.score_sd = round(statistics.pstdev(scores), 2)
    year.auto_mean = round(sum(autos) / len(autos), 2)
    year.teleop_mean = round(sum(teleops) / len(teleops), 2)
    year.one_mean = round(sum(ones) / len(ones), 2)
    year.two_mean = round(sum(twos) / len(twos), 2)
    year.endgame_mean = round(sum(endgames) / len(endgames), 2)
    year.fouls_mean = round(sum(fouls) / len(fouls), 2)
    year.no_fouls_mean = round(sum(no_fouls) / len(no_fouls), 2)
    year.rp_1_mean = round(sum(rp_1s) / len(rp_1s), 2)
    year.rp_2_mean = round(sum(rp_2s) / len(rp_2s), 2)

    return year
