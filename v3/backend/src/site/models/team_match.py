from typing import Optional

import attr

from src.site.models.main import APIModel


@attr.s(auto_attribs=True, slots=True)
class APITeamMatch(APIModel):
    num: int
    alliance: str
    match: str
    time: int
    elim: bool
    match_number: int  # qual only
    total_epa: float
    auto_epa: float
    teleop_epa: float
    endgame_epa: float
    rp_1_epa: float
    rp_2_epa: float
    post_epa: Optional[float]
    offseason: bool
    status: str
