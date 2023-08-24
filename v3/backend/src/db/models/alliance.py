from typing import Any, Dict, List

import attr
from sqlalchemy import Boolean, Float, Integer, String
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql.schema import ForeignKeyConstraint, PrimaryKeyConstraint

from src.db.main import Base
from src.db.models.main import Model, ModelORM, generate_attr_class
from src.db.models.types import MB, MI, MOB, MOF, MOI, MOS, MS


class AllianceORM(Base, ModelORM):
    """DECLARATION"""

    __tablename__ = "alliances"
    id: MOI = mapped_column(Integer, nullable=True)  # placeholder for backend API
    alliance: MS = mapped_column(String(4), index=True)
    match: MS = mapped_column(String(20), index=True)

    year: MI = mapped_column(Integer, index=True)
    event: MS = mapped_column(String(20), index=True)

    PrimaryKeyConstraint(alliance, match)
    ForeignKeyConstraint(["year"], ["years.year"])
    ForeignKeyConstraint(["event"], ["events.key"])
    ForeignKeyConstraint(["match"], ["matches.key"])

    """GENERAL"""
    offseason: MB = mapped_column(Boolean, index=True)
    week: MI = mapped_column(Integer, index=True)
    elim: MB = mapped_column(Boolean, index=True)

    time: MI = mapped_column(Integer)

    # Choices are 'Upcoming', 'Completed'
    status: MS = mapped_column(String(10), index=True)

    team_1: MS = mapped_column(String(6), index=True)
    team_2: MS = mapped_column(String(6), index=True)
    team_3: MOS = mapped_column(String(6), index=True)
    dq: MS = mapped_column(String(20))
    surrogate: MS = mapped_column(String(20))

    """OUTCOME"""
    official_winner: MOS = mapped_column(String(4), nullable=True, default=None)
    winner: MOS = mapped_column(String(4), nullable=True, default=None)
    score: MOI = mapped_column(Integer, nullable=True, default=None)
    no_foul: MOI = mapped_column(Integer, nullable=True, default=None)
    foul: MOI = mapped_column(Integer, nullable=True, default=None)
    auto: MOI = mapped_column(Integer, nullable=True, default=None)
    teleop: MOI = mapped_column(Integer, nullable=True, default=None)
    endgame: MOI = mapped_column(Integer, nullable=True, default=None)
    rp_1: MOB = mapped_column(Boolean, nullable=True, default=None)
    rp_2: MOB = mapped_column(Boolean, nullable=True, default=None)
    comp_1: MOF = mapped_column(Float, nullable=True, default=None)
    comp_2: MOF = mapped_column(Float, nullable=True, default=None)
    comp_3: MOF = mapped_column(Float, nullable=True, default=None)
    comp_4: MOF = mapped_column(Float, nullable=True, default=None)
    comp_5: MOF = mapped_column(Float, nullable=True, default=None)
    comp_6: MOF = mapped_column(Float, nullable=True, default=None)
    comp_7: MOF = mapped_column(Float, nullable=True, default=None)
    comp_8: MOF = mapped_column(Float, nullable=True, default=None)
    comp_9: MOF = mapped_column(Float, nullable=True, default=None)
    comp_10: MOF = mapped_column(Float, nullable=True, default=None)
    tiebreaker: MOF = mapped_column(Float, nullable=True, default=None)

    """EPA"""
    # TODO: implement all of these, make non-nullable
    epa_winner: MOS = mapped_column(String(4), nullable=True, default=None)
    epa_win_prob: MOF = mapped_column(Float, nullable=True, default=None)
    rp_1_prob: MOF = mapped_column(Float, nullable=True, default=None)
    rp_2_prob: MOF = mapped_column(Float, nullable=True, default=None)

    epa_sum: MOF = mapped_column(Float, nullable=True, default=None)
    auto_epa_sum: MOF = mapped_column(Float, nullable=True, default=None)
    teleop_epa_sum: MOF = mapped_column(Float, nullable=True, default=None)
    endgame_epa_sum: MOF = mapped_column(Float, nullable=True, default=None)
    comp_1_epa_sum: MOF = mapped_column(Float, nullable=True, default=None)
    comp_2_epa_sum: MOF = mapped_column(Float, nullable=True, default=None)
    comp_3_epa_sum: MOF = mapped_column(Float, nullable=True, default=None)
    comp_4_epa_sum: MOF = mapped_column(Float, nullable=True, default=None)
    comp_5_epa_sum: MOF = mapped_column(Float, nullable=True, default=None)
    comp_6_epa_sum: MOF = mapped_column(Float, nullable=True, default=None)
    comp_7_epa_sum: MOF = mapped_column(Float, nullable=True, default=None)
    comp_8_epa_sum: MOF = mapped_column(Float, nullable=True, default=None)
    comp_9_epa_sum: MOF = mapped_column(Float, nullable=True, default=None)
    comp_10_epa_sum: MOF = mapped_column(Float, nullable=True, default=None)
    rp_1_epa_sum: MOF = mapped_column(Float, nullable=True, default=None)
    rp_2_epa_sum: MOF = mapped_column(Float, nullable=True, default=None)


_Alliance = generate_attr_class("Alliance", AllianceORM)


class Alliance(_Alliance, Model):
    def to_dict(self: "Alliance") -> Dict[str, Any]:
        return attr.asdict(self)

    def sort(self: "Alliance") -> int:
        return self.time or 0

    def pk(self: "Alliance") -> str:
        return f"{self.match}_{self.alliance}"

    def __str__(self: "Alliance") -> str:
        # Only refresh DB if these change (during 1 min partial update)
        return f"{self.match}_{self.alliance}_{self.score}_{self.teleop}_{self.epa_sum}"

    """HELPER FUNCTIONS"""

    def get_teams(self: "Alliance") -> List[str]:
        return [x for x in [self.team_1, self.team_2, self.team_3] if x is not None]

    def get_surrogates(self: "Alliance") -> List[str]:
        return [x for x in self.surrogate.split(",") if x != ""]

    def get_dqs(self: "Alliance") -> List[str]:
        return [x for x in self.dq.split(",") if x != ""]
