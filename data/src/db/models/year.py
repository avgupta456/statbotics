import attr
from typing import Any, Dict, Optional

from sqlalchemy import Column, Float, Integer

from db.main import Base
from db.models.main import Model, ModelORM


class YearORM(Base, ModelORM):
    """DECLARATION"""

    __tablename__ = "years"
    year: Column[int] = Column(Integer, primary_key=True, index=True)

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

    """OPR"""
    # stats are for team's max opr in given year
    opr_max = Column(Float)
    opr_1p = Column(Float)
    opr_5p = Column(Float)
    opr_10p = Column(Float)
    opr_25p = Column(Float)
    opr_median = Column(Float)
    opr_mean = Column(Float)
    opr_sd = Column(Float)
    opr_acc = Column(Float)
    opr_mse = Column(Float)

    """'MIX"""
    mix_acc = Column(Float)
    mix_mse = Column(Float)

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

    opr_max: Optional[float] = None
    opr_1p: Optional[float] = None
    opr_5p: Optional[float] = None
    opr_10p: Optional[float] = None
    opr_25p: Optional[float] = None
    opr_median: Optional[float] = None
    opr_mean: Optional[float] = None
    opr_sd: Optional[float] = None
    opr_acc: Optional[float] = None
    opr_mse: Optional[float] = None

    mix_acc: Optional[float] = None
    mix_mse: Optional[float] = None

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
        dict = {k: dict.get(k, None) for k in cls.__slots__}
        return Year(**dict)
