from typing import Any, Dict

import attr
from sqlalchemy import Boolean, Float, Integer, String
from sqlalchemy.sql.schema import ForeignKeyConstraint, PrimaryKeyConstraint
from sqlalchemy.orm import mapped_column

from src.db.main import Base
from src.db.models.main import ModelORM, Model, generate_attr_class
from src.db.models.types import MI, MS, MF, MB, MOF


class TeamMatchORM(Base, ModelORM):
    """DECLARATION"""

    __tablename__ = "team_matches"
    id: MI = mapped_column(Integer, nullable=True)  # placeholder for backend API
    team: MS = mapped_column(String(6), index=True)
    year: MI = mapped_column(Integer, index=True)
    event: MS = mapped_column(String(20), index=True)
    match: MS = mapped_column(String(20), index=True)
    alliance: MS = mapped_column(String(6), index=True)

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
    playoff: MB = mapped_column(Boolean)
    alliance: MS = mapped_column(String(6))

    dq: MB = mapped_column(Boolean)
    surrogate: MB = mapped_column(Boolean)

    # Choices are 'Upcoming', 'Completed'
    status: MS = mapped_column(String(10))

    epa: MF = mapped_column(Float)
    auto_epa: MOF = mapped_column(Float, nullable=True)
    teleop_epa: MOF = mapped_column(Float, nullable=True)
    endgame_epa: MOF = mapped_column(Float, nullable=True)
    rp_1_epa: MOF = mapped_column(Float, nullable=True)
    rp_2_epa: MOF = mapped_column(Float, nullable=True)

    post_epa: MOF = mapped_column(Float)


_TeamMatch = generate_attr_class("TeamMatch", TeamMatchORM)


class TeamMatch(_TeamMatch, Model):
    def to_dict(self: "TeamMatch") -> Dict[str, Any]:
        return attr.asdict(self, filter=attr.filters.exclude(attr.fields(TeamMatch).id))

    def sort(self: "TeamMatch") -> int:
        return self.time

    def pk(self: "TeamMatch") -> str:
        return f"{self.team}_{self.match}"

    def __str__(self: "TeamMatch") -> str:
        # Only refresh DB if these change (during 1 min partial update)
        return f"{self.team}_{self.match}_{self.status}_{self.epa}_{self.post_epa}"
