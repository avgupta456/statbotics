from typing import Any, Dict, Tuple

import attr
from sqlalchemy import Boolean, Float, Integer, String
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql.schema import ForeignKeyConstraint, PrimaryKeyConstraint

from src.db.main import Base
from src.db.models.main import Model, ModelORM, generate_attr_class
from src.db.models.types import MB, MF, MI, MOF, MOS, MS


class TeamEventORM(Base, ModelORM):
    """DECLARATIONS"""

    __tablename__ = "team_events"
    id: MI = mapped_column(Integer, nullable=True)  # placeholder for backend API
    team: MS = mapped_column(String(6), index=True)
    year: MI = mapped_column(Integer, index=True)
    event: MS = mapped_column(String(10), index=True)

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
    country: MOS = mapped_column(String(30))
    district: MOS = mapped_column(String(10))
    state: MOS = mapped_column(String(10))
    type: MI = mapped_column(Integer)
    week: MI = mapped_column(Integer)

    # Choices are 'Upcoming', 'Ongoing', 'Completed'
    status: MS = mapped_column(String(10))
    first_event: MB = mapped_column(Boolean)

    """EPA"""
    epa_start: MF = mapped_column(Float)
    epa_pre_playoffs: MF = mapped_column(Float)
    epa_end: MF = mapped_column(Float)
    epa_mean: MF = mapped_column(Float)
    epa_max: MF = mapped_column(Float)
    epa_diff: MF = mapped_column(Float)

    auto_epa_start: MOF = mapped_column(Float, nullable=True)
    auto_epa_pre_playoffs: MOF = mapped_column(Float, nullable=True)
    auto_epa_end: MOF = mapped_column(Float, nullable=True)
    auto_epa_mean: MOF = mapped_column(Float, nullable=True)
    auto_epa_max: MOF = mapped_column(Float, nullable=True)

    teleop_epa_start: MOF = mapped_column(Float, nullable=True)
    teleop_epa_pre_playoffs: MOF = mapped_column(Float, nullable=True)
    teleop_epa_end: MOF = mapped_column(Float, nullable=True)
    teleop_epa_mean: MOF = mapped_column(Float, nullable=True)
    teleop_epa_max: MOF = mapped_column(Float, nullable=True)

    endgame_epa_start: MOF = mapped_column(Float, nullable=True)
    endgame_epa_pre_playoffs: MOF = mapped_column(Float, nullable=True)
    endgame_epa_end: MOF = mapped_column(Float, nullable=True)
    endgame_epa_mean: MOF = mapped_column(Float, nullable=True)
    endgame_epa_max: MOF = mapped_column(Float, nullable=True)

    rp_1_epa_start: MOF = mapped_column(Float, nullable=True)
    rp_1_epa_end: MOF = mapped_column(Float, nullable=True)
    rp_1_epa_mean: MOF = mapped_column(Float, nullable=True)
    rp_1_epa_max: MOF = mapped_column(Float, nullable=True)

    rp_2_epa_start: MOF = mapped_column(Float, nullable=True)
    rp_2_epa_end: MOF = mapped_column(Float, nullable=True)
    rp_2_epa_mean: MOF = mapped_column(Float, nullable=True)
    rp_2_epa_max: MOF = mapped_column(Float, nullable=True)

    # TODO: populate unitless_epa_end, make not nullable
    unitless_epa_end: MOF = mapped_column(Float, nullable=True)
    norm_epa_end: MOF = mapped_column(Float, nullable=True)

    """STATS"""
    wins: MI = mapped_column(Integer)
    losses: MI = mapped_column(Integer)
    ties: MI = mapped_column(Integer)
    count: MI = mapped_column(Integer)
    winrate: MF = mapped_column(Float)
    qual_wins: MI = mapped_column(Integer)
    qual_losses: MI = mapped_column(Integer)
    qual_ties: MI = mapped_column(Integer)
    qual_count: MI = mapped_column(Integer)
    qual_winrate: MF = mapped_column(Float)
    rps: MI = mapped_column(Integer)
    rps_per_match: MF = mapped_column(Float)
    rank: MI = mapped_column(Integer)
    num_teams: MI = mapped_column(Integer)


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

    def __str__(self: "TeamEvent") -> str:
        # Only refresh DB if these change (during 1 min partial update)
        return f"{self.team}_{self.event}_{self.status}_{self.count}_{self.rank}"
