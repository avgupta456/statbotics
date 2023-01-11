from typing import Any, Dict, Optional, Tuple

import attr
from sqlalchemy import Boolean, Column, Float, Integer
from sqlalchemy.sql.schema import ForeignKeyConstraint, PrimaryKeyConstraint
from sqlalchemy.sql.sqltypes import String

from src.db.main import Base
from src.db.models.main import Model, ModelORM


class TeamYearORM(Base, ModelORM):
    """DECLARATION"""

    __tablename__ = "team_years"
    id = Column(Integer)  # placeholder for backend API
    year = Column(Integer, index=True)
    team = Column(Integer, index=True)

    # force unique (team, year)
    PrimaryKeyConstraint(team, year)
    ForeignKeyConstraint(["year"], ["years.year"])
    ForeignKeyConstraint(["team"], ["teams.team"])

    """API COMPLETENESS"""
    offseason = Column(Boolean)
    name = Column(String(100))
    state = Column(String(10))
    country = Column(String(30))
    district = Column(String(10))

    """PRE JOINS (FOR FRONTEND LOAD TIME)"""
    next_event_key = Column(String(10))
    next_event_name = Column(String(100))
    next_event_week = Column(Integer)

    """EPA"""
    epa_start = Column(Float)
    epa_pre_champs = Column(Float)
    epa_end = Column(Float)
    epa_mean = Column(Float)
    epa_max = Column(Float)
    epa_diff = Column(Float)

    auto_epa_start = Column(Float)
    auto_epa_pre_champs = Column(Float)
    auto_epa_end = Column(Float)
    auto_epa_mean = Column(Float)
    auto_epa_max = Column(Float)

    teleop_epa_start = Column(Float)
    teleop_epa_pre_champs = Column(Float)
    teleop_epa_end = Column(Float)
    teleop_epa_mean = Column(Float)
    teleop_epa_max = Column(Float)

    endgame_epa_start = Column(Float)
    endgame_epa_pre_champs = Column(Float)
    endgame_epa_end = Column(Float)
    endgame_epa_mean = Column(Float)
    endgame_epa_max = Column(Float)

    rp_1_epa_start = Column(Float)
    rp_1_epa_pre_champs = Column(Float)
    rp_1_epa_end = Column(Float)
    rp_1_epa_mean = Column(Float)
    rp_1_epa_max = Column(Float)

    rp_2_epa_start = Column(Float)
    rp_2_epa_pre_champs = Column(Float)
    rp_2_epa_end = Column(Float)
    rp_2_epa_mean = Column(Float)
    rp_2_epa_max = Column(Float)

    """NORM EPA"""
    norm_epa_end = Column(Float)

    """STATS"""
    wins = Column(Integer)  # competition season only
    losses = Column(Integer)
    ties = Column(Integer)
    count = Column(Integer)
    winrate = Column(Float)

    full_wins = Column(Integer)  # includes offseason
    full_losses = Column(Integer)
    full_ties = Column(Integer)
    full_count = Column(Integer)
    full_winrate = Column(Float)

    total_epa_rank = Column(Integer)
    total_epa_percentile = Column(Float)
    total_team_count = Column(Integer)

    country_epa_rank = Column(Integer)
    country_epa_percentile = Column(Float)
    country_team_count = Column(Integer)

    state_epa_rank = Column(Integer)
    state_epa_percentile = Column(Float)
    state_team_count = Column(Integer)

    district_epa_rank = Column(Integer)
    district_epa_percentile = Column(Float)
    district_team_count = Column(Integer)


@attr.s(auto_attribs=True, slots=True)
class TeamYear(Model):
    id: int
    year: int
    team: int
    offseason: bool

    name: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    district: Optional[str] = None

    next_event_key: Optional[str] = None
    next_event_name: Optional[str] = None
    next_event_week: Optional[int] = None

    epa_start: Optional[float] = None
    epa_pre_champs: Optional[float] = None
    epa_end: Optional[float] = None
    epa_mean: Optional[float] = None
    epa_max: Optional[float] = None
    epa_diff: Optional[float] = None

    auto_epa_start: Optional[float] = None
    auto_epa_pre_champs: Optional[float] = None
    auto_epa_end: Optional[float] = None
    auto_epa_mean: Optional[float] = None
    auto_epa_max: Optional[float] = None

    teleop_epa_start: Optional[float] = None
    teleop_epa_pre_champs: Optional[float] = None
    teleop_epa_end: Optional[float] = None
    teleop_epa_mean: Optional[float] = None
    teleop_epa_max: Optional[float] = None

    endgame_epa_start: Optional[float] = None
    endgame_epa_pre_champs: Optional[float] = None
    endgame_epa_end: Optional[float] = None
    endgame_epa_mean: Optional[float] = None
    endgame_epa_max: Optional[float] = None

    rp_1_epa_start: Optional[float] = None
    rp_1_epa_pre_champs: Optional[float] = None
    rp_1_epa_end: Optional[float] = None
    rp_1_epa_mean: Optional[float] = None
    rp_1_epa_max: Optional[float] = None

    rp_2_epa_start: Optional[float] = None
    rp_2_epa_pre_champs: Optional[float] = None
    rp_2_epa_end: Optional[float] = None
    rp_2_epa_mean: Optional[float] = None
    rp_2_epa_max: Optional[float] = None

    norm_epa_end: Optional[float] = None

    wins: int = 0
    losses: int = 0
    ties: int = 0
    count: int = 0
    winrate: float = 0

    full_wins: int = 0
    full_losses: int = 0
    full_ties: int = 0
    full_count: int = 0
    full_winrate: float = 0

    total_epa_rank: Optional[int] = None
    total_epa_percentile: Optional[float] = None
    total_team_count: Optional[int] = None

    country_epa_rank: Optional[int] = None
    country_epa_percentile: Optional[float] = None
    country_team_count: Optional[int] = None

    state_epa_rank: Optional[int] = None
    state_epa_percentile: Optional[float] = None
    state_team_count: Optional[int] = None

    district_epa_rank: Optional[int] = None
    district_epa_percentile: Optional[float] = None
    district_team_count: Optional[int] = None

    @classmethod
    def from_dict(cls, dict: Dict[str, Any]) -> "TeamYear":
        dict = {k: dict.get(k, None) for k in cls.__slots__}  # type: ignore
        return TeamYear(**dict)

    """SUPER FUNCTIONS"""

    def sort(self) -> Tuple[int, int]:
        return (self.team, self.year)

    def __str__(self: "TeamYear"):
        # Only refresh DB if these change (during 1 min partial update)
        return f"{self.team}_{self.year}_{self.count}"
