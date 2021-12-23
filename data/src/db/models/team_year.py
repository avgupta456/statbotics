from dataclasses import dataclass, fields
from typing import Any, Dict

from sqlalchemy import Column, Float, ForeignKey, Integer

from db.main import Base
from db.models.main import Model, ModelORM


class TeamYearORM(Base, ModelORM):
    """DECLARATION"""

    __tablename__ = "team_years"
    id: Column[int] = Column(Integer, primary_key=True, index=True)
    year_id: Column[int] = Column(Integer, ForeignKey("years.id"))
    team_id: Column[int] = Column(Integer, ForeignKey("teams.id"), index=True)

    """ELO"""
    elo_start = Column(Float)
    elo_pre_champs = Column(Float)
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
    ils_1 = Column(Float)
    ils_2 = Column(Float)

    """STATS"""
    wins = Column(Integer)
    losses = Column(Integer)
    ties = Column(Integer)
    count = Column(Integer)
    winrate = Column(Float)

    elo_rank = Column(Integer)
    elo_percentile = Column(Float)
    opr_rank = Column(Integer)
    opr_percentile = Column(Float)


@dataclass
class TeamYear(Model):
    id: int
    year_id: int
    team_id: int

    elo_start: float = -1
    elo_pre_champs: float = -1
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
    ils_1: float = -1
    ils_2: float = -1

    wins: int = 0
    losses: int = 0
    ties: int = 0
    count: int = 0
    winrate: float = 0

    elo_rank: int = -1
    elo_percentile: float = -1
    opr_rank: int = -1
    opr_percentile: float = -1

    @classmethod
    def from_dict(cls, dict: Dict[str, Any]) -> "TeamYear":
        class_fields = {f.name for f in fields(cls)}
        return TeamYear(**{k: v for k, v in dict.items() if k in class_fields})

    """SUPER FUNCTIONS"""

    def __lt__(self, other: "TeamYear") -> bool:
        if self.team_id == other.team_id:
            return self.year_id < other.year_id
        return self.team_id < other.team_id

    def __repr__(self) -> str:
        return f"TeamYear ({self.team_id} {self.year_id})"
