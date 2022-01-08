import attr
from typing import Any, Dict, Optional

from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.sql.schema import PrimaryKeyConstraint

from db.main import Base
from db.models.main import Model, ModelORM


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
    active = Column(Integer)

    """ELO"""
    elo = Column(Float)
    elo_recent = Column(Float)
    elo_mean = Column(Float)
    elo_max = Column(Float)

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
    active: Optional[int] = None
    elo: Optional[float] = None
    elo_recent: Optional[float] = None
    elo_mean: Optional[float] = None
    elo_max: Optional[float] = None
    wins: Optional[int] = None
    losses: Optional[int] = None
    ties: Optional[int] = None
    count: Optional[int] = None
    winrate: Optional[float] = None

    @classmethod
    def from_dict(cls, dict: Dict[str, Any]) -> "Team":
        dict = {k: dict.get(k, None) for k in cls.__slots__}
        return Team(**dict)
