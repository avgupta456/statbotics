from typing import List, Optional

import attr

from src.site.models.main import APIModel


@attr.s(auto_attribs=True, slots=True)
class APIMatch(APIModel):
    year: int
    event: str
    time: int
    predicted_time: int
    key: str
    match_name: str
    status: str
    video: Optional[str]
    comp_level: str
    set_number: int
    match_number: int
    elim: bool
    red: List[str]
    blue: List[str]
    red_surrogates: List[str]
    blue_surrogates: List[str]
    red_dqs: List[str]
    blue_dqs: List[str]

    # Actual
    red_score: int
    red_rp_1: int
    red_rp_2: int
    blue_score: int
    blue_rp_1: int
    blue_rp_2: int
    winner: str

    # Predicted
    red_epa_pred: float
    blue_epa_pred: float
    epa_win_prob: float
    pred_winner: str
