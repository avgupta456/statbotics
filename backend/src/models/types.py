from typing import Any, Optional


class AlliancePred:
    score: float
    breakdown: Any
    rp_1: Optional[float]
    rp_2: Optional[float]
    # Backwards compatibility
    auto: Optional[float]
    teleop: Optional[float]
    endgame: Optional[float]

    def __init__(
        self,
        score: float,
        breakdown: Any,
        rp_1: Optional[float] = None,
        rp_2: Optional[float] = None,
        # Backwards compatibility
        auto: Optional[float] = None,
        teleop: Optional[float] = None,
        endgame: Optional[float] = None,
    ):
        self.score = score
        self.breakdown = breakdown
        self.rp_1 = rp_1
        self.rp_2 = rp_2
        self.auto = auto
        self.teleop = teleop
        self.endgame = endgame

    def __repr__(self):
        return f"Pred({self.score} {self.rp_1} {self.rp_2})"


class MatchPred:
    win_prob: float
    red_score: float
    blue_score: float
    red_rp_1: Optional[float]
    blue_rp_1: Optional[float]
    red_rp_2: Optional[float]
    blue_rp_2: Optional[float]
    # Backwards compatibility
    red_auto: Optional[float]
    red_teleop: Optional[float]
    red_endgame: Optional[float]
    blue_auto: Optional[float]
    blue_teleop: Optional[float]
    blue_endgame: Optional[float]

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
        # Backwards compatibility
        self.red_auto = red_pred.auto
        self.red_teleop = red_pred.teleop
        self.red_endgame = red_pred.endgame
        self.blue_auto = blue_pred.auto
        self.blue_teleop = blue_pred.teleop
        self.blue_endgame = blue_pred.endgame


class Attribution:
    epa: Any

    def __init__(self, epa: Optional[Any] = None):
        self.epa = epa

    def __repr__(self):
        return f"Attribution({self.epa})"
