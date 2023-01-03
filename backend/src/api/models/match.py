from typing import List

import attr

from src.api.models.main import APIModel


@attr.s(auto_attribs=True, slots=True)
class APIMatch(APIModel):
    time: int
    key: str
    comp_level: str
    set_number: int
    match_number: int
    playoff: bool
    red: List[int]
    blue: List[int]
    red_score: int
    blue_score: int
    winner: str
    red_rp_1: int
    red_rp_2: int
    blue_rp_1: int
    blue_rp_2: int
    red_epa_pred: float
    blue_epa_pred: float
    red_rp_1_pred: float
    red_rp_2_pred: float
    epa_win_prob: float
    pred_winner: str
    blue_rp_1_pred: float
    blue_rp_2_pred: float
    # for simulation
    red_auto: float
    red_teleop: float
    red_endgame: float
    red_1: float
    red_2: float
    blue_auto: float
    blue_teleop: float
    blue_endgame: float
    blue_1: float
    blue_2: float
