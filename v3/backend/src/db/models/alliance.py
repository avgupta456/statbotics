from typing import Any, Dict, List, Optional

import attr
from sqlalchemy import Boolean, Column, Float, Integer, String  # type: ignore
from sqlalchemy.sql.schema import (  # type: ignore
    ForeignKeyConstraint,
    PrimaryKeyConstraint,
)

from src.db.main import Base
from src.db.models.main import Model, ModelORM


class AllianceORM(Base, ModelORM):
    """DECLARATION"""

    __tablename__ = "alliances"
    alliance = Column(String(4), index=True)
    year = Column(Integer, index=True)
    event = Column(String(20), index=True)
    match = Column(String(20), index=True)

    PrimaryKeyConstraint(alliance, match)
    ForeignKeyConstraint(["year"], ["years.year"])
    ForeignKeyConstraint(["event"], ["events.key"])
    ForeignKeyConstraint(["match"], ["matches.key"])

    """GENERAL"""
    offseason = Column(Boolean, index=True)
    week = Column(Integer, index=True)
    playoff = Column(Boolean, index=True)

    # TODO: Do we need all of these?
    comp_level = Column(String(10))
    set_number = Column(Integer)
    match_number = Column(Integer)

    time = Column(Integer)

    # TODO: Convert to boolean
    # Choices are 'Upcoming', 'Completed'
    status = Column(String(10), index=True)

    team_1 = Column(String(6), index=True)
    team_2 = Column(String(6), index=True)
    team_3 = Column(String(6), index=True)
    dq = Column(String(20))
    surrogate = Column(String(20))

    """EPA"""
    epa_sum = Column(Float)
    auto_epa_sum = Column(Float)
    teleop_epa_sum = Column(Float)
    endgame_epa_sum = Column(Float)
    comp_1_epa_sum = Column(Float)
    comp_2_epa_sum = Column(Float)
    comp_3_epa_sum = Column(Float)
    comp_4_epa_sum = Column(Float)
    comp_5_epa_sum = Column(Float)
    comp_6_epa_sum = Column(Float)
    comp_7_epa_sum = Column(Float)
    comp_8_epa_sum = Column(Float)
    comp_9_epa_sum = Column(Float)
    comp_10_epa_sum = Column(Float)
    rp_1_epa_sum = Column(Float)
    rp_2_epa_sum = Column(Float)

    winner = Column(Boolean)
    epa_winner = Column(Boolean)
    epa_win_prob = Column(Float)
    rp_1_prob = Column(Float)
    rp_2_prob = Column(Float)

    """OUTCOME"""
    score = Column(Integer)
    no_foul_points = Column(Integer)
    foul_points = Column(Integer)
    auto_points = Column(Integer)
    teleop_points = Column(Integer)
    endgame_points = Column(Integer)
    rp_1 = Column(Boolean)
    rp_2 = Column(Boolean)

    comp_1 = Column(Float)
    comp_2 = Column(Float)
    comp_3 = Column(Float)
    comp_4 = Column(Float)
    comp_5 = Column(Float)
    comp_6 = Column(Float)
    comp_7 = Column(Float)
    comp_8 = Column(Float)
    comp_9 = Column(Float)
    comp_10 = Column(Float)


@attr.s(auto_attribs=True, slots=True)
class Alliance(Model):
    """DECLARATION"""

    alliance: str
    year: int
    event: str
    match: str

    """GENERAL"""
    offseason: bool
    week: int
    playoff: bool

    comp_level: str
    set_number: int
    match_number: int

    time: int
    status: str

    team_1: Optional[str] = None
    team_2: Optional[str] = None
    team_3: Optional[str] = None
    dq: Optional[str] = None
    surrogate: Optional[str] = None

    """EPA"""
    epa_sum: Optional[float] = None
    auto_epa_sum: Optional[float] = None
    teleop_epa_sum: Optional[float] = None
    endgame_epa_sum: Optional[float] = None
    comp_1_epa_sum: Optional[float] = None
    comp_2_epa_sum: Optional[float] = None
    comp_3_epa_sum: Optional[float] = None
    comp_4_epa_sum: Optional[float] = None
    comp_5_epa_sum: Optional[float] = None
    comp_6_epa_sum: Optional[float] = None
    comp_7_epa_sum: Optional[float] = None
    comp_8_epa_sum: Optional[float] = None
    comp_9_epa_sum: Optional[float] = None
    comp_10_epa_sum: Optional[float] = None
    rp_1_epa_sum: Optional[float] = None
    rp_2_epa_sum: Optional[float] = None

    winner: Optional[bool] = None
    epa_winner: Optional[bool] = None
    epa_win_prob: Optional[float] = None
    rp_1_prob: Optional[float] = None
    rp_2_prob: Optional[float] = None

    """OUTCOME"""
    score: Optional[int] = None
    no_foul_points: Optional[int] = None
    foul_points: Optional[int] = None
    auto_points: Optional[int] = None
    teleop_points: Optional[int] = None
    endgame_points: Optional[int] = None
    rp_1: Optional[bool] = None
    rp_2: Optional[bool] = None

    comp_1: Optional[float] = None
    comp_2: Optional[float] = None
    comp_3: Optional[float] = None
    comp_4: Optional[float] = None
    comp_5: Optional[float] = None
    comp_6: Optional[float] = None
    comp_7: Optional[float] = None
    comp_8: Optional[float] = None
    comp_9: Optional[float] = None
    comp_10: Optional[float] = None

    @classmethod
    def from_dict(cls, dict: Dict[str, Any]) -> "Alliance":
        dict = {k: dict.get(k, None) for k in cls.__slots__}  # type: ignore
        return Alliance(**dict)

    def as_dict(self: "Alliance") -> Dict[str, Any]:
        return attr.asdict(self)

    """SUPER FUNCTIONS"""

    def sort(self) -> int:
        return self.time or 0

    def get_teams(self) -> List[str]:
        return [x for x in [self.team_1, self.team_2, self.team_3] if x is not None]

    def get_surrogates(self) -> List[str]:
        if self.surrogate is None:
            return []
        return [x for x in self.surrogate.split(",") if x != ""]

    def get_dqs(self) -> List[str]:
        if self.dq is None:
            return []
        return [x for x in self.dq.split(",") if x != ""]

    def __str__(self: "Alliance"):
        # Only refresh DB if these change (during 1 min partial update)
        return f"{self.match}_{self.alliance}_{self.score}_{self.teleop}_{self.epa_sum}"
