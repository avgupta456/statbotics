from typing import Any, Dict, List, Optional

import attr
from sqlalchemy import Boolean, Column, Float, Integer, String
from sqlalchemy.sql.schema import ForeignKeyConstraint, PrimaryKeyConstraint

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
    comp_level = Column(String(10))
    set_number = Column(Integer)
    match_number = Column(Integer)

    # Choices are 'Upcoming', 'Completed'
    status = Column(String(10))

    red = Column(String(20))
    red_elo_sum = Column(Float)
    red_ils_1_sum = Column(Float)
    red_ils_2_sum = Column(Float)

    blue = Column(String(20))
    blue_elo_sum = Column(Float)
    blue_ils_1_sum = Column(Float)
    blue_ils_2_sum = Column(Float)

    winner = Column(String(10))
    elo_winner = Column(String(10))
    elo_win_prob = Column(Float)
    red_rp_1_prob = Column(Float)
    red_rp_2_prob = Column(Float)
    blue_rp_1_prob = Column(Float)
    blue_rp_2_prob = Column(Float)

    playoff = Column(Boolean)
    time = Column(Integer)

    red_score = Column(Integer)
    blue_score = Column(Integer)

    red_auto = Column(Integer)
    red_auto_movement = Column(Integer)
    red_auto_1 = Column(Integer)
    red_auto_2 = Column(Integer)
    red_teleop_1 = Column(Integer)
    red_teleop_2 = Column(Integer)
    red_1 = Column(Integer)
    red_2 = Column(Integer)
    red_teleop = Column(Integer)
    red_endgame = Column(Integer)
    red_no_fouls = Column(Integer)
    red_fouls = Column(Integer)
    red_rp_1 = Column(Integer)
    red_rp_2 = Column(Integer)

    blue_auto = Column(Integer)
    blue_auto_movement = Column(Integer)
    blue_auto_1 = Column(Integer)
    blue_auto_2 = Column(Integer)
    blue_teleop_1 = Column(Integer)
    blue_teleop_2 = Column(Integer)
    blue_1 = Column(Integer)
    blue_2 = Column(Integer)
    blue_teleop = Column(Integer)
    blue_endgame = Column(Integer)
    blue_no_fouls = Column(Integer)
    blue_fouls = Column(Integer)
    blue_rp_1 = Column(Integer)
    blue_rp_2 = Column(Integer)


@attr.s(auto_attribs=True, slots=True)
class Match(Model):
    key: str
    year: int
    event: str

    comp_level: str
    set_number: int
    match_number: int
    status: str

    red: Optional[str] = None
    red_elo_sum: Optional[float] = None
    red_ils_1_sum: Optional[float] = None
    red_ils_2_sum: Optional[float] = None

    blue: Optional[str] = None
    blue_elo_sum: Optional[float] = None
    blue_ils_1_sum: Optional[float] = None
    blue_ils_2_sum: Optional[float] = None

    winner: Optional[str] = None
    elo_winner: Optional[str] = None
    elo_win_prob: Optional[float] = None
    red_rp_1_prob: Optional[float] = None
    red_rp_2_prob: Optional[float] = None
    blue_rp_1_prob: Optional[float] = None
    blue_rp_2_prob: Optional[float] = None

    playoff: bool = False
    time: Optional[int] = None

    red_score: Optional[int] = None
    blue_score: Optional[int] = None

    red_auto: Optional[int] = None
    red_auto_movement: Optional[int] = None
    red_auto_1: Optional[int] = None
    red_auto_2: Optional[int] = None
    red_teleop_1: Optional[int] = None
    red_teleop_2: Optional[int] = None
    red_1: Optional[int] = None
    red_2: Optional[int] = None
    red_teleop: Optional[int] = None
    red_endgame: Optional[int] = None
    red_no_fouls: Optional[int] = None
    red_fouls: Optional[int] = None
    red_rp_1: Optional[int] = None
    red_rp_2: Optional[int] = None

    blue_auto: Optional[int] = None
    blue_auto_movement: Optional[int] = None
    blue_auto_1: Optional[int] = None
    blue_auto_2: Optional[int] = None
    blue_teleop_1: Optional[int] = None
    blue_teleop_2: Optional[int] = None
    blue_1: Optional[int] = None
    blue_2: Optional[int] = None
    blue_teleop: Optional[int] = None
    blue_endgame: Optional[int] = None
    blue_no_fouls: Optional[int] = None
    blue_fouls: Optional[int] = None
    blue_rp_1: Optional[int] = None
    blue_rp_2: Optional[int] = None

    @classmethod
    def from_dict(cls, dict: Dict[str, Any]) -> "Match":
        dict = {k: dict.get(k, None) for k in cls.__slots__}  # type: ignore
        return Match(**dict)

    """SUPER FUNCTIONS"""

    def sort(self) -> int:
        return self.time or 0

    def get_red(self) -> List[int]:
        if self.red is None:
            return []
        return [int(x) for x in self.red.split(",")]

    def get_blue(self) -> List[int]:
        if self.blue is None:
            return []
        return [int(x) for x in self.blue.split(",")]

    def get_teams(self) -> List[List[int]]:
        return [self.get_red(), self.get_blue()]
