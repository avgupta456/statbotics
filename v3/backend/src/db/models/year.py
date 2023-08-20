from typing import Any, Dict, Optional

from sqlalchemy import Column, Float, Integer  # type: ignore
from sqlalchemy.sql.schema import PrimaryKeyConstraint  # type: ignore

from src.db.main import Base
from src.db.models.main import ModelORM, generate_attr_class


class YearORM(Base, ModelORM):
    """DECLARATION"""

    __tablename__ = "years"
    year: int = Column(Integer, index=True)

    PrimaryKeyConstraint(year)

    """EPA"""
    epa_1p: float = Column(Float)
    epa_10p: float = Column(Float)
    epa_25p: float = Column(Float)
    epa_75p: float = Column(Float)

    auto_epa_1p: float = Column(Float)
    auto_epa_10p: float = Column(Float)
    auto_epa_25p: float = Column(Float)
    auto_epa_75p: float = Column(Float)

    teleop_epa_max: float = Column(Float)
    teleop_epa_1p: float = Column(Float)
    teleop_epa_10p: float = Column(Float)
    teleop_epa_25p: float = Column(Float)
    teleop_epa_75p: float = Column(Float)

    endgame_epa_1p: float = Column(Float)
    endgame_epa_10p: float = Column(Float)
    endgame_epa_25p: float = Column(Float)
    endgame_epa_75p: float = Column(Float)

    comp_1_epa_1p: float = Column(Float)
    comp_1_epa_10p: float = Column(Float)
    comp_1_epa_25p: float = Column(Float)
    comp_1_epa_75p: float = Column(Float)

    comp_2_epa_1p: float = Column(Float)
    comp_2_epa_10p: float = Column(Float)
    comp_2_epa_25p: float = Column(Float)
    comp_2_epa_75p: float = Column(Float)

    comp_3_epa_1p: float = Column(Float)
    comp_3_epa_10p: float = Column(Float)
    comp_3_epa_25p: float = Column(Float)
    comp_3_epa_75p: float = Column(Float)

    comp_4_epa_1p: float = Column(Float)
    comp_4_epa_10p: float = Column(Float)
    comp_4_epa_25p: float = Column(Float)
    comp_4_epa_75p: float = Column(Float)

    comp_5_epa_1p: float = Column(Float)
    comp_5_epa_10p: float = Column(Float)
    comp_5_epa_25p: float = Column(Float)
    comp_5_epa_75p: float = Column(Float)

    comp_6_epa_1p: float = Column(Float)
    comp_6_epa_10p: float = Column(Float)
    comp_6_epa_25p: float = Column(Float)
    comp_6_epa_75p: float = Column(Float)

    comp_7_epa_1p: float = Column(Float)
    comp_7_epa_10p: float = Column(Float)
    comp_7_epa_25p: float = Column(Float)
    comp_7_epa_75p: float = Column(Float)

    comp_8_epa_1p: float = Column(Float)
    comp_8_epa_10p: float = Column(Float)
    comp_8_epa_25p: float = Column(Float)
    comp_8_epa_75p: float = Column(Float)

    comp_9_epa_1p: float = Column(Float)
    comp_9_epa_10p: float = Column(Float)
    comp_9_epa_25p: float = Column(Float)
    comp_9_epa_75p: float = Column(Float)

    comp_10_epa_1p: float = Column(Float)
    comp_10_epa_10p: float = Column(Float)
    comp_10_epa_25p: float = Column(Float)
    comp_10_epa_75p: float = Column(Float)

    """WIN PROB"""
    epa_quals_acc: Optional[float] = Column(Float)
    epa_quals_mse: Optional[float] = Column(Float)
    quals_count: int = Column(Integer)
    epa_elims_acc: Optional[float] = Column(Float)
    epa_elims_mse: Optional[float] = Column(Float)
    elims_count: int = Column(Integer)
    epa_champs_acc: Optional[float] = Column(Float)
    epa_champs_mse: Optional[float] = Column(Float)
    champs_count: int = Column(Integer)
    epa_acc: Optional[float] = Column(Float)
    epa_mse: Optional[float] = Column(Float)
    count: int = Column(Integer)

    """RP PROB"""
    rp_1_champs_acc: Optional[float] = Column(Float)
    rp_1_champs_mse: Optional[float] = Column(Float)
    rp_2_champs_acc: Optional[float] = Column(Float)
    rp_2_champs_mse: Optional[float] = Column(Float)
    rp_champs_count: int = Column(Integer)
    rp_1_acc: Optional[float] = Column(Float)
    rp_1_mse: Optional[float] = Column(Float)
    rp_2_acc: Optional[float] = Column(Float)
    rp_2_mse: Optional[float] = Column(Float)
    rp_count: int = Column(Integer)

    """CONSTANTS"""
    # TODO: enforce consistent order of score mean, score sd, no_foul, foul, auto, teleop, endgame, rp_1, rp_2, comps
    score_mean: float = Column(Float)
    score_sd: float = Column(Float)
    foul_mean: Optional[float] = Column(Float)
    no_foul_mean: Optional[float] = Column(Float)
    auto_mean: Optional[float] = Column(Float)
    teleop_mean: Optional[float] = Column(Float)
    endgame_mean: Optional[float] = Column(Float)
    rp_1_mean: Optional[float] = Column(Float)
    rp_2_mean: Optional[float] = Column(Float)
    comp_1_mean: Optional[float] = Column(Float)
    comp_2_mean: Optional[float] = Column(Float)
    comp_3_mean: Optional[float] = Column(Float)
    comp_4_mean: Optional[float] = Column(Float)
    comp_5_mean: Optional[float] = Column(Float)
    comp_6_mean: Optional[float] = Column(Float)
    comp_7_mean: Optional[float] = Column(Float)
    comp_8_mean: Optional[float] = Column(Float)
    comp_9_mean: Optional[float] = Column(Float)
    comp_10_mean: Optional[float] = Column(Float)


_Year = generate_attr_class("Year", YearORM)


class Year(_Year):
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Year":
        dict = {k: data.get(k, None) for k in cls.__slots__}  # type: ignore
        return Year(**dict)

    def __str__(self: Any):
        # Only refresh DB if these change (during 1 min partial update)
        return f"{self.year}_{self.count}"
