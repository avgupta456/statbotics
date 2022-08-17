from typing import Any, Dict, Optional

import attr
from sqlalchemy import Boolean, Column, Float, Integer, String
from sqlalchemy.sql.schema import ForeignKeyConstraint, PrimaryKeyConstraint

from src.db.main import Base
from src.db.models.main import Model, ModelORM


class TeamMatchORM(Base, ModelORM):
    """DECLARATION"""

    __tablename__ = "team_matches"
    id = Column(Integer)  # placeholder for backend API
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
    playoff = Column(Boolean)
    alliance = Column(String(10))

    # Choices are 'Upcoming', 'Completed'
    status = Column(String(10))

    elo = Column(Float)

    ils_1 = Column(Float)
    ils_2 = Column(Float)


@attr.s(auto_attribs=True, slots=True)
class TeamMatch(Model):
    id: int
    team: int
    year: int
    event: str
    match: str

    time: int = 0
    playoff: bool = False
    alliance: str = ""
    status: str = ""

    elo: Optional[float] = None

    ils_1: Optional[float] = None
    ils_2: Optional[float] = None

    @classmethod
    def from_dict(cls, dict: Dict[str, Any]) -> "TeamMatch":
        dict = {k: dict.get(k, None) for k in cls.__slots__}
        return TeamMatch(**dict)

    """SUPER FUNCTIONS"""

    def sort(self) -> int:
        return self.time
