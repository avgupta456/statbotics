from typing import Any, Dict, Tuple

import attr
from sqlalchemy import Boolean, Float, Integer, String
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql.schema import ForeignKeyConstraint, PrimaryKeyConstraint

from src.db.main import Base
from src.db.models.main import Model, ModelORM, generate_attr_class
from src.db.models.types import MB, MF, MI, MOF, MOI, MOS, MS


class TeamYearORM(Base, ModelORM):
    """DECLARATION"""

    __tablename__ = "team_years"
    id: MI = mapped_column(Integer, nullable=True)  # placeholder for backend API
    year: MI = mapped_column(Integer, index=True)
    team: MS = mapped_column(String(6), index=True)

    # force unique (team, year)
    PrimaryKeyConstraint(team, year)
    ForeignKeyConstraint(["year"], ["years.year"])
    ForeignKeyConstraint(["team"], ["teams.team"])

    """API COMPLETENESS"""
    offseason: MB = mapped_column(Boolean)
    name: MS = mapped_column(String(100))
    country: MOS = mapped_column(String(30))
    district: MOS = mapped_column(String(10))
    state: MOS = mapped_column(String(10))

    """PRE JOINS (FOR FRONTEND LOAD TIME)"""
    # TODO: replace is_competing with better method or at least rename
    is_competing: MB = mapped_column(Boolean)
    next_event_key: MOS = mapped_column(String(10), nullable=True)
    next_event_name: MOS = mapped_column(String(100), nullable=True)
    next_event_week: MOI = mapped_column(Integer, nullable=True)

    """EPA"""
    epa_start: MF = mapped_column(Float)
    epa_pre_champs: MF = mapped_column(Float)
    epa_end: MF = mapped_column(Float, index=True)
    epa_mean: MF = mapped_column(Float)
    epa_max: MF = mapped_column(Float)
    epa_diff: MF = mapped_column(Float)

    auto_epa_start: MOF = mapped_column(Float, nullable=True)
    auto_epa_pre_champs: MOF = mapped_column(Float, nullable=True)
    auto_epa_end: MOF = mapped_column(Float, nullable=True)
    auto_epa_mean: MOF = mapped_column(Float, nullable=True)
    auto_epa_max: MOF = mapped_column(Float, nullable=True)

    teleop_epa_start: MOF = mapped_column(Float, nullable=True)
    teleop_epa_pre_champs: MOF = mapped_column(Float, nullable=True)
    teleop_epa_end: MOF = mapped_column(Float, nullable=True)
    teleop_epa_mean: MOF = mapped_column(Float, nullable=True)
    teleop_epa_max: MOF = mapped_column(Float, nullable=True)

    endgame_epa_start: MOF = mapped_column(Float, nullable=True)
    endgame_epa_pre_champs: MOF = mapped_column(Float, nullable=True)
    endgame_epa_end: MOF = mapped_column(Float, nullable=True)
    endgame_epa_mean: MOF = mapped_column(Float, nullable=True)
    endgame_epa_max: MOF = mapped_column(Float, nullable=True)

    rp_1_epa_start: MOF = mapped_column(Float, nullable=True)
    rp_1_epa_pre_champs: MOF = mapped_column(Float, nullable=True)
    rp_1_epa_end: MOF = mapped_column(Float, nullable=True)
    rp_1_epa_mean: MOF = mapped_column(Float, nullable=True)
    rp_1_epa_max: MOF = mapped_column(Float, nullable=True)

    rp_2_epa_start: MOF = mapped_column(Float, nullable=True)
    rp_2_epa_pre_champs: MOF = mapped_column(Float, nullable=True)
    rp_2_epa_end: MOF = mapped_column(Float, nullable=True)
    rp_2_epa_mean: MOF = mapped_column(Float, nullable=True)
    rp_2_epa_max: MOF = mapped_column(Float, nullable=True)

    """NORM EPA"""
    unitless_epa_end: MF = mapped_column(Float)
    norm_epa_end: MOF = mapped_column(Float)

    """STATS"""
    wins: MI = mapped_column(Integer)  # competition season only
    losses: MI = mapped_column(Integer)
    ties: MI = mapped_column(Integer)
    count: MI = mapped_column(Integer)
    winrate: MF = mapped_column(Float)

    full_wins: MI = mapped_column(Integer)  # includes offseason
    full_losses: MI = mapped_column(Integer)
    full_ties: MI = mapped_column(Integer)
    full_count: MI = mapped_column(Integer)
    full_winrate: MF = mapped_column(Float)

    total_epa_rank: MOI = mapped_column(Integer, nullable=True)
    total_epa_percentile: MOF = mapped_column(Float, nullable=True)
    total_team_count: MOI = mapped_column(Integer, nullable=True)

    country_epa_rank: MOI = mapped_column(Integer, nullable=True)
    country_epa_percentile: MOF = mapped_column(Float, nullable=True)
    country_team_count: MOI = mapped_column(Integer, nullable=True)

    state_epa_rank: MOI = mapped_column(Integer, nullable=True)
    state_epa_percentile: MOF = mapped_column(Float, nullable=True)
    state_team_count: MOI = mapped_column(Integer, nullable=True)

    district_epa_rank: MOI = mapped_column(Integer, nullable=True)
    district_epa_percentile: MOF = mapped_column(Float, nullable=True)
    district_team_count: MOI = mapped_column(Integer, nullable=True)


_TeamYear = generate_attr_class("TeamYear", TeamYearORM)


class TeamYear(_TeamYear, Model):
    def to_dict(self: "TeamYear") -> Dict[str, Any]:
        return attr.asdict(
            self,
            filter=attr.filters.exclude(
                attr.fields(TeamYear).id,
                attr.fields(TeamYear).next_event_key,
                attr.fields(TeamYear).next_event_name,
                attr.fields(TeamYear).next_event_week,
            ),
        )

    def sort(self: "TeamYear") -> Tuple[str, int]:
        return (self.team, self.year)

    def pk(self: "TeamYear") -> str:
        return f"{self.team}_{self.year}"

    def __str__(self: "TeamYear") -> str:
        # Only refresh DB if these change (during 1 min partial update)
        return f"{self.team}_{self.year}_{self.count}"
