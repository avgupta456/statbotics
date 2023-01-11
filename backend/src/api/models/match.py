from typing import List, Optional

import attr

from src.api.models.main import APIModel


@attr.s(auto_attribs=True, slots=True)
class APIMatch(APIModel):
    year: int
    event: str
    time: int
    key: str
    match_name: str
    status: str
    video: Optional[str]
    comp_level: str
    set_number: int
    match_number: int
    playoff: bool
    red: List[int]
    blue: List[int]

    # Actual
    red_score: int
    red_auto: int
    red_teleop: int
    red_endgame: int
    red_1: int
    red_2: int
    red_fouls: int
    red_rp_1: int
    red_rp_2: int
    blue_score: int
    blue_auto: int
    blue_teleop: int
    blue_endgame: int
    blue_1: int
    blue_2: int
    blue_fouls: int
    blue_rp_1: int
    blue_rp_2: int
    winner: str

    # Predicted
    red_epa_pred: float
    red_auto_epa_pred: float
    red_teleop_epa_pred: float
    red_endgame_epa_pred: float
    red_rp_1_pred: float
    red_rp_2_pred: float
    blue_epa_pred: float
    blue_auto_epa_pred: float
    blue_teleop_epa_pred: float
    blue_endgame_epa_pred: float
    blue_rp_1_pred: float
    blue_rp_2_pred: float
    epa_win_prob: float
    pred_winner: str
