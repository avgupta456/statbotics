from typing import Optional

import attr

from src.site.models.main import APIModel


@attr.s(auto_attribs=True, slots=True)
class APITeamYear(APIModel):
    num: int
    team: str
    state: Optional[str]
    country: Optional[str]
    district: Optional[str]
    next_event_key: Optional[str]
    next_event_name: Optional[str]
    next_event_week: Optional[int]
    epa_rank: int
    epa_count: int
    state_epa_rank: int
    state_epa_count: int
    country_epa_rank: int
    country_epa_count: int
    district_epa_rank: int
    district_epa_count: int
    total_epa: float
    unitless_epa: float
    norm_epa: float
    auto_epa: float
    teleop_epa: float
    endgame_epa: float
    rp_1_epa: float
    rp_2_epa: float
    wins: int
    losses: int
    ties: int
    count: int
    offseason: bool
