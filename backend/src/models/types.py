from typing import Any, Optional


class AlliancePred:
    score: float
    breakdown: Any
    rp_1: Optional[float]
    rp_2: Optional[float]
    rp_3: Optional[float]

    def __init__(
        self,
        score: float,
        breakdown: Any,
        rp_1: Optional[float] = None,
        rp_2: Optional[float] = None,
        rp_3: Optional[float] = None,
    ):
        self.score = score
        self.breakdown = breakdown
        self.rp_1 = rp_1
        self.rp_2 = rp_2
        self.rp_3 = rp_3

    def __repr__(self):
        return f"Pred({self.score} {self.rp_1} {self.rp_2} {self.rp_3})"


class MatchPred:
    win_prob: float
    red_score: float
    blue_score: float
    red_rp_1: Optional[float]
    blue_rp_1: Optional[float]
    red_rp_2: Optional[float]
    blue_rp_2: Optional[float]
    red_rp_3: Optional[float]
    blue_rp_3: Optional[float]

    def __init__(
        self,
        win_prob: float,
        red_pred: AlliancePred,
        blue_pred: AlliancePred,
    ):
        self.win_prob = win_prob
        self.red_score = red_pred.score
        self.blue_score = blue_pred.score
        self.red_rp_1 = red_pred.rp_1
        self.blue_rp_1 = blue_pred.rp_1
        self.red_rp_2 = red_pred.rp_2
        self.blue_rp_2 = blue_pred.rp_2
        self.red_rp_3 = red_pred.rp_3
        self.blue_rp_3 = blue_pred.rp_3


class Attribution:
    epa: Any

    def __init__(self, epa: Optional[Any] = None):
        self.epa = epa

    def __repr__(self):
        return f"Attribution({self.epa})"
