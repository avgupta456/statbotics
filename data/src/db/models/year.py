from dataclasses import dataclass, fields
from typing import Any, Dict

from sqlalchemy import Column, Float, Integer

from db.main import Base
from db.models.main import Model, ModelORM


class YearORM(Base, ModelORM):
    """DECLARATION"""

    __tablename__ = "years"
    id: Column[int] = Column(Integer, primary_key=True, index=True)

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


@dataclass
class Year(Model):
    id: int
    elo_max: float = -1
    elo_1p: float = -1
    elo_5p: float = -1
    elo_10p: float = -1
    elo_25p: float = -1
    elo_median: float = -1
    elo_mean: float = -1
    elo_sd: float = -1
    elo_acc: float = -1
    elo_mse: float = -1

    opr_max: float = -1
    opr_1p: float = -1
    opr_5p: float = -1
    opr_10p: float = -1
    opr_25p: float = -1
    opr_median: float = -1
    opr_mean: float = -1
    opr_sd: float = -1
    opr_acc: float = -1
    opr_mse: float = -1

    mix_acc: float = -1
    mix_mse: float = -1

    rp1_acc: float = -1
    rp1_mse: float = -1
    rp2_acc: float = -1
    rp2_mse: float = -1

    score_mean: float = -1
    score_sd: float = -1
    auto_mean: float = -1
    teleop_mean: float = -1
    one_mean: float = -1
    two_mean: float = -1
    endgame_mean: float = -1
    fouls_mean: float = -1
    no_fouls_mean: float = -1
    rp_1_mean: float = -1
    rp_2_mean: float = -1

    @classmethod
    def from_dict(cls, dict: Dict[str, Any]) -> "Year":
        class_fields = {f.name for f in fields(cls)}
        return Year(**{k: v for k, v in dict.items() if k in class_fields})

    """SUPER FUNCTIONS"""

    def __lt__(self, other: "Year") -> bool:
        return self.id < other.id

    def __repr__(self) -> str:
        return f"Year ({self.id})"
