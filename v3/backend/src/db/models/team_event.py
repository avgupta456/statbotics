from typing import Any, Dict, Tuple

import attr
from sqlalchemy import Boolean, Float, Integer, String, Enum
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.sql.schema import ForeignKeyConstraint, PrimaryKeyConstraint

from src.types.enums import EventStatus, EventType
from src.db.main import Base
from src.db.models.main import Model, ModelORM, generate_attr_class
from src.db.models.types import MB, MF, MI, MOF, MOI, MOS, MS, values_callable


class TeamEventORM(Base, ModelORM):
    """DECLARATIONS"""

    __tablename__ = "team_events"
    id: MOI = mapped_column(Integer, nullable=True)  # placeholder for backend API
    team: MS = mapped_column(String(6), index=True)
    year: MI = mapped_column(Integer, index=True)
    event: MS = mapped_column(String(12), index=True)

    PrimaryKeyConstraint(team, event)
    ForeignKeyConstraint(["team"], ["teams.team"])
    ForeignKeyConstraint(["year"], ["years.year"])
    ForeignKeyConstraint(["team", "year"], ["team_years.team", "team_years.year"])
    ForeignKeyConstraint(["event"], ["events.key"])

    """GENERAL"""
    time: MI = mapped_column(Integer)
    offseason: MB = mapped_column(Boolean)

    """API COMPLETENESS"""
    team_name: MS = mapped_column(String(100))
    event_name: MS = mapped_column(String(100))
    country: MOS = mapped_column(String(30), nullable=True)
    district: MOS = mapped_column(String(10), nullable=True)
    state: MOS = mapped_column(String(10), nullable=True)
    type: Mapped[EventType] = mapped_column(
        Enum(EventType, values_callable=values_callable)
    )
    week: MI = mapped_column(Integer)

    status: Mapped[EventStatus] = mapped_column(
        Enum(EventStatus, values_callable=values_callable)
    )
    first_event: MB = mapped_column(Boolean)

    """STATS"""
    wins: MI = mapped_column(Integer, default=0)
    losses: MI = mapped_column(Integer, default=0)
    ties: MI = mapped_column(Integer, default=0)
    count: MI = mapped_column(Integer, default=0)
    winrate: MF = mapped_column(Float, default=0)
    qual_wins: MI = mapped_column(Integer, default=0)
    qual_losses: MI = mapped_column(Integer, default=0)
    qual_ties: MI = mapped_column(Integer, default=0)
    qual_count: MI = mapped_column(Integer, default=0)
    qual_winrate: MF = mapped_column(Float, default=0)
    rps: MI = mapped_column(Integer, default=0)
    rps_per_match: MF = mapped_column(Float, default=0)
    rank: MOI = mapped_column(Integer, nullable=True, default=None)
    num_teams: MI = mapped_column(Integer, default=0)

    """EPA"""
    epa_start: MF = mapped_column(Float, default=0)
    epa_pre_elim: MF = mapped_column(Float, default=0)
    epa_mean: MF = mapped_column(Float, default=0)
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

    unitless_epa: MF = mapped_column(Float, default=0)
    norm_epa: MOF = mapped_column(Float, default=0)


_TeamEvent = generate_attr_class("TeamEvent", TeamEventORM)


class TeamEvent(_TeamEvent, Model):
    def to_dict(self: "TeamEvent") -> Dict[str, Any]:
        return attr.asdict(
            self,
            filter=attr.filters.exclude(
                attr.fields(TeamEvent).id, attr.fields(TeamEvent).time
            ),
        )

    def sort(self: "TeamEvent") -> Tuple[str, int]:
        return (self.team, self.time)

    def pk(self: "TeamEvent") -> str:
        return f"{self.team}_{self.event}"

    def __hash__(self: "TeamEvent") -> int:
        return hash(self.pk())

    def __str__(self: "TeamEvent") -> str:
        # Only refresh DB if these change (during 1 min partial update)
        return "_".join(
            [self.team, self.event, str(self.status), str(self.count), str(self.rank)]
        )
