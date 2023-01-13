from typing import Optional

import attr

from src.site.models.main import APIModel


@attr.s(auto_attribs=True, slots=True)
class APIEvent(APIModel):
    key: str
    name: str
    year: int
    week: int
    start_date: str
    end_date: str
    country: Optional[str]
    state: Optional[str]
    district: Optional[str]
    offseason: bool
    status: str
    status_str: str
