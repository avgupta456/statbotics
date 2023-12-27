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
    id: MOI = mapped_column(Integer, nullable=True)  # placeholder for backend API
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
    competing_this_week: MB = mapped_column(Boolean)
    next_event_key: MOS = mapped_column(String(10), nullable=True)
    next_event_name: MOS = mapped_column(String(100), nullable=True)
    next_event_week: MOI = mapped_column(Integer, nullable=True)

    """EPA"""
    epa_start: MF = mapped_column(Float, default=0)
    epa_pre_champs: MF = mapped_column(Float, default=0)
    epa_max: MF = mapped_column(Float, default=0)

    epa: MF = mapped_column(Float, index=True, default=0)
    epa_sd: MF = mapped_column(Float, default=0)
    epa_skew: MF = mapped_column(Float, default=0)
    auto_epa: MOF = mapped_column(Float, default=None)
    auto_epa_sd: MOF = mapped_column(Float, default=None)
    teleop_epa: MOF = mapped_column(Float, default=None)
    teleop_epa_sd: MOF = mapped_column(Float, default=None)
    endgame_epa: MOF = mapped_column(Float, default=None)
    endgame_epa_sd: MOF = mapped_column(Float, default=None)
    rp_1_epa: MOF = mapped_column(Float, default=None)
    rp_1_epa_sd: MOF = mapped_column(Float, default=None)
    rp_2_epa: MOF = mapped_column(Float, default=None)
    rp_2_epa_sd: MOF = mapped_column(Float, default=None)
    tiebreaker_epa: MOF = mapped_column(Float, default=None)
    tiebreaker_epa_sd: MOF = mapped_column(Float, default=None)
    comp_1_epa: MOF = mapped_column(Float, default=None)
    comp_1_epa_sd: MOF = mapped_column(Float, default=None)
    comp_2_epa: MOF = mapped_column(Float, default=None)
    comp_2_epa_sd: MOF = mapped_column(Float, default=None)
    comp_3_epa: MOF = mapped_column(Float, default=None)
    comp_3_epa_sd: MOF = mapped_column(Float, default=None)
    comp_4_epa: MOF = mapped_column(Float, default=None)
    comp_4_epa_sd: MOF = mapped_column(Float, default=None)
    comp_5_epa: MOF = mapped_column(Float, default=None)
    comp_5_epa_sd: MOF = mapped_column(Float, default=None)
    comp_6_epa: MOF = mapped_column(Float, default=None)
    comp_6_epa_sd: MOF = mapped_column(Float, default=None)
    comp_7_epa: MOF = mapped_column(Float, default=None)
    comp_7_epa_sd: MOF = mapped_column(Float, default=None)
    comp_8_epa: MOF = mapped_column(Float, default=None)
    comp_8_epa_sd: MOF = mapped_column(Float, default=None)
    comp_9_epa: MOF = mapped_column(Float, default=None)
    comp_9_epa_sd: MOF = mapped_column(Float, default=None)
    comp_10_epa: MOF = mapped_column(Float, default=None)
    comp_10_epa_sd: MOF = mapped_column(Float, default=None)
    comp_11_epa: MOF = mapped_column(Float, default=None)
    comp_11_epa_sd: MOF = mapped_column(Float, default=None)
    comp_12_epa: MOF = mapped_column(Float, default=None)
    comp_12_epa_sd: MOF = mapped_column(Float, default=None)
    comp_13_epa: MOF = mapped_column(Float, default=None)
    comp_13_epa_sd: MOF = mapped_column(Float, default=None)
    comp_14_epa: MOF = mapped_column(Float, default=None)
    comp_14_epa_sd: MOF = mapped_column(Float, default=None)
    comp_15_epa: MOF = mapped_column(Float, default=None)
    comp_15_epa_sd: MOF = mapped_column(Float, default=None)
    comp_16_epa: MOF = mapped_column(Float, default=None)
    comp_16_epa_sd: MOF = mapped_column(Float, default=None)
    comp_17_epa: MOF = mapped_column(Float, default=None)
    comp_17_epa_sd: MOF = mapped_column(Float, default=None)
    comp_18_epa: MOF = mapped_column(Float, default=None)
    comp_18_epa_sd: MOF = mapped_column(Float, default=None)

    unitless_epa: MF = mapped_column(Float, default=0)
    norm_epa: MOF = mapped_column(Float, default=0)

    """STATS"""
    wins: MI = mapped_column(Integer, default=0)  # competition season only
    losses: MI = mapped_column(Integer, default=0)
    ties: MI = mapped_column(Integer, default=0)
    count: MI = mapped_column(Integer, default=0)
    winrate: MF = mapped_column(Float, default=0)

    full_wins: MI = mapped_column(Integer, default=0)  # includes offseason
    full_losses: MI = mapped_column(Integer, default=0)
    full_ties: MI = mapped_column(Integer, default=0)
    full_count: MI = mapped_column(Integer, default=0)
    full_winrate: MF = mapped_column(Float, default=0)

    total_epa_rank: MOI = mapped_column(Integer, nullable=True, default=None)
    total_epa_percentile: MOF = mapped_column(Float, nullable=True, default=None)
    total_team_count: MOI = mapped_column(Integer, nullable=True, default=None)

    country_epa_rank: MOI = mapped_column(Integer, nullable=True, default=None)
    country_epa_percentile: MOF = mapped_column(Float, nullable=True, default=None)
    country_team_count: MOI = mapped_column(Integer, nullable=True, default=None)

    district_epa_rank: MOI = mapped_column(Integer, nullable=True, default=None)
    district_epa_percentile: MOF = mapped_column(Float, nullable=True, default=None)
    district_team_count: MOI = mapped_column(Integer, nullable=True, default=None)

    state_epa_rank: MOI = mapped_column(Integer, nullable=True, default=None)
    state_epa_percentile: MOF = mapped_column(Float, nullable=True, default=None)
    state_team_count: MOI = mapped_column(Integer, nullable=True, default=None)


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

    def __hash__(self: "TeamYear") -> int:
        return hash(self.pk())

    def __str__(self: "TeamYear") -> str:
        # Only refresh DB if these change (during 1 min partial update)
        return "_".join([self.team, str(self.year), str(self.count)])
