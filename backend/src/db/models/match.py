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
    offseason = Column(Boolean)

    # Choices are 'Upcoming', 'Completed'
    status = Column(String(10))
    video = Column(String(20))

    red_1 = Column(Integer)
    red_2 = Column(Integer)
    red_3 = Column(Integer)
    red_dq = Column(String(20))
    red_surrogate = Column(String(20))
    red_epa_sum = Column(Float)
    red_auto_epa_sum = Column(Float)
    red_teleop_epa_sum = Column(Float)
    red_endgame_epa_sum = Column(Float)
    red_rp_1_epa_sum = Column(Float)
    red_rp_2_epa_sum = Column(Float)

    # Different than dq/surrogate to allow for easier querying
    blue_1 = Column(Integer)
    blue_2 = Column(Integer)
    blue_3 = Column(Integer)
    blue_dq = Column(String(20))
    blue_surrogate = Column(String(20))
    blue_epa_sum = Column(Float)
    blue_auto_epa_sum = Column(Float)
    blue_teleop_epa_sum = Column(Float)
    blue_endgame_epa_sum = Column(Float)
    blue_rp_1_epa_sum = Column(Float)
    blue_rp_2_epa_sum = Column(Float)

    winner = Column(String(10))
    epa_winner = Column(String(10))
    epa_win_prob = Column(Float)
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
    red_auto_2_1 = Column(Integer)
    red_auto_2_2 = Column(Integer)
    red_teleop_1 = Column(Integer)
    red_teleop_2 = Column(Integer)
    red_teleop_2_1 = Column(Integer)
    red_teleop_2_2 = Column(Integer)
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
    blue_auto_2_1 = Column(Integer)
    blue_auto_2_2 = Column(Integer)
    blue_teleop_1 = Column(Integer)
    blue_teleop_2 = Column(Integer)
    blue_teleop_2_1 = Column(Integer)
    blue_teleop_2_2 = Column(Integer)
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
    offseason: bool
    status: str
    video: Optional[str] = None

    red_1: Optional[int] = None
    red_2: Optional[int] = None
    red_3: Optional[int] = None
    red_dq: Optional[str] = None
    red_surrogate: Optional[str] = None
    red_epa_sum: Optional[float] = None
    red_auto_epa_sum: Optional[float] = None
    red_teleop_epa_sum: Optional[float] = None
    red_endgame_epa_sum: Optional[float] = None
    red_rp_1_epa_sum: Optional[float] = None
    red_rp_2_epa_sum: Optional[float] = None

    blue_1: Optional[int] = None
    blue_2: Optional[int] = None
    blue_3: Optional[int] = None
    blue_dq: Optional[str] = None
    blue_surrogate: Optional[str] = None
    blue_epa_sum: Optional[float] = None
    blue_auto_epa_sum: Optional[float] = None
    blue_teleop_epa_sum: Optional[float] = None
    blue_endgame_epa_sum: Optional[float] = None
    blue_rp_1_epa_sum: Optional[float] = None
    blue_rp_2_epa_sum: Optional[float] = None

    winner: Optional[str] = None
    epa_winner: Optional[str] = None
    epa_win_prob: Optional[float] = None
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
    red_auto_2_1: Optional[int] = None
    red_auto_2_2: Optional[int] = None
    red_teleop_1: Optional[int] = None
    red_teleop_2: Optional[int] = None
    red_teleop_2_1: Optional[int] = None
    red_teleop_2_2: Optional[int] = None
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
    blue_auto_2_1: Optional[int] = None
    blue_auto_2_2: Optional[int] = None
    blue_teleop_1: Optional[int] = None
    blue_teleop_2: Optional[int] = None
    blue_teleop_2_1: Optional[int] = None
    blue_teleop_2_2: Optional[int] = None
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

    def as_dict(self: "Match") -> Dict[str, Any]:
        return attr.asdict(
            self,  # type: ignore
            filter=attr.filters.exclude(
                attr.fields(Match).red_auto_1,  # type: ignore
                attr.fields(Match).red_auto_2,  # type: ignore
                attr.fields(Match).red_auto_2_1,  # type: ignore
                attr.fields(Match).red_auto_2_2,  # type: ignore
                attr.fields(Match).red_teleop_1,  # type: ignore
                attr.fields(Match).red_teleop_2,  # type: ignore
                attr.fields(Match).red_teleop_2_1,  # type: ignore
                attr.fields(Match).red_teleop_2_2,  # type: ignore
                attr.fields(Match).blue_auto_1,  # type: ignore
                attr.fields(Match).blue_auto_2,  # type: ignore
                attr.fields(Match).blue_auto_2_1,  # type: ignore
                attr.fields(Match).blue_auto_2_2,  # type: ignore
                attr.fields(Match).blue_teleop_1,  # type: ignore
                attr.fields(Match).blue_teleop_2,  # type: ignore
                attr.fields(Match).blue_teleop_2_1,  # type: ignore
                attr.fields(Match).blue_teleop_2_2,  # type: ignore
            ),
        )

    """SUPER FUNCTIONS"""

    def sort(self) -> int:
        return self.time or 0

    def get_red(self) -> List[int]:
        return [x for x in [self.red_1, self.red_2, self.red_3] if x is not None]

    def get_blue(self) -> List[int]:
        return [x for x in [self.blue_1, self.blue_2, self.blue_3] if x is not None]

    def get_teams(self) -> List[List[int]]:
        return [self.get_red(), self.get_blue()]

    def to_dict(self) -> Dict[str, Any]:
        out: Dict[str, Any] = {k: getattr(self, k) for k in self.__slots__}  # type: ignore
        out["red"] = self.get_red()
        out["blue"] = self.get_blue()
        return out

    def __str__(self: "Match"):
        # Only refresh DB if these change (during 1 min partial update)
        return f"{self.key}_{self.status}_{self.red_score}_{self.blue_score}"
