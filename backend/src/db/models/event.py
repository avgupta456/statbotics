from typing import Any, Dict, Optional

import attr
from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.sql.schema import ForeignKeyConstraint, PrimaryKeyConstraint

from src.db.main import Base
from src.db.models.main import Model, ModelORM


class EventORM(Base, ModelORM):
    """DECLARATION"""

    __tablename__ = "events"
    key = Column(String(20), index=True)
    year = Column(Integer, index=True)

    PrimaryKeyConstraint(key)
    ForeignKeyConstraint(["year"], ["years.year"])

    """GENERAL"""
    name = Column(String(100))
    time = Column(Integer)
    state = Column(String(10))
    country = Column(String(30))
    district = Column(String(10))

    # 0 is regional, 1 is district, 2 is district champ,
    # 3 is worlds division, 4 is einsteins/FOC
    type = Column(Integer)
    week = Column(Integer)

    # Choices are 'Upcoming', 'Ongoing', 'Completed'
    status = Column(String(10))

    # -1 = upcoming event, 0 = schedule release, x = match x concluded
    current_match = Column(Integer)
    qual_matches = Column(Integer)

    """ELO"""
    elo_max = Column(Float)
    elo_top8 = Column(Float)
    elo_top24 = Column(Float)
    elo_mean = Column(Float)
    elo_sd = Column(Float)

    """STATS"""
    elo_acc = Column(Float)
    elo_mse = Column(Float)
    rp1_acc = Column(Float)
    rp1_mse = Column(Float)
    rp2_acc = Column(Float)
    rp2_mse = Column(Float)


@attr.s(auto_attribs=True, slots=True)
class Event(Model):
    key: str
    year: int

    name: str
    time: int
    state: str
    country: str
    district: str
    type: int
    week: int

    status: str
    current_match: int
    qual_matches: int

    elo_max: Optional[float] = None
    elo_top8: Optional[float] = None
    elo_top24: Optional[float] = None
    elo_mean: Optional[float] = None
    elo_sd: Optional[float] = None

    elo_acc: Optional[float] = None
    elo_mse: Optional[float] = None

    rp1_acc: Optional[float] = None
    rp1_mse: Optional[float] = None
    rp2_acc: Optional[float] = None
    rp2_mse: Optional[float] = None

    @classmethod
    def from_dict(cls, dict: Dict[str, Any]) -> "Event":
        dict = {k: dict.get(k, None) for k in cls.__slots__}
        return Event(**dict)
