from typing import Optional

import attr

from src.api.models.main import APIModel


@attr.s(auto_attribs=True, slots=True)
class APITeamYear(APIModel):
    num: int
    team: str
    state: Optional[str]
    country: Optional[str]
    district: Optional[str]
    epa_rank: int
    epa_count: int
    state_epa_rank: int
    state_epa_count: int
    country_epa_rank: int
    country_epa_count: int
    district_epa_rank: int
    district_epa_count: int
    norm_epa: float
    total_epa: float
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
