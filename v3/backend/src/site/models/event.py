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
    qual_matches: Optional[int]
    current_match: Optional[int]
    epa_acc: Optional[float]
    epa_mse: Optional[float]
    epa_max: Optional[float]
    epa_top_8: Optional[float]
    epa_top_24: Optional[float]
    epa_mean: Optional[float]
