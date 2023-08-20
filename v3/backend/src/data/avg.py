import statistics
from typing import List

from src.db.models import Alliance, Year


def process_year(year: Year, alliances: List[Alliance]) -> Year:
    week_one_alliances = [
        a for a in alliances if a.week == 1 and a.status == "Completed"
    ]

    score_arr: List[int] = []
    no_foul_arr: List[int] = []
    foul_arr: List[int] = []
    auto_arr: List[int] = []
    teleop_arr: List[int] = []
    endgame_arr: List[int] = []
    rp_1_arr: List[int] = []
    rp_2_arr: List[int] = []
    comp_1_arr: List[float] = []
    comp_2_arr: List[float] = []
    comp_3_arr: List[float] = []
    comp_4_arr: List[float] = []
    comp_5_arr: List[float] = []
    comp_6_arr: List[float] = []
    comp_7_arr: List[float] = []
    comp_8_arr: List[float] = []
    comp_9_arr: List[float] = []
    comp_10_arr: List[float] = []

    for alliance in week_one_alliances:
        score_arr.append(alliance.score or 0)
        no_foul_arr.append(alliance.no_foul_points or 0)
        foul_arr.append(alliance.foul_points or 0)
        auto_arr.append(alliance.auto_points or 0)
        teleop_arr.append(alliance.teleop_points or 0)
        endgame_arr.append(alliance.endgame_points or 0)
        rp_1_arr.append(alliance.rp_1 or 0)
        rp_2_arr.append(alliance.rp_2 or 0)
        comp_1_arr.append(alliance.comp_1 or 0)
        comp_2_arr.append(alliance.comp_2 or 0)
        comp_3_arr.append(alliance.comp_3 or 0)
        comp_4_arr.append(alliance.comp_4 or 0)
        comp_5_arr.append(alliance.comp_5 or 0)
        comp_6_arr.append(alliance.comp_6 or 0)
        comp_7_arr.append(alliance.comp_7 or 0)
        comp_8_arr.append(alliance.comp_8 or 0)
        comp_9_arr.append(alliance.comp_9 or 0)
        comp_10_arr.append(alliance.comp_10 or 0)

    if len(score_arr) > 0:
        year.score_mean = round(sum(score_arr) / len(score_arr), 2)
        year.score_sd = round(statistics.pstdev(score_arr), 2)
        year.no_foul_mean = round(sum(no_foul_arr) / len(no_foul_arr), 2)
        year.foul_mean = round(sum(foul_arr) / len(foul_arr), 2)
        year.auto_mean = round(sum(auto_arr) / len(auto_arr), 2)
        year.teleop_mean = round(sum(teleop_arr) / len(teleop_arr), 2)
        year.endgame_mean = round(sum(endgame_arr) / len(endgame_arr), 2)
        year.rp_1_mean = round(sum(rp_1_arr) / len(rp_1_arr), 2)
        year.rp_2_mean = round(sum(rp_2_arr) / len(rp_2_arr), 2)
        year.comp_1_mean = round(sum(comp_1_arr) / len(comp_1_arr), 2)
        year.comp_2_mean = round(sum(comp_2_arr) / len(comp_2_arr), 2)
        year.comp_3_mean = round(sum(comp_3_arr) / len(comp_3_arr), 2)
        year.comp_4_mean = round(sum(comp_4_arr) / len(comp_4_arr), 2)
        year.comp_5_mean = round(sum(comp_5_arr) / len(comp_5_arr), 2)
        year.comp_6_mean = round(sum(comp_6_arr) / len(comp_6_arr), 2)
        year.comp_7_mean = round(sum(comp_7_arr) / len(comp_7_arr), 2)
        year.comp_8_mean = round(sum(comp_8_arr) / len(comp_8_arr), 2)
        year.comp_9_mean = round(sum(comp_9_arr) / len(comp_9_arr), 2)
        year.comp_10_mean = round(sum(comp_10_arr) / len(comp_10_arr), 2)

    if year.year < 2016:
        year.no_foul_mean = None
        year.foul_mean = None
        year.auto_mean = None
        year.teleop_mean = None
        year.endgame_mean = None
        year.rp_1_mean = None
        year.rp_2_mean = None
        year.comp_1_mean = None
        year.comp_2_mean = None
        year.comp_3_mean = None
        year.comp_4_mean = None
        year.comp_5_mean = None
        year.comp_6_mean = None
        year.comp_7_mean = None
        year.comp_8_mean = None
        year.comp_9_mean = None
        year.comp_10_mean = None

    return year
