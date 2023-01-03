from typing import Optional

import attr

from src.api.models.main import APIModel


@attr.s(auto_attribs=True, slots=True)
class APITeam(APIModel):
    num: int
    team: str
    state: Optional[str]
    country: Optional[str]
    district: Optional[str]
    rookie_year: int
    offseason: bool
