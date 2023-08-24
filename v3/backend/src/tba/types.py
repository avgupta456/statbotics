from typing import Optional, TypedDict


class TeamDict(TypedDict):
    team: str
    name: str
    rookie_year: int
    offseason: bool
    state: Optional[str]
    country: Optional[str]


class EventDict(TypedDict):
    year: int
    key: str
    name: str
    state: Optional[str]
    country: Optional[str]
    district: Optional[str]
    start_date: str
    end_date: str
    time: int
    type: int
    week: int
    video: Optional[str]


class BreakdownDict(TypedDict):
    score: Optional[int]
    no_foul_points: Optional[int]
    foul_points: Optional[int]
    auto_points: Optional[int]
    teleop_points: Optional[int]
    endgame_points: Optional[int]
    rp_1: Optional[bool]
    rp_2: Optional[bool]
    match_comp_1: Optional[int]
    match_comp_2: Optional[int]
    match_comp_3: Optional[int]
    match_comp_4: Optional[int]
    match_comp_5: Optional[int]
    match_comp_6: Optional[int]
    match_comp_7: Optional[int]
    match_comp_8: Optional[int]
    match_comp_9: Optional[int]
    match_comp_10: Optional[int]
    match_comp_11: Optional[int]
    match_comp_12: Optional[int]
    tiebreaker: Optional[int]


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
