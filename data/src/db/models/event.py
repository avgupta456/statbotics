from dataclasses import dataclass, fields
from typing import Any, Dict

from sqlalchemy import Column, Float, ForeignKey, Integer, String

from db.main import Base
from db.models.main import Model, ModelORM


class EventORM(Base, ModelORM):
    """DECLARATION"""

    __tablename__ = "events"
    id: Column[int] = Column(Integer, primary_key=True, index=True)
    year_id: Column[int] = Column(Integer, ForeignKey("years.id"), index=True)

    """GENERAL"""
    key = Column(String(20))
    name = Column(String(100))
    time = Column(Integer)
    state = Column(String(10))
    country = Column(String(30))
    district = Column(String(10))

    # 0 is regional, 1 is district, 2 is district champ,
    # 3 is worlds division, 4 is einsteins/FOC
    type = Column(Integer)
    week = Column(Integer)

    """ELO"""
    elo_max = Column(Float)
    elo_top8 = Column(Float)
    elo_top24 = Column(Float)
    elo_mean = Column(Float)
    elo_sd = Column(Float)

    """OPR"""
    opr_max = Column(Float)
    opr_top8 = Column(Float)
    opr_top24 = Column(Float)
    opr_mean = Column(Float)
    opr_sd = Column(Float)

    """STATS"""
    elo_acc = Column(Float)
    elo_mse = Column(Float)

    opr_acc = Column(Float)
    opr_mse = Column(Float)

    mix_acc = Column(Float)
    mix_mse = Column(Float)

    rp1_acc = Column(Float)
    rp1_mse = Column(Float)
    rp2_acc = Column(Float)
    rp2_mse = Column(Float)


@dataclass
class Event(Model):
    id: int
    year_id: int

    key: str
    name: str
    time: int
    state: str
    country: str
    district: str
    type: int
    week: int

    elo_max: float = -1
    elo_top8: float = -1
    elo_top24: float = -1
    elo_mean: float = -1
    elo_sd: float = -1

    opr_max: float = -1
    opr_top8: float = -1
    opr_top24: float = -1
    opr_mean: float = -1
    opr_sd: float = -1

    elo_acc: float = -1
    elo_mse: float = -1
    opr_acc: float = -1
    opr_mse: float = -1
    mix_acc: float = -1
    mix_mse: float = -1

    rp1_acc: float = -1
    rp1_mse: float = -1
    rp2_acc: float = -1
    rp2_mse: float = -1

    @classmethod
    def from_dict(cls, dict: Dict[str, Any]) -> "Event":
        class_fields = {f.name for f in fields(cls)}
        return Event(**{k: v for k, v in dict.items() if k in class_fields})

    """SUPER FUNCTIONS"""

    def __lt__(self, other: "Event") -> bool:
        return self.time < other.time

    def __repr__(self) -> str:
        return "(Event " + str(self.key) + ")"
