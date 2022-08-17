from typing import Any, Dict, Optional

import attr
from sqlalchemy import Column, Float, Integer
from sqlalchemy.sql.schema import PrimaryKeyConstraint

from src.db.main import Base
from src.db.models.main import Model, ModelORM


class YearORM(Base, ModelORM):
    """DECLARATION"""

    __tablename__ = "years"
    year = Column(Integer, index=True)

    PrimaryKeyConstraint(year)

    """ELO"""
    elo_max = Column(Float)
    elo_1p = Column(Float)
    elo_5p = Column(Float)
    elo_10p = Column(Float)
    elo_25p = Column(Float)
    elo_median = Column(Float)
    elo_mean = Column(Float)
    elo_sd = Column(Float)
    elo_acc = Column(Float)
    elo_mse = Column(Float)

    """ILS"""
    rp1_acc = Column(Float)
    rp1_mse = Column(Float)
    rp2_acc = Column(Float)
    rp2_mse = Column(Float)

    """CONSTANTS"""
    score_mean = Column(Float)
    score_sd = Column(Float)
    auto_mean = Column(Float)
    teleop_mean = Column(Float)
    one_mean = Column(Float)
    two_mean = Column(Float)
    endgame_mean = Column(Float)
    fouls_mean = Column(Float)
    no_fouls_mean = Column(Float)
    rp_1_mean = Column(Float)
    rp_2_mean = Column(Float)


@attr.s(auto_attribs=True, slots=True)
class Year(Model):
    year: int
    elo_max: Optional[float] = None
    elo_1p: Optional[float] = None
    elo_5p: Optional[float] = None
    elo_10p: Optional[float] = None
    elo_25p: Optional[float] = None
    elo_median: Optional[float] = None
    elo_mean: Optional[float] = None
    elo_sd: Optional[float] = None
    elo_acc: Optional[float] = None
    elo_mse: Optional[float] = None

    rp1_acc: Optional[float] = None
    rp1_mse: Optional[float] = None
    rp2_acc: Optional[float] = None
    rp2_mse: Optional[float] = None

    score_mean: Optional[float] = None
    score_sd: Optional[float] = None
    auto_mean: Optional[float] = None
    teleop_mean: Optional[float] = None
    one_mean: Optional[float] = None
    two_mean: Optional[float] = None
    endgame_mean: Optional[float] = None
    fouls_mean: Optional[float] = None
    no_fouls_mean: Optional[float] = None
    rp_1_mean: Optional[float] = None
    rp_2_mean: Optional[float] = None

    @classmethod
    def from_dict(cls, dict: Dict[str, Any]) -> "Year":
        dict = {k: dict.get(k, None) for k in cls.__slots__}  # type: ignore
        return Year(**dict)
