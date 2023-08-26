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
    epa_end: MF = mapped_column(Float, index=True, default=0)
    epa_max: MF = mapped_column(Float, default=0)

    # auto_epa_start: MOF = mapped_column(Float, nullable=True, default=None)
    # auto_epa_pre_champs: MOF = mapped_column(Float, nullable=True, default=None)
    # auto_epa_end: MOF = mapped_column(Float, nullable=True, default=None)
    # auto_epa_max: MOF = mapped_column(Float, nullable=True, default=None)

    # teleop_epa_start: MOF = mapped_column(Float, nullable=True, default=None)
    # teleop_epa_pre_champs: MOF = mapped_column(Float, nullable=True, default=None)
    # teleop_epa_end: MOF = mapped_column(Float, nullable=True, default=None)
    # teleop_epa_max: MOF = mapped_column(Float, nullable=True, default=None)

    # endgame_epa_start: MOF = mapped_column(Float, nullable=True, default=None)
    # endgame_epa_pre_champs: MOF = mapped_column(Float, nullable=True, default=None)
    # endgame_epa_end: MOF = mapped_column(Float, nullable=True, default=None)
    # endgame_epa_max: MOF = mapped_column(Float, nullable=True, default=None)

    rp_1_epa_start: MOF = mapped_column(Float, nullable=True, default=None)
    rp_1_epa_pre_champs: MOF = mapped_column(Float, nullable=True, default=None)
    rp_1_epa_end: MOF = mapped_column(Float, nullable=True, default=None)
    rp_1_epa_max: MOF = mapped_column(Float, nullable=True, default=None)

    rp_2_epa_start: MOF = mapped_column(Float, nullable=True, default=None)
    rp_2_epa_pre_champs: MOF = mapped_column(Float, nullable=True, default=None)
    rp_2_epa_end: MOF = mapped_column(Float, nullable=True, default=None)
    rp_2_epa_max: MOF = mapped_column(Float, nullable=True, default=None)

    unitless_epa_end: MF = mapped_column(Float, default=0)
    norm_epa_end: MOF = mapped_column(Float, default=0)

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
        return f"{self.team}_{self.year}_{self.count}"
