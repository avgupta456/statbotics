from typing import Any, Dict, List, Optional

import attr
from sqlalchemy import Boolean, Column, Float, Integer, String  # type: ignore
from sqlalchemy.sql.schema import (  # type: ignore
    ForeignKeyConstraint,
    PrimaryKeyConstraint,
)

from src.db.main import Base
from src.db.models.main import Model, ModelORM


class MatchORM(Base, ModelORM):
    """DECLARATION"""

    __tablename__ = "matches"
    key = Column(String(20), index=True)
    year = Column(Integer, index=True)
    event = Column(String(20), index=True)

    PrimaryKeyConstraint(key)
    ForeignKeyConstraint(["year"], ["years.year"])
    ForeignKeyConstraint(["event"], ["events.key"])

    """GENERAL"""
    offseason = Column(Boolean, index=True)
    week = Column(Integer, index=True)
    playoff = Column(Boolean, index=True)

    comp_level = Column(String(10))
    set_number = Column(Integer)
    match_number = Column(Integer)

    time = Column(Integer)  # Enforces ordering
    predicted_time = Column(Integer)  # For display

    # Choices are 'Upcoming', 'Completed'
    status = Column(String(10), index=True)
    video = Column(String(20))

    # Different than dq/surrogate to allow for easier querying
    red_1 = Column(Integer, index=True)
    red_2 = Column(Integer, index=True)
    red_3 = Column(Integer, index=True)
    red_dq = Column(String(20))
    red_surrogate = Column(String(20))

    blue_1 = Column(Integer, index=True)
    blue_2 = Column(Integer, index=True)
    blue_3 = Column(Integer, index=True)
    blue_dq = Column(String(20))
    blue_surrogate = Column(String(20))

    """EPA"""
    red_epa_sum = Column(Float)
    red_rp_1_epa_sum = Column(Float)
    red_rp_2_epa_sum = Column(Float)

    blue_epa_sum = Column(Float)
    blue_rp_1_epa_sum = Column(Float)
    blue_rp_2_epa_sum = Column(Float)

    epa_winner = Column(String(10))
    epa_win_prob = Column(Float)
    red_rp_1_prob = Column(Float)
    red_rp_2_prob = Column(Float)
    blue_rp_1_prob = Column(Float)
    blue_rp_2_prob = Column(Float)

    """OUTCOME"""
    winner = Column(String(10))

    red_score = Column(Integer)
    red_no_foul = Column(Integer)
    red_rp_1 = Column(Integer)
    red_rp_2 = Column(Integer)
    red_tiebreaker = Column(Integer)

    blue_score = Column(Integer)
    blue_no_foul = Column(Integer)
    blue_rp_1 = Column(Integer)
    blue_rp_2 = Column(Integer)
    blue_tiebreaker = Column(Integer)


@attr.s(auto_attribs=True, slots=True)
class Match(Model):
    key: str
    year: int
    event: str

    """GENERAL"""
    offseason: bool
    week: int
    playoff: bool

    comp_level: str
    set_number: int
    match_number: int

    time: int
    predicted_time: int

    status: str
    video: Optional[str] = None

    red_1: Optional[int] = None
    red_2: Optional[int] = None
    red_3: Optional[int] = None
    red_dq: Optional[str] = None
    red_surrogate: Optional[str] = None

    blue_1: Optional[int] = None
    blue_2: Optional[int] = None
    blue_3: Optional[int] = None
    blue_dq: Optional[str] = None
    blue_surrogate: Optional[str] = None

    """EPA"""
    red_epa_sum: Optional[float] = None
    red_rp_1_epa_sum: Optional[float] = None
    red_rp_2_epa_sum: Optional[float] = None

    blue_epa_sum: Optional[float] = None
    blue_rp_1_epa_sum: Optional[float] = None
    blue_rp_2_epa_sum: Optional[float] = None

    epa_winner: Optional[str] = None
    epa_win_prob: Optional[float] = None
    red_rp_1_prob: Optional[float] = None
    red_rp_2_prob: Optional[float] = None
    blue_rp_1_prob: Optional[float] = None
    blue_rp_2_prob: Optional[float] = None

    """OUTCOME"""
    winner: Optional[str] = None

    red_score: Optional[int] = None
    red_no_foul: Optional[int] = None
    red_rp_1: Optional[int] = None
    red_rp_2: Optional[int] = None
    red_tiebreaker: Optional[int] = None

    blue_score: Optional[int] = None
    blue_no_foul: Optional[int] = None
    blue_rp_1: Optional[int] = None
    blue_rp_2: Optional[int] = None
    blue_tiebreaker: Optional[int] = None

    @classmethod
    def from_dict(cls, dict: Dict[str, Any]) -> "Match":
        dict = {k: dict.get(k, None) for k in cls.__slots__}  # type: ignore
        return Match(**dict)

    def as_dict(self: "Match") -> Dict[str, Any]:
        return attr.asdict(self)

    """SUPER FUNCTIONS"""

    def sort(self) -> int:
        return self.time or 0

    def get_red(self) -> List[int]:
        return [x for x in [self.red_1, self.red_2, self.red_3] if x is not None]

    def get_blue(self) -> List[int]:
        return [x for x in [self.blue_1, self.blue_2, self.blue_3] if x is not None]

    def get_red_surrogates(self) -> List[int]:
        if self.red_surrogate is None:
            return []
        return [int(x) for x in self.red_surrogate.split(",") if x != ""]

    def get_blue_surrogates(self) -> List[int]:
        if self.blue_surrogate is None:
            return []
        return [int(x) for x in self.blue_surrogate.split(",") if x != ""]

    def get_red_dqs(self) -> List[int]:
        if self.red_dq is None:
            return []
        return [int(x) for x in self.red_dq.split(",") if x != ""]

    def get_blue_dqs(self) -> List[int]:
        if self.blue_dq is None:
            return []
        return [int(x) for x in self.blue_dq.split(",") if x != ""]

    def get_teams(self) -> List[List[int]]:
        return [self.get_red(), self.get_blue()]

    # TODO: consolidate with as_dict()
    def to_dict(self) -> Dict[str, Any]:
        out: Dict[str, Any] = {k: getattr(self, k) for k in self.__slots__}  # type: ignore
        out["red"] = self.get_red()
        out["blue"] = self.get_blue()
        return out

    def __str__(self: "Match"):
        # Only refresh DB if these change (during 1 min partial update)
        return f"{self.key}_{self.status}_{self.red_score}_{self.blue_score}_{self.red_epa_sum}_{self.blue_epa_sum}_{self.predicted_time}"
