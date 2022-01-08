from typing import Any, Dict, Optional, Tuple

import attr
from sqlalchemy import Column, Float, Integer
from sqlalchemy.sql.schema import ForeignKeyConstraint, PrimaryKeyConstraint
from sqlalchemy.sql.sqltypes import String

from db.main import Base
from db.models.main import Model, ModelORM


class TeamEventORM(Base, ModelORM):
    """DECLARATIONS"""

    __tablename__ = "team_events"
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


@attr.s(auto_attribs=True, slots=True)
class TeamEvent(Model):
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

    opr_start: Optional[float] = None
    opr_end: Optional[float] = None
    opr_auto: Optional[float] = None
    opr_teleop: Optional[float] = None
    opr_1: Optional[float] = None
    opr_2: Optional[float] = None
    opr_endgame: Optional[float] = None
    opr_fouls: Optional[float] = None
    opr_no_fouls: Optional[float] = None

    ils_1_start: Optional[float] = None
    ils_2_start: Optional[float] = None
    ils_1_end: Optional[float] = None
    ils_2_end: Optional[float] = None

    wins: Optional[int] = None
    losses: Optional[int] = None
    ties: Optional[int] = None
    count: Optional[int] = None
    winrate: Optional[float] = None
    rank: Optional[int] = None

    @classmethod
    def from_dict(cls, dict: Dict[str, Any]) -> "TeamEvent":
        dict = {k: dict.get(k, None) for k in cls.__slots__}
        return TeamEvent(**dict)

    """SUPER FUNCTIONS"""

    def sort(self) -> Tuple[int, int]:
        return self.team, self.time
