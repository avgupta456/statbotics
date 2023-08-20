from typing import Any, Dict, List, Optional

import attr
from sqlalchemy import Boolean, Column, Float, Integer, String  # type: ignore
from sqlalchemy.sql.schema import (  # type: ignore
    ForeignKeyConstraint,
    PrimaryKeyConstraint,
)

from src.db.main import Base
from src.db.models.main import ModelORM, generate_attr_class


class AllianceORM(Base, ModelORM):
    """DECLARATION"""

    __tablename__ = "alliances"
    id: int = Column(Integer)  # placeholder for backend API
    alliance: str = Column(String(4), index=True)
    year: int = Column(Integer, index=True)
    event: str = Column(String(20), index=True)
    match: str = Column(String(20), index=True)

    PrimaryKeyConstraint(alliance, match)
    ForeignKeyConstraint(["year"], ["years.year"])
    ForeignKeyConstraint(["event"], ["events.key"])
    ForeignKeyConstraint(["match"], ["matches.key"])

    """GENERAL"""
    offseason: bool = Column(Boolean, index=True)
    week: int = Column(Integer, index=True)
    playoff: bool = Column(Boolean, index=True)

    # TODO: Do we need all of these?
    comp_level: str = Column(String(10))
    set_number: int = Column(Integer)
    match_number: int = Column(Integer)

    time: int = Column(Integer)

    # TODO: Convert to boolean
    # Choices are 'Upcoming', 'Completed'
    status: str = Column(String(10), index=True)

    team_1: str = Column(String(6), index=True)
    team_2: str = Column(String(6), index=True)
    team_3: Optional[str] = Column(String(6), index=True)
    dq: str = Column(String(20))
    surrogate: str = Column(String(20))

    """EPA"""
    epa_winner: bool = Column(Boolean)
    epa_win_prob: float = Column(Float)
    rp_1_prob: float = Column(Float)
    rp_2_prob: float = Column(Float)

    epa_sum: float = Column(Float)
    auto_epa_sum: float = Column(Float)
    teleop_epa_sum: float = Column(Float)
    endgame_epa_sum: float = Column(Float)
    comp_1_epa_sum: float = Column(Float)
    comp_2_epa_sum: float = Column(Float)
    comp_3_epa_sum: float = Column(Float)
    comp_4_epa_sum: float = Column(Float)
    comp_5_epa_sum: float = Column(Float)
    comp_6_epa_sum: float = Column(Float)
    comp_7_epa_sum: float = Column(Float)
    comp_8_epa_sum: float = Column(Float)
    comp_9_epa_sum: float = Column(Float)
    comp_10_epa_sum: float = Column(Float)
    rp_1_epa_sum: float = Column(Float)
    rp_2_epa_sum: float = Column(Float)

    """OUTCOME"""
    winner: Optional[bool] = Column(Boolean)
    score: Optional[int] = Column(Integer)
    no_foul_points: Optional[int] = Column(Integer)
    foul_points: Optional[int] = Column(Integer)
    auto_points: Optional[int] = Column(Integer)
    teleop_points: Optional[int] = Column(Integer)
    endgame_points: Optional[int] = Column(Integer)
    rp_1: Optional[bool] = Column(Boolean)
    rp_2: Optional[bool] = Column(Boolean)

    comp_1: Optional[float] = Column(Float)
    comp_2: Optional[float] = Column(Float)
    comp_3: Optional[float] = Column(Float)
    comp_4: Optional[float] = Column(Float)
    comp_5: Optional[float] = Column(Float)
    comp_6: Optional[float] = Column(Float)
    comp_7: Optional[float] = Column(Float)
    comp_8: Optional[float] = Column(Float)
    comp_9: Optional[float] = Column(Float)
    comp_10: Optional[float] = Column(Float)


_Alliance = generate_attr_class("Alliance", AllianceORM)


class Alliance(_Alliance):
    @classmethod
    def from_dict(cls, dict: Dict[str, Any]) -> "Alliance":
        dict = {k: dict.get(k, None) for k in cls.__slots__}  # type: ignore
        return Alliance(**dict)

    def as_dict(self: "Alliance") -> Dict[str, Any]:
        return attr.asdict(self)

    """HELPER FUNCTIONS"""

    def get_teams(self: "Alliance") -> List[str]:
        return [x for x in [self.team_1, self.team_2, self.team_3] if x is not None]

    def get_surrogates(self: "Alliance") -> List[str]:
        return [x for x in self.surrogate.split(",") if x != ""]

    def get_dqs(self: "Alliance") -> List[str]:
        return [x for x in self.dq.split(",") if x != ""]

    """PARENT FUNCTIONS"""

    def sort(self: "Alliance") -> int:
        return self.time or 0

    def pk(self: "Alliance") -> str:
        return f"{self.match}_{self.alliance}"

    def __str__(self: "Alliance") -> str:
        # Only refresh DB if these change (during 1 min partial update)
        return f"{self.match}_{self.alliance}_{self.score}_{self.teleop_points}_{self.epa_sum}"
