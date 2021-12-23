import statistics
from typing import List

from db.models.year import Year
from db.read.match import get_matches as get_matches_db
from db.read.year import get_years as get_years_db
from db.write.main import update_years as update_years_db


def process(start_year: int, end_year: int) -> None:
    year_objs: List[Year] = []
    for year in range(start_year, end_year + 1):
        year_obj = get_years_db(year)[0]
        matches = sorted(get_matches_db(year=year, week=1))

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

        for match in matches:
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

        year_obj.score_mean = round(sum(scores) / len(scores), 2)
        year_obj.score_sd = round(statistics.pstdev(scores), 2)
        year_obj.auto_mean = round(sum(autos) / len(autos), 2)
        year_obj.teleop_mean = round(sum(teleops) / len(teleops), 2)
        year_obj.one_mean = round(sum(ones) / len(ones), 2)
        year_obj.two_mean = round(sum(twos) / len(twos), 2)
        year_obj.endgame_mean = round(sum(endgames) / len(endgames), 2)
        year_obj.foul_mean = round(sum(fouls) / len(fouls), 2)
        year_obj.no_foul_mean = round(sum(no_fouls) / len(no_fouls), 2)
        year_obj.rp_1_mean = round(sum(rp_1s) / len(rp_1s), 2)
        year_obj.rp_2_mean = round(sum(rp_2s) / len(rp_2s), 2)
        year_objs.append(year_obj)

    update_years_db(year_objs, False)


def main(start_year: int, end_year: int):
    process(start_year, end_year)
