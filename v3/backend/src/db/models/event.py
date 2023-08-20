from typing import Any, Dict, Optional

import attr
from sqlalchemy import Boolean, Column, Float, Integer, String  # type: ignore
from sqlalchemy.sql.schema import (  # type: ignore
    ForeignKeyConstraint,
    PrimaryKeyConstraint,
)

from src.db.main import Base
from src.db.models.main import ModelORM, generate_attr_class


class EventORM(Base, ModelORM):
    """DECLARATION"""

    __tablename__ = "events"
    key: str = Column(String(20), index=True)
    year: int = Column(Integer, index=True)

    PrimaryKeyConstraint(key)
    ForeignKeyConstraint(["year"], ["years.year"])

    """GENERAL"""
    name: str = Column(String(100))
    time: int = Column(Integer)
    country: Optional[str] = Column(String(30))
    district: Optional[str] = Column(String(10))
    state: Optional[str] = Column(String(10))
    start_date: str = Column(String(10))
    end_date: str = Column(String(10))

    # 0 is regional, 1 is district, 2 is district champ,
    # 3 is worlds division, 4 is einsteins/FOC
    # 99 is offseason, 100 is preseason
    type: int = Column(Integer)
    week: int = Column(Integer)
    offseason: bool = Column(Boolean)

    # Link to livestream, full link (unlike Match) to handle Twitch/YT
    video: str = Column(String(50))

    # Choices are 'Upcoming', 'Ongoing', 'Completed'
    status: str = Column(String(10))

    # -1 = upcoming event, 0 = schedule release, x = match x concluded
    current_match: int = Column(Integer)
    qual_matches: int = Column(Integer)

    """EPA"""
    epa_max: float = Column(Float)
    epa_top8: Optional[float] = Column(Float)
    epa_top24: Optional[float] = Column(Float)
    epa_mean: float = Column(Float)
    epa_sd: float = Column(Float)

    """STATS"""
    epa_acc: Optional[float] = Column(Float)
    epa_mse: Optional[float] = Column(Float)
    rp_1_acc: Optional[float] = Column(Float)
    rp_1_mse: Optional[float] = Column(Float)
    rp_2_acc: Optional[float] = Column(Float)
    rp_2_mse: Optional[float] = Column(Float)


_Event = generate_attr_class("Event", EventORM)


class Event(_Event):
    @classmethod
    def from_dict(cls, dict: Dict[str, Any]) -> "Event":
        dict = {k: dict.get(k, None) for k in cls.__slots__}  # type: ignore
        return Event(**dict)

    def as_dict(self: "Event") -> Dict[str, Any]:
        return attr.asdict(
            self,  # type: ignore
            filter=attr.filters.exclude(attr.fields(Event).current_match),  # type: ignore
        )

    def __str__(self: "Event"):
        # Only refresh DB if these change (during 1 min partial update)
        return f"{self.key}_{self.status}_{self.current_match}_{self.qual_matches}"
