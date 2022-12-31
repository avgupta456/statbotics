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
    rookie_year = Column(Integer)
    active = Column(Boolean)

    """EPA"""
    norm_epa = Column(Float)
    norm_epa_recent = Column(Float)
    norm_epa_mean = Column(Float)
    norm_epa_max = Column(Float)

    """STATS"""
    wins = Column(Integer)
    losses = Column(Integer)
    ties = Column(Integer)
    count = Column(Integer)
    winrate = Column(Float)

    full_wins = Column(Integer)
    full_losses = Column(Integer)
    full_ties = Column(Integer)
    full_count = Column(Integer)
    full_winrate = Column(Float)


@attr.s(auto_attribs=True, slots=True)
class Team(Model):
    team: int
    name: str
    state: Optional[str] = None
    country: Optional[str] = None
    district: Optional[str] = None
    rookie_year: Optional[int] = None
    active: Optional[bool] = None

    norm_epa: Optional[float] = None
    norm_epa_recent: Optional[float] = None
    norm_epa_mean: Optional[float] = None
    norm_epa_max: Optional[float] = None

    wins: int = 0
    losses: int = 0
    ties: int = 0
    count: int = 0
    winrate: float = 0

    full_wins: int = 0
    full_losses: int = 0
    full_ties: int = 0
    full_count: int = 0
    full_winrate: float = 0

    @classmethod
    def from_dict(cls, dict: Dict[str, Any]) -> "Team":
        dict = {k: dict.get(k, None) for k in cls.__slots__}  # type: ignore
        return Team(**dict)
