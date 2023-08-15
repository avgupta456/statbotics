from typing import Optional

import attr

from src.site.models.main import APIModel


@attr.s(auto_attribs=True, slots=True)
class APITeam(APIModel):
    num: int
    team: str
    active: bool
    state: Optional[str]
    country: Optional[str]
    district: Optional[str]
    rookie_year: int
    offseason: bool
