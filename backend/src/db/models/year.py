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

    """EPA"""
    epa_max = Column(Float)
    epa_1p = Column(Float)
    epa_5p = Column(Float)
    epa_10p = Column(Float)
    epa_25p = Column(Float)
    epa_median = Column(Float)
    epa_mean = Column(Float)
    epa_sd = Column(Float)

    epa_quals_acc = Column(Float)
    epa_quals_mse = Column(Float)
    quals_count = Column(Integer)
    epa_elims_acc = Column(Float)
    epa_elims_mse = Column(Float)
    elims_count = Column(Integer)
    epa_champs_acc = Column(Float)
    epa_champs_mse = Column(Float)
    champs_count = Column(Integer)
    epa_acc = Column(Float)
    epa_mse = Column(Float)
    count = Column(Integer)

    """ILS"""
    # rp1_acc = Column(Float)
    # rp1_mse = Column(Float)
    # rp2_acc = Column(Float)
    # rp2_mse = Column(Float)

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
    epa_max: Optional[float] = None
    epa_1p: Optional[float] = None
    epa_5p: Optional[float] = None
    epa_10p: Optional[float] = None
    epa_25p: Optional[float] = None
    epa_median: Optional[float] = None
    epa_mean: Optional[float] = None
    epa_sd: Optional[float] = None

    epa_quals_acc: Optional[float] = None
    epa_quals_mse: Optional[float] = None
    quals_count: Optional[int] = None
    epa_elims_acc: Optional[float] = None
    epa_elims_mse: Optional[float] = None
    elims_count: Optional[int] = None
    epa_champs_acc: Optional[float] = None
    epa_champs_mse: Optional[float] = None
    champs_count: Optional[int] = None
    epa_acc: Optional[float] = None
    epa_mse: Optional[float] = None
    count: Optional[int] = None

    # rp1_acc: Optional[float] = None
    # rp1_mse: Optional[float] = None
    # rp2_acc: Optional[float] = None
    # rp2_mse: Optional[float] = None

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
