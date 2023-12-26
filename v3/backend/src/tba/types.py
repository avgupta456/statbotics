from typing import Optional, TypedDict
from src.types.enums import EventType, CompLevel, MatchStatus, MatchWinner


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
    type: EventType
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
    tiebreaker: Optional[int]
    comp_1: Optional[int]
    comp_2: Optional[int]
    comp_3: Optional[int]
    comp_4: Optional[int]
    comp_5: Optional[int]
    comp_6: Optional[int]
    comp_7: Optional[int]
    comp_8: Optional[int]
    comp_9: Optional[int]
    comp_10: Optional[int]
    comp_11: Optional[int]
    comp_12: Optional[int]


class MatchDict(TypedDict):
    event: str
    key: str
    comp_level: CompLevel
    set_number: int
    match_number: int
    status: MatchStatus
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
    winner: Optional[MatchWinner]
    time: int
    predicted_time: Optional[int]
    red_score: Optional[int]
    blue_score: Optional[int]
    red_score_breakdown: BreakdownDict
    blue_score_breakdown: BreakdownDict
