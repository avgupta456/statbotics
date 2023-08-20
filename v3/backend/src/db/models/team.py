from typing import Any, Dict, Optional

import attr
from sqlalchemy import Boolean, Column, Float, Integer, String  # type: ignore
from sqlalchemy.sql.schema import PrimaryKeyConstraint  # type: ignore

from src.db.main import Base
from src.db.models.main import ModelORM, generate_attr_class


class TeamORM(Base, ModelORM):
    """DECLARATION"""

    __tablename__ = "teams"
    team: str = Column(String(6), index=True)

    PrimaryKeyConstraint(team)

    """GENERAL"""
    name: str = Column(String(100))
    offseason: bool = Column(Boolean)
    country: Optional[str] = Column(String(30))
    district: Optional[str] = Column(String(10))
    state: Optional[str] = Column(String(10))
    rookie_year: int = Column(Integer)
    active: bool = Column(Boolean)

    """EPA"""
    norm_epa: Optional[float] = Column(Float)
    norm_epa_recent: Optional[float] = Column(Float)
    norm_epa_mean: Optional[float] = Column(Float)
    norm_epa_max: Optional[float] = Column(Float)

    """STATS"""
    wins: int = Column(Integer)
    losses: int = Column(Integer)
    ties: int = Column(Integer)
    count: int = Column(Integer)
    winrate: float = Column(Float)

    full_wins: int = Column(Integer)
    full_losses: int = Column(Integer)
    full_ties: int = Column(Integer)
    full_count: int = Column(Integer)
    full_winrate: float = Column(Float)


_Team = generate_attr_class("Team", TeamORM)


class Team(_Team):
    @classmethod
    def from_dict(cls, dict: Dict[str, Any]) -> "Team":
        dict = {k: dict.get(k, None) for k in cls.__slots__}  # type: ignore
        return Team(**dict)

    def as_dict(self: "Team") -> Dict[str, Any]:
        return attr.asdict(self)  # type: ignore

    def __str__(self: Any):
        # Only refresh DB if these change (during 1 min partial update)
        return f"{self.team}_{self.count}"
