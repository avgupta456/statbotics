import attr
from typing import Any, Dict, Optional

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


@attr.s(auto_attribs=True, slots=True)
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

    elo_max: Optional[float] = None
    elo_top8: Optional[float] = None
    elo_top24: Optional[float] = None
    elo_mean: Optional[float] = None
    elo_sd: Optional[float] = None

    opr_max: Optional[float] = None
    opr_top8: Optional[float] = None
    opr_top24: Optional[float] = None
    opr_mean: Optional[float] = None
    opr_sd: Optional[float] = None

    elo_acc: Optional[float] = None
    elo_mse: Optional[float] = None
    opr_acc: Optional[float] = None
    opr_mse: Optional[float] = None
    mix_acc: Optional[float] = None
    mix_mse: Optional[float] = None

    rp1_acc: Optional[float] = None
    rp1_mse: Optional[float] = None
    rp2_acc: Optional[float] = None
    rp2_mse: Optional[float] = None

    @classmethod
    def from_dict(cls, dict: Dict[str, Any]) -> "Event":
        dict = {k: dict.get(k, None) for k in cls.__slots__}
        return Event(**dict)
