import attr
from typing import Any, Dict, Optional

from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.sql.schema import ForeignKeyConstraint, PrimaryKeyConstraint

from db.main import Base
from db.models.main import Model, ModelORM


class TeamMatchORM(Base, ModelORM):
    """DECLARATION"""

    __tablename__ = "team_matches"
    team = Column(Integer, index=True)
    year = Column(Integer, index=True)
    event = Column(String(20), index=True)
    match = Column(String(20), index=True)

    PrimaryKeyConstraint(team, match)
    ForeignKeyConstraint(["year"], ["years.year"])
    ForeignKeyConstraint(["team"], ["teams.team"])
    ForeignKeyConstraint(["event"], ["events.key"])
    ForeignKeyConstraint(["match"], ["matches.key"])
    ForeignKeyConstraint(["team", "year"], ["team_years.team", "team_years.year"])
    ForeignKeyConstraint(["team", "event"], ["team_events.team", "team_events.event"])

    """GENERAL"""
    time = Column(Integer)
    playoff = Column(Integer)
    alliance = Column(String(10))

    # Choices are 'Upcoming', 'Completed'
    status = Column(String(10))

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
    team: int
    year: int
    event: str
    match: str

    time: int = 0
    playoff: int = 0
    alliance: str = ""
    status: str = ""

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
