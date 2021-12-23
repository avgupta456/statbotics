from dataclasses import dataclass, fields
from typing import Any, Dict, List, Optional

from sqlalchemy import Column, Float, ForeignKey, Integer, String

from db.main import Base
from db.models.main import Model, ModelORM


class MatchORM(Base, ModelORM):
    """DECLARATION"""

    __tablename__ = "matches"
    id: Column[int] = Column(Integer, primary_key=True, index=True)
    year_id: Column[int] = Column(Integer, ForeignKey("years.id"))
    event_id: Column[int] = Column(Integer, ForeignKey("events.id"), index=True)

    """GENERAL"""
    key = Column(String(20))
    comp_level = Column(String(10))
    set_number = Column(Integer)
    match_number = Column(Integer)

    red = Column(String(20))
    red_elo_sum = Column(Float)
    red_opr_sum = Column(Float)
    red_ils_1_sum = Column(Float)
    red_ils_2_sum = Column(Float)

    blue = Column(String(20))
    blue_elo_sum = Column(Float)
    blue_opr_sum = Column(Float)
    blue_ils_1_sum = Column(Float)
    blue_ils_2_sum = Column(Float)

    winner = Column(String(10))
    elo_winner = Column(String(10))
    elo_win_prob = Column(Float)
    opr_winner = Column(String(10))
    opr_win_prob = Column(Float)
    mix_winner = Column(String(10))
    mix_win_prob = Column(Float)
    red_rp_1_prob = Column(Float)
    red_rp_2_prob = Column(Float)
    blue_rp_1_prob = Column(Float)
    blue_rp_2_prob = Column(Float)

    playoff = Column(Integer)  # 0 is qual, 1 is playoff
    time = Column(Integer)

    red_score = Column(Integer)
    blue_score = Column(Integer)

    red_auto = Column(Integer)
    red_auto_movement = Column(Integer)
    red_auto_1 = Column(Integer)
    red_auto_2 = Column(Integer)
    red_auto_2_1 = Column(Integer)
    red_auto_2_2 = Column(Integer)
    red_auto_2_3 = Column(Integer)
    red_teleop_1 = Column(Integer)
    red_teleop_2 = Column(Integer)
    red_teleop_2_1 = Column(Integer)
    red_teleop_2_2 = Column(Integer)
    red_teleop_2_3 = Column(Integer)
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
    blue_auto_2_1 = Column(Integer)
    blue_auto_2_2 = Column(Integer)
    blue_auto_2_3 = Column(Integer)
    blue_teleop_1 = Column(Integer)
    blue_teleop_2 = Column(Integer)
    blue_teleop_2_1 = Column(Integer)
    blue_teleop_2_2 = Column(Integer)
    blue_teleop_2_3 = Column(Integer)
    blue_1 = Column(Integer)
    blue_2 = Column(Integer)
    blue_teleop = Column(Integer)
    blue_endgame = Column(Integer)
    blue_no_fouls = Column(Integer)
    blue_fouls = Column(Integer)
    blue_rp_1 = Column(Integer)
    blue_rp_2 = Column(Integer)


@dataclass
class Match(Model):
    id: int
    year_id: int
    event_id: int

    key: str
    comp_level: str
    set_number: int
    match_number: int

    red: Optional[str] = None
    red_elo_sum: float = -1
    red_opr_sum: float = -1
    red_ils_1_sum: float = -1
    red_ils_2_sum: float = -1

    blue: Optional[str] = None
    blue_elo_sum: float = -1
    blue_opr_sum: float = -1
    blue_ils_1_sum: float = -1
    blue_ils_2_sum: float = -1

    winner: Optional[str] = None
    elo_winner: Optional[str] = None
    elo_win_prob: float = -1
    opr_winner: Optional[str] = None
    opr_win_prob: float = -1
    mix_winner: Optional[str] = None
    mix_win_prob: float = -1
    red_rp_1_prob: float = -1
    red_rp_2_prob: float = -1
    blue_rp_1_prob: float = -1
    blue_rp_2_prob: float = -1

    playoff: int = -1
    time: int = -1

    red_score: int = -1
    blue_score: int = -1

    red_auto: int = -1
    red_auto_movement: int = -1
    red_auto_1: int = -1
    red_auto_2: int = -1
    red_auto_2_1: int = -1
    red_auto_2_2: int = -1
    red_auto_2_3: int = -1
    red_teleop_1: int = -1
    red_teleop_2: int = -1
    red_teleop_2_1: int = -1
    red_teleop_2_2: int = -1
    red_teleop_2_3: int = -1
    red_1: int = -1
    red_2: int = -1
    red_teleop: int = -1
    red_endgame: int = -1
    red_no_fouls: int = -1
    red_fouls: int = -1
    red_rp_1: int = -1
    red_rp_2: int = -1

    blue_auto: int = -1
    blue_auto_movement: int = -1
    blue_auto_1: int = -1
    blue_auto_2: int = -1
    blue_auto_2_1: int = -1
    blue_auto_2_2: int = -1
    blue_auto_2_3: int = -1
    blue_teleop_1: int = -1
    blue_teleop_2: int = -1
    blue_teleop_2_1: int = -1
    blue_teleop_2_2: int = -1
    blue_teleop_2_3: int = -1
    blue_1: int = -1
    blue_2: int = -1
    blue_teleop: int = -1
    blue_endgame: int = -1
    blue_no_fouls: int = -1
    blue_fouls: int = -1
    blue_rp_1: int = -1
    blue_rp_2: int = -1

    @classmethod
    def from_dict(cls, dict: Dict[str, Any]) -> "Match":
        class_fields = {f.name for f in fields(cls)}
        return Match(**{k: v for k, v in dict.items() if k in class_fields})

    """SUPER FUNCTIONS"""

    def __lt__(self, other: "Match") -> bool:
        return self.time < other.time

    def __repr__(self) -> str:
        return "(Match " + str(self.key) + ")"

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
