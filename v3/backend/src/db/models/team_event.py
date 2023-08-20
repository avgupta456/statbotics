from typing import Any, Dict, Optional, Tuple

import attr
from sqlalchemy import Boolean, Column, Float, Integer  # type: ignore
from sqlalchemy.sql.schema import (  # type: ignore
    ForeignKeyConstraint,
    PrimaryKeyConstraint,
)
from sqlalchemy.sql.sqltypes import String  # type: ignore

from src.db.main import Base
from src.db.models.main import Model, ModelORM


class TeamEventORM(Base, ModelORM):
    """DECLARATIONS"""

    __tablename__ = "team_events"
    id = Column(Integer)  # placeholder for backend API
    team = Column(String(6), index=True)
    year = Column(Integer, index=True)
    event = Column(String, index=True)

    PrimaryKeyConstraint(team, event)
    ForeignKeyConstraint(["team"], ["teams.team"])
    ForeignKeyConstraint(["year"], ["years.year"])
    ForeignKeyConstraint(["team", "year"], ["team_years.team", "team_years.year"])
    ForeignKeyConstraint(["event"], ["events.key"])

    """GENERAL"""
    time = Column(Integer)
    offseason = Column(Boolean)

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
    first_event = Column(Boolean)

    """EPA"""
    epa_start = Column(Float)
    epa_pre_playoffs = Column(Float)
    epa_end = Column(Float)
    epa_mean = Column(Float)
    epa_max = Column(Float)
    epa_diff = Column(Float)

    auto_epa_start = Column(Float)
    auto_epa_pre_playoffs = Column(Float)
    auto_epa_end = Column(Float)
    auto_epa_mean = Column(Float)
    auto_epa_max = Column(Float)

    teleop_epa_start = Column(Float)
    teleop_epa_pre_playoffs = Column(Float)
    teleop_epa_end = Column(Float)
    teleop_epa_mean = Column(Float)
    teleop_epa_max = Column(Float)

    endgame_epa_start = Column(Float)
    endgame_epa_pre_playoffs = Column(Float)
    endgame_epa_end = Column(Float)
    endgame_epa_mean = Column(Float)
    endgame_epa_max = Column(Float)

    rp_1_epa_start = Column(Float)
    rp_1_epa_end = Column(Float)
    rp_1_epa_mean = Column(Float)
    rp_1_epa_max = Column(Float)

    rp_2_epa_start = Column(Float)
    rp_2_epa_end = Column(Float)
    rp_2_epa_mean = Column(Float)
    rp_2_epa_max = Column(Float)

    # TODO: Add unitless and norm epa
    # """NORM EPA"""
    # unitless_epa_end = Column(Float)
    # norm_epa_end = Column(Float)

    """STATS"""
    wins = Column(Integer)
    losses = Column(Integer)
    ties = Column(Integer)
    count = Column(Integer)
    winrate = Column(Float)
    qual_wins = Column(Integer)
    qual_losses = Column(Integer)
    qual_ties = Column(Integer)
    qual_count = Column(Integer)
    qual_winrate = Column(Float)
    rps = Column(Integer)
    rps_per_match = Column(Float)
    rank = Column(Integer)
    num_teams = Column(Integer)


@attr.s(auto_attribs=True, slots=True)
class TeamEvent(Model):
    id: int
    team: str
    year: int
    event: str

    time: int
    offseason: bool

    team_name: Optional[str] = None
    event_name: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    district: Optional[str] = None
    type: Optional[int] = None
    week: Optional[int] = None

    status: Optional[str] = None
    first_event: Optional[bool] = None

    epa_start: Optional[float] = None
    epa_pre_playoffs: Optional[float] = None
    epa_end: Optional[float] = None
    epa_mean: Optional[float] = None
    epa_max: Optional[float] = None
    epa_diff: Optional[float] = None

    auto_epa_start: Optional[float] = None
    auto_epa_pre_playoffs: Optional[float] = None
    auto_epa_end: Optional[float] = None
    auto_epa_mean: Optional[float] = None
    auto_epa_max: Optional[float] = None

    teleop_epa_start: Optional[float] = None
    teleop_epa_pre_playoffs: Optional[float] = None
    teleop_epa_end: Optional[float] = None
    teleop_epa_mean: Optional[float] = None
    teleop_epa_max: Optional[float] = None

    endgame_epa_start: Optional[float] = None
    endgame_epa_pre_playoffs: Optional[float] = None
    endgame_epa_end: Optional[float] = None
    endgame_epa_mean: Optional[float] = None
    endgame_epa_max: Optional[float] = None

    rp_1_epa_start: Optional[float] = None
    rp_1_epa_end: Optional[float] = None
    rp_1_epa_mean: Optional[float] = None
    rp_1_epa_max: Optional[float] = None

    rp_2_epa_start: Optional[float] = None
    rp_2_epa_end: Optional[float] = None
    rp_2_epa_mean: Optional[float] = None
    rp_2_epa_max: Optional[float] = None

    wins: int = 0
    losses: int = 0
    ties: int = 0
    count: int = 0
    winrate: float = 0
    qual_wins: int = 0
    qual_losses: int = 0
    qual_ties: int = 0
    qual_count: int = 0
    qual_winrate: float = 0
    rps: int = 0
    rps_per_match: float = 0
    rank: Optional[int] = None
    num_teams: Optional[int] = None

    @classmethod
    def from_dict(cls, dict: Dict[str, Any]) -> "TeamEvent":
        dict = {k: dict.get(k, None) for k in cls.__slots__}  # type: ignore
        return TeamEvent(**dict)

    def as_dict(self: "TeamEvent") -> Dict[str, Any]:
        return attr.asdict(
            self,  # type: ignore
            filter=attr.filters.exclude(
                attr.fields(TeamEvent).id, attr.fields(TeamEvent).time  # type: ignore
            ),
        )

    """SUPER FUNCTIONS"""

    def sort(self) -> Tuple[str, int]:
        return (self.team, self.time)

    def __str__(self: "TeamEvent"):
        # Only refresh DB if these change (during 1 min partial update)
        return f"{self.team}_{self.event}_{self.status}_{self.count}_{self.rank}"
