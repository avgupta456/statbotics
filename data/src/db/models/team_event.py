from dataclasses import dataclass, fields
from typing import Any, Dict

from sqlalchemy import Column, Float, ForeignKey, Integer

from db.main import Base
from db.models.main import Model, ModelORM


class TeamEventORM(Base, ModelORM):
    """DECLARATIONS"""

    __tablename__ = "team_events"
    id: Column[int] = Column(Integer, primary_key=True, index=True)
    team_id: Column[int] = Column(Integer, ForeignKey("teams.id"), index=True)
    team_year_id: Column[int] = Column(Integer, ForeignKey("team_years.id"))
    year_id: Column[int] = Column(Integer, ForeignKey("years.id"))
    event_id: Column[int] = Column(Integer, ForeignKey("events.id"), index=True)

    """GENERAL"""
    time = Column(Integer)

    """ELO"""
    elo_start = Column(Float)
    elo_pre_playoffs = Column(Float)
    elo_end = Column(Float)
    elo_mean = Column(Float)
    elo_max = Column(Float)
    elo_diff = Column(Float)

    """OPR"""
    opr_start = Column(Float)
    opr_end = Column(Float)

    opr_auto = Column(Float)
    opr_teleop = Column(Float)
    opr_1 = Column(Float)
    opr_2 = Column(Float)
    opr_endgame = Column(Float)
    opr_fouls = Column(Float)
    opr_no_fouls = Column(Float)

    """ILS"""
    ils_1_start = Column(Float)
    ils_2_start = Column(Float)
    ils_1_end = Column(Float)
    ils_2_end = Column(Float)

    """STATS"""
    wins = Column(Integer)
    losses = Column(Integer)
    ties = Column(Integer)
    count = Column(Integer)
    winrate = Column(Float)
    rank = Column(Integer)


@dataclass
class TeamEvent(Model):
    id: int
    team_id: int
    team_year_id: int
    year_id: int
    event_id: int

    time: int
    elo_start: float = -1
    elo_pre_playoffs: float = -1
    elo_end: float = -1
    elo_mean: float = -1
    elo_max: float = -1
    elo_diff: float = -1

    opr_start: float = -1
    opr_end: float = -1
    opr_auto: float = -1
    opr_teleop: float = -1
    opr_1: float = -1
    opr_2: float = -1
    opr_endgame: float = -1
    opr_fouls: float = -1
    opr_no_fouls: float = -1

    ils_1_start: float = -1
    ils_2_start: float = -1
    ils_1_end: float = -1
    ils_2_end: float = -1

    wins: int = 0
    losses: int = 0
    ties: int = 0
    count: int = 0
    winrate: float = 0
    rank: int = -1

    @classmethod
    def from_dict(cls, dict: Dict[str, Any]) -> "TeamEvent":
        class_fields = {f.name for f in fields(cls)}
        return TeamEvent(**{k: v for k, v in dict.items() if k in class_fields})

    """SUPER FUNCTIONS"""

    def __lt__(self, other: "TeamEvent") -> bool:
        if self.team_id == other.team_id:
            return self.time < other.time
        return self.team_id < other.team_id

    def __repr__(self) -> str:
        return "(TeamEvent " + str(self.team_id) + " " + str(self.event_id) + ")"
