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
    tiebreaker_arr: List[float] = []
    match_comp_1_arr: List[float] = []
    match_comp_2_arr: List[float] = []
    match_comp_3_arr: List[float] = []
    match_comp_4_arr: List[float] = []
    match_comp_5_arr: List[float] = []
    match_comp_6_arr: List[float] = []
    match_comp_7_arr: List[float] = []
    match_comp_8_arr: List[float] = []
    match_comp_9_arr: List[float] = []
    match_comp_10_arr: List[float] = []
    match_comp_11_arr: List[float] = []
    match_comp_12_arr: List[float] = []

    for alliance in week_one_alliances:
        score_arr.append(alliance.score or 0)
        no_foul_arr.append(alliance.no_foul or 0)
        foul_arr.append(alliance.foul or 0)
        auto_arr.append(alliance.auto or 0)
        teleop_arr.append(alliance.teleop or 0)
        endgame_arr.append(alliance.endgame or 0)
        rp_1_arr.append(alliance.rp_1 or 0)
        rp_2_arr.append(alliance.rp_2 or 0)
        tiebreaker_arr.append(alliance.tiebreaker or 0)
        match_comp_1_arr.append(alliance.match_comp_1 or 0)
        match_comp_2_arr.append(alliance.match_comp_2 or 0)
        match_comp_3_arr.append(alliance.match_comp_3 or 0)
        match_comp_4_arr.append(alliance.match_comp_4 or 0)
        match_comp_5_arr.append(alliance.match_comp_5 or 0)
        match_comp_6_arr.append(alliance.match_comp_6 or 0)
        match_comp_7_arr.append(alliance.match_comp_7 or 0)
        match_comp_8_arr.append(alliance.match_comp_8 or 0)
        match_comp_9_arr.append(alliance.match_comp_9 or 0)
        match_comp_10_arr.append(alliance.match_comp_10 or 0)
        match_comp_11_arr.append(alliance.match_comp_11 or 0)
        match_comp_12_arr.append(alliance.match_comp_12 or 0)

    if len(score_arr) > 0:
        N = len(score_arr)
        year.score_mean = round(sum(score_arr) / N, 2)
        year.score_sd = round(statistics.pstdev(score_arr), 2)
        year.no_foul_mean = round(sum(no_foul_arr) / N, 2)
        year.foul_mean = round(sum(foul_arr) / N, 2)
        year.auto_mean = round(sum(auto_arr) / N, 2)
        year.teleop_mean = round(sum(teleop_arr) / N, 2)
        year.endgame_mean = round(sum(endgame_arr) / N, 2)
        year.rp_1_mean = round(sum(rp_1_arr) / N, 2)
        year.rp_2_mean = round(sum(rp_2_arr) / N, 2)
        year.tiebreaker_mean = round(sum(tiebreaker_arr) / N, 2)
        year.match_comp_1_mean = round(sum(match_comp_1_arr) / N, 2)
        year.match_comp_2_mean = round(sum(match_comp_2_arr) / N, 2)
        year.match_comp_3_mean = round(sum(match_comp_3_arr) / N, 2)
        year.match_comp_4_mean = round(sum(match_comp_4_arr) / N, 2)
        year.match_comp_5_mean = round(sum(match_comp_5_arr) / N, 2)
        year.match_comp_6_mean = round(sum(match_comp_6_arr) / N, 2)
        year.match_comp_7_mean = round(sum(match_comp_7_arr) / N, 2)
        year.match_comp_8_mean = round(sum(match_comp_8_arr) / N, 2)
        year.match_comp_9_mean = round(sum(match_comp_9_arr) / N, 2)
        year.match_comp_10_mean = round(sum(match_comp_10_arr) / N, 2)
        year.match_comp_11_mean = round(sum(match_comp_11_arr) / N, 2)
        year.match_comp_12_mean = round(sum(match_comp_12_arr) / N, 2)

    return year
