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


class TeamYearORM(Base, ModelORM):
    """DECLARATION"""

    __tablename__ = "team_years"
    id: int = Column(Integer)  # placeholder for backend API
    year: int = Column(Integer, index=True)
    team: str = Column(String(6), index=True)

    # force unique (team, year)
    PrimaryKeyConstraint(team, year)
    ForeignKeyConstraint(["year"], ["years.year"])
    ForeignKeyConstraint(["team"], ["teams.team"])

    """API COMPLETENESS"""
    offseason: bool = Column(Boolean)
    name: str = Column(String(100))
    country: Optional[str] = Column(String(30))
    district: Optional[str] = Column(String(10))
    state: Optional[str] = Column(String(10))

    """PRE JOINS (FOR FRONTEND LOAD TIME)"""
    is_competing: bool = Column(Boolean)
    next_event_key: str = Column(String(10))
    next_event_name: str = Column(String(100))
    next_event_week: int = Column(Integer)

    """EPA"""
    epa_start: float = Column(Float)
    epa_pre_champs: float = Column(Float)
    epa_end: float = Column(Float, index=True)
    epa_mean: float = Column(Float)
    epa_max: float = Column(Float)
    epa_diff: float = Column(Float)

    auto_epa_start: float = Column(Float)
    auto_epa_pre_champs: float = Column(Float)
    auto_epa_end: float = Column(Float)
    auto_epa_mean: float = Column(Float)
    auto_epa_max: float = Column(Float)

    teleop_epa_start: float = Column(Float)
    teleop_epa_pre_champs: float = Column(Float)
    teleop_epa_end: float = Column(Float)
    teleop_epa_mean: float = Column(Float)
    teleop_epa_max: float = Column(Float)

    endgame_epa_start: float = Column(Float)
    endgame_epa_pre_champs: float = Column(Float)
    endgame_epa_end: float = Column(Float)
    endgame_epa_mean: float = Column(Float)
    endgame_epa_max: float = Column(Float)

    rp_1_epa_start: float = Column(Float)
    rp_1_epa_pre_champs: float = Column(Float)
    rp_1_epa_end: float = Column(Float)
    rp_1_epa_mean: float = Column(Float)
    rp_1_epa_max: float = Column(Float)

    rp_2_epa_start: float = Column(Float)
    rp_2_epa_pre_champs: float = Column(Float)
    rp_2_epa_end: float = Column(Float)
    rp_2_epa_mean: float = Column(Float)
    rp_2_epa_max: float = Column(Float)

    """NORM EPA"""
    unitless_epa_end: float = Column(Float)
    norm_epa_end: Optional[float] = Column(Float)

    """STATS"""
    wins: int = Column(Integer)  # competition season only
    losses: int = Column(Integer)
    ties: int = Column(Integer)
    count: int = Column(Integer)
    winrate: float = Column(Float)

    full_wins: int = Column(Integer)  # includes offseason
    full_losses: int = Column(Integer)
    full_ties: int = Column(Integer)
    full_count: int = Column(Integer)
    full_winrate: float = Column(Float)

    total_epa_rank: int = Column(Integer)
    total_epa_percentile: float = Column(Float)
    total_team_count: int = Column(Integer)

    country_epa_rank: int = Column(Integer)
    country_epa_percentile: float = Column(Float)
    country_team_count: int = Column(Integer)

    state_epa_rank: int = Column(Integer)
    state_epa_percentile: float = Column(Float)
    state_team_count: int = Column(Integer)

    district_epa_rank: int = Column(Integer)
    district_epa_percentile: float = Column(Float)
    district_team_count: int = Column(Integer)


_TeamYear = generate_attr_class("TeamYear", TeamYearORM)


class TeamYear(_TeamYear):
    @classmethod
    def from_dict(cls, dict: Dict[str, Any]) -> "TeamYear":
        dict = {k: dict.get(k, None) for k in cls.__slots__}  # type: ignore
        return TeamYear(**dict)

    def as_dict(self: "TeamYear") -> Dict[str, Any]:
        return attr.asdict(
            self,  # type: ignore
            filter=attr.filters.exclude(
                attr.fields(TeamYear).id,  # type: ignore
                attr.fields(TeamYear).next_event_key,  # type: ignore
                attr.fields(TeamYear).next_event_name,  # type: ignore
                attr.fields(TeamYear).next_event_week,  # type: ignore
            ),
        )

    """SUPER FUNCTIONS"""

    def sort(self: Any) -> Tuple[str, int]:
        return (self.team, self.year)

    def __str__(self: Any):
        # Only refresh DB if these change (during 1 min partial update)
        return f"{self.team}_{self.year}_{self.count}"
