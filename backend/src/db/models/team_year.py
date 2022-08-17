from typing import Any, Dict, Optional, Tuple

import attr
from sqlalchemy import Column, Float, Integer
from sqlalchemy.sql.schema import ForeignKeyConstraint, PrimaryKeyConstraint
from sqlalchemy.sql.sqltypes import String

from src.db.main import Base
from src.db.models.main import Model, ModelORM


class TeamYearORM(Base, ModelORM):
    """DECLARATION"""

    __tablename__ = "team_years"
    id = Column(Integer)  # placeholder for backend API
    year = Column(Integer, index=True)
    team = Column(Integer, index=True)

    # force unique (team, year)
    PrimaryKeyConstraint(team, year)
    ForeignKeyConstraint(["year"], ["years.year"])
    ForeignKeyConstraint(["team"], ["teams.team"])

    """API COMPLETENESS"""
    name = Column(String(100))
    state = Column(String(10))
    country = Column(String(30))
    district = Column(String(10))

    """ELO"""
    elo_start = Column(Float)
    elo_pre_champs = Column(Float)
    elo_end = Column(Float)
    elo_mean = Column(Float)
    elo_max = Column(Float)
    elo_diff = Column(Float)

    """ILS"""
    ils_1 = Column(Float)
    ils_2 = Column(Float)

    """STATS"""
    wins = Column(Integer)
    losses = Column(Integer)
    ties = Column(Integer)
    count = Column(Integer)
    winrate = Column(Float)

    elo_rank = Column(Integer)
    elo_percentile = Column(Float)


@attr.s(auto_attribs=True, slots=True)
class TeamYear(Model):
    id: int
    year: int
    team: int

    name: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    district: Optional[str] = None

    elo_start: Optional[float] = None
    elo_pre_champs: Optional[float] = None
    elo_end: Optional[float] = None
    elo_mean: Optional[float] = None
    elo_max: Optional[float] = None
    elo_diff: Optional[float] = None

    ils_1: Optional[float] = None
    ils_2: Optional[float] = None

    wins: int = 0
    losses: int = 0
    ties: int = 0
    count: int = 0
    winrate: float = 0

    elo_rank: Optional[int] = None
    elo_percentile: Optional[float] = None

    @classmethod
    def from_dict(cls, dict: Dict[str, Any]) -> "TeamYear":
        dict = {k: dict.get(k, None) for k in cls.__slots__}  # type: ignore
        return TeamYear(**dict)

    """SUPER FUNCTIONS"""

    def sort(self) -> Tuple[int, int]:
        return self.team, self.year
