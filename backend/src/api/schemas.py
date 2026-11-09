"""Pydantic response schemas for OpenAPI spec generation.

These models define the structure of API responses so that FastAPI can generate
a complete OpenAPI specification with typed fields instead of generic object/any.
Each schema mirrors the output of an entity's to_dict() method.
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel


# Team schemas
class TeamRecord(BaseModel):
    wins: int = 0
    losses: int = 0
    ties: int = 0
    count: int = 0
    winrate: float = 0.0


class TeamNormEpa(BaseModel):
    current: Optional[float] = None
    recent: Optional[float] = None
    mean: Optional[float] = None
    max: Optional[float] = None


class TeamResponse(BaseModel):
    team: int
    name: str
    nickname: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    website: Optional[str] = None
    rookie_year: Optional[int] = None
    record: TeamRecord
    norm_epa: TeamNormEpa


# Event schemas
class EventEpa(BaseModel):
    max: Optional[float] = None
    top_8: Optional[float] = None
    top_24: Optional[float] = None
    mean: Optional[float] = None
    sd: Optional[float] = None


class WinProbMetrics(BaseModel):
    count: int = 0
    conf: Optional[float] = None
    acc: Optional[float] = None
    mse: Optional[float] = None


class ScorePredMetrics(BaseModel):
    count: int = 0
    rmse: Optional[float] = None
    error: Optional[float] = None


class EventMetrics(BaseModel):
    win_prob: WinProbMetrics
    score_pred: ScorePredMetrics
    rp_pred: Optional[Dict[str, Any]] = None
    rp_3: Optional[Dict[str, Any]] = None


class EventResponse(BaseModel):
    key: str
    year: int
    name: str
    time: Optional[float] = None
    country: Optional[str] = None
    state: Optional[str] = None
    district: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    type: Optional[int] = None
    week: Optional[int] = None
    video: Optional[List[Any]] = None
    status: str
    status_str: str
    num_teams: int = 0
    current_match: int = 0
    qual_matches: int = 0
    epa: EventEpa
    metrics: EventMetrics


# Match schemas
class MatchResponse(BaseModel):
    key: str
    year: int
    event: str
    week: int
    elim: bool
    comp_level: str
    set_number: int
    match_number: int
    time: Optional[int] = None
    predicted_time: Optional[int] = None
    status: str
    video: Optional[str] = None
    red_1: int
    red_2: int
    red_3: Optional[int] = None
    red_dq: str
    red_surrogate: str
    blue_1: int
    blue_2: int
    blue_3: Optional[int] = None
    blue_dq: str
    blue_surrogate: str
    winner: Optional[str] = None
    epa_winner: Optional[str] = None
    red_score: Optional[int] = None
    red_no_foul: Optional[int] = None
    red_foul: Optional[int] = None
    red_auto: Optional[int] = None
    red_teleop: Optional[int] = None
    red_endgame: Optional[int] = None
    blue_score: Optional[int] = None
    blue_no_foul: Optional[int] = None
    blue_foul: Optional[int] = None
    blue_auto: Optional[int] = None
    blue_teleop: Optional[int] = None
    blue_endgame: Optional[int] = None
    epa_win_prob: Optional[float] = None
    epa_red_score_pred: Optional[float] = None
    epa_blue_score_pred: Optional[float] = None
    pre_epas: Optional[Dict[str, Any]] = None
    epas: Optional[Dict[str, Any]] = None


# TeamEvent schemas
class TeamEpaBreakdown(BaseModel):
    """Dynamic fields by year - use Dict to capture all keys."""
    pass


class TeamEpaStats(BaseModel):
    start: float = 0.0
    pre_elim: float = 0.0
    mean: float = 0.0
    max: float = 0.0


class TeamEpaResponse(BaseModel):
    total_points: float = 0.0
    unitless: float = 0.0
    norm: float = 0.0
    breakdown: Dict[str, Optional[float]] = {}
    stats: TeamEpaStats


class TeamEventQualRecord(BaseModel):
    wins: int = 0
    losses: int = 0
    ties: int = 0
    count: int = 0
    winrate: float = 0.0
    rps: Optional[float] = None
    rps_per_match: Optional[float] = None
    rank: Optional[int] = None
    num_teams: Optional[int] = None


class TeamEventElimRecord(BaseModel):
    wins: int = 0
    losses: int = 0
    ties: int = 0
    count: int = 0
    winrate: float = 0.0
    alliance: Optional[str] = None
    is_captain: Optional[bool] = None


class TeamEventTotalRecord(BaseModel):
    wins: int = 0
    losses: int = 0
    ties: int = 0
    count: int = 0
    winrate: float = 0.0


class TeamEventRecord(BaseModel):
    qual: TeamEventQualRecord
    elim: TeamEventElimRecord
    total: TeamEventTotalRecord


class TeamEventResponse(BaseModel):
    team: int
    year: int
    event: str
    time: Optional[float] = None
    team_name: Optional[str] = None
    event_name: Optional[str] = None
    country: Optional[str] = None
    state: Optional[str] = None
    district: Optional[str] = None
    type: Optional[int] = None
    week: Optional[int] = None
    status: str
    first_event: bool = False
    epa: TeamEpaResponse
    record: TeamEventRecord


# TeamYear schemas
class TeamYearResponse(BaseModel):
    team: int
    year: int
    epa: TeamEpaResponse
    record: TeamEventRecord
    competing: bool = False


# Year schemas
class YearTeamEntry(BaseModel):
    team_number: int
    name: str
    nickname: Optional[str] = None
    city: Optional[str] = None
    state_prov: Optional[str] = None
    country: Optional[str] = None
    rookie_year: Optional[int] = None


class YearEventEntry(BaseModel):
    event_key: str
    name: str
    short_name: Optional[str] = None
    city: Optional[str] = None
    state_prov: Optional[str] = None
    country: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None


class YearResponse(BaseModel):
    year: int
    teams: List[YearTeamEntry]
    events: List[YearEventEntry]
