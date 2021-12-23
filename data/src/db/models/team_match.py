from dataclasses import dataclass, fields
from typing import Any, Dict

from sqlalchemy import Column, Float, ForeignKey, Integer, String

from db.main import Base
from db.models.main import Model, ModelORM


class TeamMatchORM(Base, ModelORM):
    """DECLARATION"""

    __tablename__ = "team_matches"
    id: Column[int] = Column(Integer, primary_key=True, index=True)
    team_id: Column[int] = Column(Integer, ForeignKey("teams.id"))
    team_year_id: Column[int] = Column(Integer, ForeignKey("team_years.id"))
    team_event_id: Column[int] = Column(
        Integer, ForeignKey("team_events.id"), index=True
    )
    year_id: Column[int] = Column(Integer, ForeignKey("years.id"))
    event_id: Column[int] = Column(Integer, ForeignKey("events.id"))
    match_id: Column[int] = Column(Integer, ForeignKey("matches.id"), index=True)

    time = Column(Integer)
    alliance = Column(String(10))

    """GENERAL"""

    elo = Column(Float)
    opr_score = Column(Float)
    opr_auto = Column(Float)
    opr_teleop = Column(Float)
    opr_one = Column(Float)
    opr_two = Column(Float)
    opr_endgame = Column(Float)
    opr_no_fouls = Column(Float)
    opr_fouls = Column(Float)

    ils_1 = Column(Float)
    ils_2 = Column(Float)


@dataclass
class TeamMatch(Model):
    id: int
    team_id: int
    team_year_id: int
    team_event_id: int
    year_id: int
    event_id: int
    match_id: int

    time: int
    alliance: str

    elo: float = -1
    opr_score: float = -1
    opr_auto: float = -1
    opr_teleop: float = -1
    opr_one: float = -1
    opr_two: float = -1
    opr_endgame: float = -1
    opr_no_fouls: float = -1
    opr_fouls: float = -1

    ils_1: float = -1
    ils_2: float = -1

    @classmethod
    def from_dict(cls, dict: Dict[str, Any]) -> "TeamMatch":
        class_fields = {f.name for f in fields(cls)}
        return TeamMatch(**{k: v for k, v in dict.items() if k in class_fields})

    """SUPER FUNCTIONS"""

    def __lt__(self, other: "TeamMatch") -> bool:
        return self.time < other.time

    def __repr__(self) -> str:
        return "(Team Match " + str(self.team_id) + " " + str(self.match_id) + ")"
