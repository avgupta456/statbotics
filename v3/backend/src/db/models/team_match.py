from typing import Any, Dict

import attr
from sqlalchemy import Boolean, Float, Integer, String, Enum
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.sql.schema import ForeignKeyConstraint, PrimaryKeyConstraint

from src.types.enums import MatchStatus, AllianceColor
from src.db.main import Base
from src.db.models.main import Model, ModelORM, generate_attr_class
from src.db.models.types import MB, MF, MI, MOF, MOI, MS, values_callable


class TeamMatchORM(Base, ModelORM):
    """DECLARATION"""

    __tablename__ = "team_matches"
    id: MOI = mapped_column(Integer, nullable=True)  # placeholder for backend API
    team: MS = mapped_column(String(6), index=True)
    year: MI = mapped_column(Integer, index=True)
    event: MS = mapped_column(String(12), index=True)
    match: MS = mapped_column(String(20), index=True)
    alliance: Mapped[AllianceColor] = mapped_column(
        Enum(AllianceColor, values_callable=values_callable), index=True
    )

    PrimaryKeyConstraint(team, match)
    ForeignKeyConstraint(["year"], ["years.year"])
    ForeignKeyConstraint(["team"], ["teams.team"])
    ForeignKeyConstraint(["event"], ["events.key"])
    ForeignKeyConstraint(["match"], ["matches.key"])
    ForeignKeyConstraint(["team", "year"], ["team_years.team", "team_years.year"])
    ForeignKeyConstraint(["team", "event"], ["team_events.team", "team_events.event"])
    ForeignKeyConstraint(
        ["match", "alliance"], ["alliances.match", "alliances.alliance"]
    )

    """GENERAL"""
    time: MI = mapped_column(Integer)
    offseason: MB = mapped_column(Boolean)
    week: MI = mapped_column(Integer)
    elim: MB = mapped_column(Boolean)

    dq: MB = mapped_column(Boolean)
    surrogate: MB = mapped_column(Boolean)

    status: Mapped[MatchStatus] = mapped_column(
        Enum(MatchStatus, values_callable=values_callable)
    )

    epa: MF = mapped_column(Float, default=0)
    auto_epa: MOF = mapped_column(Float, nullable=True, default=None)
    teleop_epa: MOF = mapped_column(Float, nullable=True, default=None)
    endgame_epa: MOF = mapped_column(Float, nullable=True, default=None)
    rp_1_epa: MOF = mapped_column(Float, nullable=True, default=None)
    rp_2_epa: MOF = mapped_column(Float, nullable=True, default=None)
    tiebreaker_epa: MOF = mapped_column(Float, nullable=True, default=None)
    comp_1_epa: MOF = mapped_column(Float, nullable=True, default=None)
    comp_2_epa: MOF = mapped_column(Float, nullable=True, default=None)
    comp_3_epa: MOF = mapped_column(Float, nullable=True, default=None)
    comp_4_epa: MOF = mapped_column(Float, nullable=True, default=None)
    comp_5_epa: MOF = mapped_column(Float, nullable=True, default=None)
    comp_6_epa: MOF = mapped_column(Float, nullable=True, default=None)
    comp_7_epa: MOF = mapped_column(Float, nullable=True, default=None)
    comp_8_epa: MOF = mapped_column(Float, nullable=True, default=None)
    comp_9_epa: MOF = mapped_column(Float, nullable=True, default=None)
    comp_10_epa: MOF = mapped_column(Float, nullable=True, default=None)
    comp_11_epa: MOF = mapped_column(Float, nullable=True, default=None)
    comp_12_epa: MOF = mapped_column(Float, nullable=True, default=None)
    comp_13_epa: MOF = mapped_column(Float, nullable=True, default=None)
    comp_14_epa: MOF = mapped_column(Float, nullable=True, default=None)
    comp_15_epa: MOF = mapped_column(Float, nullable=True, default=None)
    comp_16_epa: MOF = mapped_column(Float, nullable=True, default=None)
    comp_17_epa: MOF = mapped_column(Float, nullable=True, default=None)
    comp_18_epa: MOF = mapped_column(Float, nullable=True, default=None)
    post_epa: MOF = mapped_column(Float, nullable=True, default=None)


_TeamMatch = generate_attr_class("TeamMatch", TeamMatchORM)


class TeamMatch(_TeamMatch, Model):
    def to_dict(self: "TeamMatch") -> Dict[str, Any]:
        return attr.asdict(self, filter=attr.filters.exclude(attr.fields(TeamMatch).id))

    def sort(self: "TeamMatch") -> int:
        return self.time

    def pk(self: "TeamMatch") -> str:
        return f"{self.team}_{self.match}"

    def __hash__(self: "TeamMatch") -> int:
        return hash(self.pk())

    def __str__(self: "TeamMatch") -> str:
        # Only refresh DB if these change (during 1 min partial update)
        return "_".join(
            [self.team, self.match, str(self.status), str(self.epa), str(self.post_epa)]
        )
