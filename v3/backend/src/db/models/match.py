from typing import Any, Dict, List, Optional

import attr
from sqlalchemy import Boolean, Column, Float, Integer, String  # type: ignore
from sqlalchemy.sql.schema import (  # type: ignore
    ForeignKeyConstraint,
    PrimaryKeyConstraint,
)

from src.db.main import Base
from src.db.models.main import ModelORM, generate_attr_class


class MatchORM(Base, ModelORM):
    """DECLARATION"""

    __tablename__ = "matches"
    key: str = Column(String(20), index=True)
    year: int = Column(Integer, index=True)
    event: str = Column(String(20), index=True)

    PrimaryKeyConstraint(key)
    ForeignKeyConstraint(["year"], ["years.year"])
    ForeignKeyConstraint(["event"], ["events.key"])

    """GENERAL"""
    offseason: bool = Column(Boolean, index=True)
    week: int = Column(Integer, index=True)
    playoff: bool = Column(Boolean, index=True)

    comp_level: str = Column(String(10))
    set_number: int = Column(Integer)
    match_number: int = Column(Integer)

    time: int = Column(Integer)  # Enforces ordering
    predicted_time: int = Column(Integer)  # For display

    # Choices are 'Upcoming', 'Completed'
    status: str = Column(String(10), index=True)
    video: str = Column(String(20))

    # Different than dq/surrogate to allow for easier querying
    red_1: str = Column(String(6), index=True)
    red_2: str = Column(String(6), index=True)
    red_3: Optional[str] = Column(String(6), index=True)
    red_dq: str = Column(String(20))
    red_surrogate: str = Column(String(20))

    blue_1: str = Column(String(6), index=True)
    blue_2: str = Column(String(6), index=True)
    blue_3: Optional[str] = Column(String(6), index=True)
    blue_dq: str = Column(String(20))
    blue_surrogate: str = Column(String(20))

    """EPA"""
    red_epa_sum: float = Column(Float)
    red_rp_1_epa_sum: float = Column(Float)
    red_rp_2_epa_sum: float = Column(Float)

    blue_epa_sum: float = Column(Float)
    blue_rp_1_epa_sum: float = Column(Float)
    blue_rp_2_epa_sum: float = Column(Float)

    epa_winner: str = Column(String(10))
    epa_win_prob: float = Column(Float)
    red_rp_1_prob: float = Column(Float)
    red_rp_2_prob: float = Column(Float)
    blue_rp_1_prob: float = Column(Float)
    blue_rp_2_prob: float = Column(Float)

    """OUTCOME"""
    winner: Optional[str] = Column(String(10))

    red_score: Optional[int] = Column(Integer)
    red_no_foul: Optional[int] = Column(Integer)
    red_rp_1: Optional[int] = Column(Integer)
    red_rp_2: Optional[int] = Column(Integer)
    red_tiebreaker: Optional[int] = Column(Integer)

    blue_score: Optional[int] = Column(Integer)
    blue_no_foul: Optional[int] = Column(Integer)
    blue_rp_1: Optional[int] = Column(Integer)
    blue_rp_2: Optional[int] = Column(Integer)
    blue_tiebreaker: Optional[int] = Column(Integer)


_Match = generate_attr_class("Match", MatchORM)


class Match(_Match):
    @classmethod
    def from_dict(cls, dict: Dict[str, Any]) -> "Match":
        dict = {k: dict.get(k, None) for k in cls.__slots__}  # type: ignore
        return Match(**dict)

    def as_dict(self: "Match") -> Dict[str, Any]:
        return attr.asdict(self)

    """SUPER FUNCTIONS"""

    def sort(self: "Match") -> int:
        return self.time or 0

    def get_red(self: "Match") -> List[str]:
        return [x for x in [self.red_1, self.red_2, self.red_3] if x is not None]

    def get_blue(self: "Match") -> List[str]:
        return [x for x in [self.blue_1, self.blue_2, self.blue_3] if x is not None]

    def get_red_surrogates(self: "Match") -> List[str]:
        return [x for x in self.red_surrogate.split(",") if x != ""]

    def get_blue_surrogates(self: "Match") -> List[str]:
        return [x for x in self.blue_surrogate.split(",") if x != ""]

    def get_red_dqs(self: "Match") -> List[str]:
        return [x for x in self.red_dq.split(",") if x != ""]

    def get_blue_dqs(self: "Match") -> List[str]:
        return [x for x in self.blue_dq.split(",") if x != ""]

    def get_teams(self: "Match") -> List[List[str]]:
        return [self.get_red(), self.get_blue()]

    # TODO: consolidate with as_dict()
    def to_dict(self: "Match") -> Dict[str, Any]:
        out: Dict[str, Any] = {k: getattr(self, k) for k in self.__slots__}  # type: ignore
        out["red"] = self.get_red()
        out["blue"] = self.get_blue()
        return out

    def __str__(self: "Match"):
        # Only refresh DB if these change (during 1 min partial update)
        return f"{self.key}_{self.status}_{self.red_score}_{self.blue_score}_{self.red_epa_sum}_{self.blue_epa_sum}_{self.predicted_time}"
