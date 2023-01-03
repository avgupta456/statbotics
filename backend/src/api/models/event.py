from typing import Optional

import attr

from src.api.models.main import APIModel


@attr.s(auto_attribs=True, slots=True)
class APIEvent(APIModel):
    key: str
    name: str
    year: int
    week: int
    country: Optional[str]
    state: Optional[str]
    district: Optional[str]
