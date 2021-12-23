from dataclasses import dataclass, fields
from typing import Any, Dict, Optional

from sqlalchemy import Column, Float, Integer, String

from db.main import Base
from db.models.main import Model, ModelORM


class TeamORM(Base, ModelORM):
    """DECLARATION"""

    __tablename__ = "teams"
    id: Column[int] = Column(Integer, primary_key=True, index=True)

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


@dataclass
class Team(Model):
    id: int
    name: str
    state: Optional[str] = None
    country: Optional[str] = None
    district: Optional[str] = None
    active: int = 1
    elo: float = -1
    elo_recent: float = -1
    elo_mean: float = -1
    elo_max: float = -1
    wins: int = 0
    losses: int = 0
    ties: int = 0
    count: int = 0
    winrate: float = 0

    @classmethod
    def from_dict(cls, dict: Dict[str, Any]) -> "Team":
        class_fields = {f.name for f in fields(cls)}
        return Team(**{k: v for k, v in dict.items() if k in class_fields})

    """SUPER FUNCTIONS"""

    def __lt__(self, other: "TeamORM"):
        return self.id < other.id

    def __repr__(self) -> str:
        return f"Team ({self.id})"

    def isActive(self) -> bool:
        return self.active == 1
