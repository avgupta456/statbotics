import attr
from typing import Any, Dict, Optional

from sqlalchemy import Column, Float, ForeignKey, Integer, String

from db.main import Base
from db.models.main import Model, ModelORM


class TeamMatchORM(Base, ModelORM):
    """DECLARATION"""

    __tablename__ = "team_matches"
    id: Column[int] = Column(Integer, primary_key=True, index=True)
    team: Column[int] = Column(Integer, ForeignKey("teams.team"), index=True)
    team_year_id: Column[int] = Column(Integer, ForeignKey("team_years.id"), index=True)
    team_event_id: Column[int] = Column(
        Integer, ForeignKey("team_events.id"), index=True
    )
    year: Column[int] = Column(Integer, ForeignKey("years.year"), index=True)
    event_id: Column[int] = Column(Integer, ForeignKey("events.id"), index=True)
    match_id: Column[int] = Column(Integer, ForeignKey("matches.id"), index=True)

    """GENERAL"""
    time = Column(Integer)
    playoff = Column(Integer)
    alliance = Column(String(10))

    # Choices are 'Upcoming', 'Completed'
    status = Column(String(10))

    """API COMPLETENESS"""
    event = Column(String(20))
    match = Column(String(20))

    elo = Column(Float)
    opr = Column(Float)
    opr_auto = Column(Float)
    opr_teleop = Column(Float)
    opr_one = Column(Float)
    opr_two = Column(Float)
    opr_endgame = Column(Float)
    opr_no_fouls = Column(Float)
    opr_fouls = Column(Float)

    ils_1 = Column(Float)
    ils_2 = Column(Float)


@attr.s(auto_attribs=True, slots=True)
class TeamMatch(Model):
    id: int
    team: int
    team_year_id: int
    team_event_id: int
    year: int
    event_id: int
    match_id: int

    time: int
    playoff: int
    alliance: str
    status: str

    event: Optional[str] = None
    match: Optional[str] = None

    elo: Optional[float] = None
    opr: Optional[float] = None
    opr_auto: Optional[float] = None
    opr_teleop: Optional[float] = None
    opr_one: Optional[float] = None
    opr_two: Optional[float] = None
    opr_endgame: Optional[float] = None
    opr_no_fouls: Optional[float] = None
    opr_fouls: Optional[float] = None

    ils_1: Optional[float] = None
    ils_2: Optional[float] = None

    @classmethod
    def from_dict(cls, dict: Dict[str, Any]) -> "TeamMatch":
        dict = {k: dict.get(k, None) for k in cls.__slots__}
        return TeamMatch(**dict)

    """SUPER FUNCTIONS"""

    def sort(self) -> int:
        return self.time
