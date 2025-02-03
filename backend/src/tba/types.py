from typing import Optional, TypedDict, Union

from src.types.enums import CompLevel, EventType, MatchStatus, MatchWinner


class TeamDict(TypedDict):
    team: int
    name: str
    rookie_year: int
    country: Optional[str]
    state: Optional[str]


class EventDict(TypedDict):
    year: int
    key: str
    name: str
    country: Optional[str]
    state: Optional[str]
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
    rp_3: Optional[bool]
    tiebreaker: Optional[int]
    comp_1: Optional[Union[int, float]]
    comp_2: Optional[Union[int, float]]
    comp_3: Optional[Union[int, float]]
    comp_4: Optional[Union[int, float]]
    comp_5: Optional[Union[int, float]]
    comp_6: Optional[Union[int, float]]
    comp_7: Optional[Union[int, float]]
    comp_8: Optional[Union[int, float]]
    comp_9: Optional[Union[int, float]]
    comp_10: Optional[Union[int, float]]
    comp_11: Optional[Union[int, float]]
    comp_12: Optional[Union[int, float]]
    comp_13: Optional[Union[int, float]]
    comp_14: Optional[Union[int, float]]
    comp_15: Optional[Union[int, float]]
    comp_16: Optional[Union[int, float]]
    comp_17: Optional[Union[int, float]]
    comp_18: Optional[Union[int, float]]


empty_breakdown: BreakdownDict = {
    "score": 0,
    "no_foul_points": None,
    "foul_points": None,
    "auto_points": None,
    "teleop_points": None,
    "endgame_points": None,
    "rp_1": False,
    "rp_2": False,
    "rp_3": False,
    "tiebreaker": None,
    "comp_1": None,
    "comp_2": None,
    "comp_3": None,
    "comp_4": None,
    "comp_5": None,
    "comp_6": None,
    "comp_7": None,
    "comp_8": None,
    "comp_9": None,
    "comp_10": None,
    "comp_11": None,
    "comp_12": None,
    "comp_13": None,
    "comp_14": None,
    "comp_15": None,
    "comp_16": None,
    "comp_17": None,
    "comp_18": None,
}


class MatchDict(TypedDict):
    event: str
    key: str
    comp_level: CompLevel
    set_number: int
    match_number: int
    status: MatchStatus
    video: Optional[str]
    red_1: int
    red_2: int
    red_3: Optional[int]
    red_dq: str
    red_surrogate: str
    blue_1: int
    blue_2: int
    blue_3: Optional[int]
    blue_dq: str
    blue_surrogate: str
    winner: Optional[MatchWinner]
    time: int
    predicted_time: Optional[int]
    red_score: Optional[int]
    blue_score: Optional[int]
    red_score_breakdown: BreakdownDict
    blue_score_breakdown: BreakdownDict
