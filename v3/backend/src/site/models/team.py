from typing import Optional

import attr

from src.site.models.main import APIModel


@attr.s(auto_attribs=True, slots=True)
class APITeam(APIModel):
    num: str
    team: str
    active: bool
    country: Optional[str]
    state: Optional[str]
    district: Optional[str]
    rookie_year: int
    offseason: bool
