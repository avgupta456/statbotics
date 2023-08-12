import copy
from typing import Any, Dict, Optional


class Match:
    key: str
    event: str
    week: int
    year: int
    playoff: bool
    time: int
    red_1: int
    red_2: int
    red_3: int
    blue_1: int
    blue_2: int
    blue_3: int
    red_score: int
    blue_score: int
    red_no_fouls: int
    blue_no_fouls: int
    red_rp_1: bool
    blue_rp_1: bool
    red_rp_2: bool
    blue_rp_2: bool
    red_breakdown: Any
    blue_breakdown: Any
    winner: float

    def __init__(
        self,
        key: str,
        event: str,
        week: int,
        year: int,
        playoff: bool,
        time: int,
        red_1: int,
        red_2: int,
        red_3: int,
        blue_1: int,
        blue_2: int,
        blue_3: int,
        red_score: int,
        blue_score: int,
        red_no_fouls: int,
        blue_no_fouls: int,
        red_rp_1: bool,
        blue_rp_1: bool,
        red_rp_2: bool,
        blue_rp_2: bool,
        red_breakdown: Any,
        blue_breakdown: Any,
    ):
        self.key = key
        self.event = event
        self.week = week
        self.year = year
        self.playoff = playoff
        self.time = time
        self.red_1 = red_1
        self.red_2 = red_2
        self.red_3 = red_3
        self.blue_1 = blue_1
        self.blue_2 = blue_2
        self.blue_3 = blue_3
        self.red_score = red_score
        self.blue_score = blue_score
        self.red_no_fouls = red_no_fouls
        self.blue_no_fouls = blue_no_fouls
        self.red_rp_1 = red_rp_1
        self.blue_rp_1 = blue_rp_1
        self.red_rp_2 = red_rp_2
        self.blue_rp_2 = blue_rp_2
        self.red_breakdown = red_breakdown
        self.blue_breakdown = blue_breakdown

        self.winner = (
            1 if red_score > blue_score else 0.5 if red_score == blue_score else 0
        )

    def red(self):
        return (self.red_1, self.red_2, self.red_3)

    def blue(self):
        return (self.blue_1, self.blue_2, self.blue_3)

    def mask(self) -> "Match":
        match_copy = copy.deepcopy(self)
        match_copy.red_score = 0
        match_copy.blue_score = 0
        return match_copy

    def __repr__(self):
        return f"Match({self.key}, {self.red_1} {self.red_2} {self.red_3} vs. {self.blue_1} {self.blue_2} {self.blue_3}, {self.red_score}-{self.blue_score})"


class YearStats:
    year: int
    score_mean: float
    score_sd: float
    rp_1_mean: float
    rp_1_sd: float
    rp_2_mean: float
    rp_2_sd: float
    breakdown_mean: Dict[str, float]
    breakdown_sd: Dict[str, float]

    def __init__(
        self,
        year: int,
        score_mean: float,
        score_sd: float,
        rp_1_mean: float,
        rp_1_sd: float,
        rp_2_mean: float,
        rp_2_sd: float,
        breakdown_mean: Dict[str, float],
        breakdown_sd: Dict[str, float],
    ):
        self.year = year
        self.score_mean = score_mean
        self.score_sd = score_sd
        self.rp_1_mean = rp_1_mean
        self.rp_1_sd = rp_1_sd
        self.rp_2_mean = rp_2_mean
        self.rp_2_sd = rp_2_sd
        self.breakdown_mean = breakdown_mean
        self.breakdown_sd = breakdown_sd

    def __repr__(self):
        return f"YearStats({self.year})"


class Pred:
    red_score: float
    blue_score: float
    win_prob: float

    red_rp_1: float
    blue_rp_1: float
    red_rp_2: float
    blue_rp_2: float

    # Optional
    red_breakdown: Dict[str, Any]
    blue_breakdown: Dict[str, Any]

    def __init__(
        self,
        red_score: float,
        blue_score: float,
        win_prob: float,
        red_rp_1: float,
        blue_rp_1: float,
        red_rp_2: float,
        blue_rp_2: float,
        red_breakdown: Optional[Dict[str, Any]] = None,
        blue_breakdown: Optional[Dict[str, Any]] = None,
    ):
        self.red_score = red_score
        self.blue_score = blue_score
        self.win_prob = win_prob
        self.red_rp_1 = red_rp_1
        self.blue_rp_1 = blue_rp_1
        self.red_rp_2 = red_rp_2
        self.blue_rp_2 = blue_rp_2
        self.red_breakdown = red_breakdown or {}
        self.blue_breakdown = blue_breakdown or {}

    def __repr__(self):
        return f"Pred({self.red_score}-{self.blue_score}, {self.win_prob})"


class Attribution:
    contrib: float
    breakdown: Dict[str, Any]

    def __init__(self, contrib: float, breakdown: Optional[Dict[str, Any]] = None):
        self.contrib = contrib
        self.breakdown = breakdown or {}

    def __repr__(self):
        return f"Attribution({self.contrib})"
