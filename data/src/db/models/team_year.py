from typing import Any, Dict, Optional, Tuple

import attr
from sqlalchemy import Column, Float, Integer
from sqlalchemy.sql.schema import ForeignKeyConstraint, PrimaryKeyConstraint
from sqlalchemy.sql.sqltypes import String

from db.main import Base
from db.models.main import Model, ModelORM


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

    """OPR"""
    opr = Column(Float)
    opr_start = Column(Float)
    opr_end = Column(Float)

    opr_auto = Column(Float)
    opr_teleop = Column(Float)
    opr_1 = Column(Float)
    opr_2 = Column(Float)
    opr_endgame = Column(Float)
    opr_fouls = Column(Float)
    opr_no_fouls = Column(Float)

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
    opr_rank = Column(Integer)
    opr_percentile = Column(Float)


@attr.s(auto_attribs=True, slots=True)
class TeamYear(Model):
    id: int
    year: int
    team: int

    name: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    district: Optional[str] = None
    opr: Optional[float] = None

    elo_start: Optional[float] = None
    elo_pre_champs: Optional[float] = None
    elo_end: Optional[float] = None
    elo_mean: Optional[float] = None
    elo_max: Optional[float] = None
    elo_diff: Optional[float] = None

    opr_start: Optional[float] = None
    opr_end: Optional[float] = None
    opr_auto: Optional[float] = None
    opr_teleop: Optional[float] = None
    opr_1: Optional[float] = None
    opr_2: Optional[float] = None
    opr_endgame: Optional[float] = None
    opr_fouls: Optional[float] = None
    opr_no_fouls: Optional[float] = None
    ils_1: Optional[float] = None
    ils_2: Optional[float] = None

    wins: Optional[int] = None
    losses: Optional[int] = None
    ties: Optional[int] = None
    count: Optional[int] = None
    winrate: Optional[float] = None

    elo_rank: Optional[int] = None
    elo_percentile: Optional[float] = None
    opr_rank: Optional[int] = None
    opr_percentile: Optional[float] = None

    @classmethod
    def from_dict(cls, dict: Dict[str, Any]) -> "TeamYear":
        dict = {k: dict.get(k, None) for k in cls.__slots__}
        return TeamYear(**dict)

    """SUPER FUNCTIONS"""

    def sort(self) -> Tuple[int, int]:
        return self.team, self.year
