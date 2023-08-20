from typing import Any, Dict, Tuple, Optional

import attr
from sqlalchemy import Boolean, Column, Float, Integer  # type: ignore
from sqlalchemy.sql.schema import (  # type: ignore
    ForeignKeyConstraint,
    PrimaryKeyConstraint,
)
from sqlalchemy.sql.sqltypes import String  # type: ignore

from src.db.main import Base
from src.db.models.main import ModelORM, generate_attr_class


class TeamEventORM(Base, ModelORM):
    """DECLARATIONS"""

    __tablename__ = "team_events"
    id: int = Column(Integer)  # placeholder for backend API
    team: str = Column(String(6), index=True)
    year: int = Column(Integer, index=True)
    event: str = Column(String(10), index=True)

    PrimaryKeyConstraint(team, event)
    ForeignKeyConstraint(["team"], ["teams.team"])
    ForeignKeyConstraint(["year"], ["years.year"])
    ForeignKeyConstraint(["team", "year"], ["team_years.team", "team_years.year"])
    ForeignKeyConstraint(["event"], ["events.key"])

    """GENERAL"""
    time: int = Column(Integer)
    offseason: bool = Column(Boolean)

    """API COMPLETENESS"""
    team_name: str = Column(String(100))
    event_name: str = Column(String(100))
    state: str = Column(String(10))
    country: str = Column(String(30))
    district: str = Column(String(10))
    type: int = Column(Integer)
    week: int = Column(Integer)

    # Choices are 'Upcoming', 'Ongoing', 'Completed'
    status: str = Column(String(10))
    first_event: bool = Column(Boolean)

    """EPA"""
    epa_start: float = Column(Float)
    epa_pre_playoffs: float = Column(Float)
    epa_end: float = Column(Float)
    epa_mean: float = Column(Float)
    epa_max: float = Column(Float)
    epa_diff: float = Column(Float)

    auto_epa_start: float = Column(Float)
    auto_epa_pre_playoffs: float = Column(Float)
    auto_epa_end: float = Column(Float)
    auto_epa_mean: float = Column(Float)
    auto_epa_max: float = Column(Float)

    teleop_epa_start: float = Column(Float)
    teleop_epa_pre_playoffs: float = Column(Float)
    teleop_epa_end: float = Column(Float)
    teleop_epa_mean: float = Column(Float)
    teleop_epa_max: float = Column(Float)

    endgame_epa_start: float = Column(Float)
    endgame_epa_pre_playoffs: float = Column(Float)
    endgame_epa_end: float = Column(Float)
    endgame_epa_mean: float = Column(Float)
    endgame_epa_max: float = Column(Float)

    rp_1_epa_start: float = Column(Float)
    rp_1_epa_end: float = Column(Float)
    rp_1_epa_mean: float = Column(Float)
    rp_1_epa_max: float = Column(Float)

    rp_2_epa_start: float = Column(Float)
    rp_2_epa_end: float = Column(Float)
    rp_2_epa_mean: float = Column(Float)
    rp_2_epa_max: float = Column(Float)

    unitless_epa_end: float = Column(Float)
    norm_epa_end: Optional[float] = Column(Float)

    """STATS"""
    wins: int = Column(Integer)
    losses: int = Column(Integer)
    ties: int = Column(Integer)
    count: int = Column(Integer)
    winrate: float = Column(Float)
    qual_wins: int = Column(Integer)
    qual_losses: int = Column(Integer)
    qual_ties: int = Column(Integer)
    qual_count: int = Column(Integer)
    qual_winrate: float = Column(Float)
    rps: int = Column(Integer)
    rps_per_match: float = Column(Float)
    rank: int = Column(Integer)
    num_teams: int = Column(Integer)


_TeamEvent = generate_attr_class("TeamEvent", TeamEventORM)


class TeamEvent(_TeamEvent):
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

    def sort(self: "TeamEvent") -> Tuple[str, int]:
        return (self.team, self.time)

    def __str__(self: "TeamEvent"):
        # Only refresh DB if these change (during 1 min partial update)
        return f"{self.team}_{self.event}_{self.status}_{self.count}_{self.rank}"
