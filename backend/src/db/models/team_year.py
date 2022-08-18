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

    """EPA"""
    epa_start = Column(Float)
    epa_pre_champs = Column(Float)
    epa_end = Column(Float)
    epa_mean = Column(Float)
    epa_max = Column(Float)
    epa_diff = Column(Float)

    """ILS"""
    # ils_1 = Column(Float)
    # ils_2 = Column(Float)

    """STATS"""
    wins = Column(Integer)
    losses = Column(Integer)
    ties = Column(Integer)
    count = Column(Integer)
    winrate = Column(Float)

    epa_rank = Column(Integer)
    epa_percentile = Column(Float)


@attr.s(auto_attribs=True, slots=True)
class TeamYear(Model):
    id: int
    year: int
    team: int

    name: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    district: Optional[str] = None

    epa_start: Optional[float] = None
    epa_pre_champs: Optional[float] = None
    epa_end: Optional[float] = None
    epa_mean: Optional[float] = None
    epa_max: Optional[float] = None
    epa_diff: Optional[float] = None

    # ils_1: Optional[float] = None
    # ils_2: Optional[float] = None

    wins: int = 0
    losses: int = 0
    ties: int = 0
    count: int = 0
    winrate: float = 0

    epa_rank: Optional[int] = None
    epa_percentile: Optional[float] = None

    @classmethod
    def from_dict(cls, dict: Dict[str, Any]) -> "TeamYear":
        dict = {k: dict.get(k, None) for k in cls.__slots__}  # type: ignore
        return TeamYear(**dict)

    """SUPER FUNCTIONS"""

    def sort(self) -> Tuple[int, int]:
        return self.team, self.year
