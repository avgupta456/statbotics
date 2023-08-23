from typing import Optional, TypedDict


class BreakdownDict(TypedDict):
    score: Optional[int]
    no_foul_points: Optional[int]
    foul_points: Optional[int]
    auto_points: Optional[int]
    teleop_points: Optional[int]
    endgame_points: Optional[int]
    rp1: Optional[bool]
    rp2: Optional[bool]
    comp_1: Optional[float]
    comp_2: Optional[float]
    comp_3: Optional[float]
    comp_4: Optional[float]
    comp_5: Optional[float]
    comp_6: Optional[float]
    comp_7: Optional[float]
    comp_8: Optional[float]
    comp_9: Optional[float]
    comp_10: Optional[float]
    tiebreaker: Optional[float]


class MatchDict(TypedDict):
    event: str
    key: str
    comp_level: str
    set_number: int
    match_number: int
    status: str
    video: Optional[str]
    red_1: str
    red_2: str
    red_3: Optional[str]
    red_dq: str
    red_surrogate: str
    blue_1: str
    blue_2: str
    blue_3: Optional[str]
    blue_dq: str
    blue_surrogate: str
    official_winner: Optional[str]
    winner: Optional[str]
    time: int
    predicted_time: Optional[int]
    red_score: Optional[int]
    blue_score: Optional[int]
    red_score_breakdown: BreakdownDict
    blue_score_breakdown: BreakdownDict
