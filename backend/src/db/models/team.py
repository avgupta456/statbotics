from typing import Any, Dict, Optional

import attr
from sqlalchemy import Boolean, Column, Float, Integer, String
from sqlalchemy.sql.schema import PrimaryKeyConstraint

from src.db.main import Base
from src.db.models.main import Model, ModelORM


class TeamORM(Base, ModelORM):
    """DECLARATION"""

    __tablename__ = "teams"
    team = Column(Integer, index=True)

    PrimaryKeyConstraint(team)

    """GENERAL"""
    name = Column(String(100))
    state = Column(String(10))
    country = Column(String(30))
    district = Column(String(10))
    active = Column(Boolean)

    """EPA"""
    # TODO: normalized EPA values
    # epa = Column(Float)
    # epa_recent = Column(Float)
    # epa_mean = Column(Float)
    # epa_max = Column(Float)

    """STATS"""
    wins = Column(Integer)
    losses = Column(Integer)
    ties = Column(Integer)
    count = Column(Integer)
    winrate = Column(Float)


@attr.s(auto_attribs=True, slots=True)
class Team(Model):
    team: int
    name: str
    state: Optional[str] = None
    country: Optional[str] = None
    district: Optional[str] = None
    active: Optional[bool] = None

    # epa: Optional[float] = None
    # epa_recent: Optional[float] = None
    # epa_mean: Optional[float] = None
    # epa_max: Optional[float] = None

    # TODO: populate Team Model in post_process_epa
    wins: int = 0
    losses: int = 0
    ties: int = 0
    count: int = 0
    winrate: float = 0

    @classmethod
    def from_dict(cls, dict: Dict[str, Any]) -> "Team":
        dict = {k: dict.get(k, None) for k in cls.__slots__}  # type: ignore
        return Team(**dict)