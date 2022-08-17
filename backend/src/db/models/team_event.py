from typing import Any, Dict, Optional, Tuple

import attr
from sqlalchemy import Column, Float, Integer
from sqlalchemy.sql.schema import ForeignKeyConstraint, PrimaryKeyConstraint
from sqlalchemy.sql.sqltypes import String

from src.db.main import Base
from src.db.models.main import Model, ModelORM


class TeamEventORM(Base, ModelORM):
    """DECLARATIONS"""

    __tablename__ = "team_events"
    id = Column(Integer)  # placeholder for backend API
    team = Column(Integer, index=True)
    year = Column(Integer, index=True)
    event = Column(String, index=True)

    PrimaryKeyConstraint(team, event)
    ForeignKeyConstraint(["team"], ["teams.team"])
    ForeignKeyConstraint(["year"], ["years.year"])
    ForeignKeyConstraint(["team", "year"], ["team_years.team", "team_years.year"])
    ForeignKeyConstraint(["event"], ["events.key"])

    """GENERAL"""
    time = Column(Integer)

    """API COMPLETENESS"""
    team_name = Column(String(100))
    event_name = Column(String(100))
    state = Column(String(10))
    country = Column(String(30))
    district = Column(String(10))
    type = Column(Integer)
    week = Column(Integer)

    # Choices are 'Upcoming', 'Ongoing', 'Completed'
    status = Column(String(10))

    """ELO"""
    elo_start = Column(Float)
    elo_pre_playoffs = Column(Float)
    elo_end = Column(Float)
    elo_mean = Column(Float)
    elo_max = Column(Float)
    elo_diff = Column(Float)

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


@attr.s(auto_attribs=True, slots=True)
class TeamEvent(Model):
    id: int
    team: int
    year: int
    event: str

    time: int

    team_name: Optional[str] = None
    event_name: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    district: Optional[str] = None
    type: Optional[int] = None
    week: Optional[int] = None
    status: Optional[str] = None

    elo_start: Optional[float] = None
    elo_pre_playoffs: Optional[float] = None
    elo_end: Optional[float] = None
    elo_mean: Optional[float] = None
    elo_max: Optional[float] = None
    elo_diff: Optional[float] = None

    ils_1_start: Optional[float] = None
    ils_2_start: Optional[float] = None
    ils_1_end: Optional[float] = None
    ils_2_end: Optional[float] = None

    wins: int = 0
    losses: int = 0
    ties: int = 0
    count: int = 0
    winrate: float = 0
    rank: Optional[int] = None

    @classmethod
    def from_dict(cls, dict: Dict[str, Any]) -> "TeamEvent":
        dict = {k: dict.get(k, None) for k in cls.__slots__}  # type: ignore
        return TeamEvent(**dict)

    """SUPER FUNCTIONS"""

    def sort(self) -> Tuple[int, int]:
        return self.team, self.time
