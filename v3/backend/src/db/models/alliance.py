from typing import Any, Dict, List, Optional

import attr
from sqlalchemy import Boolean, Float, Integer, String, Enum
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.sql.schema import ForeignKeyConstraint, PrimaryKeyConstraint

from src.types.enums import AllianceColor, MatchStatus, MatchWinner
from src.db.main import Base
from src.db.models.main import Model, ModelORM, generate_attr_class
from src.db.models.types import MB, MI, MOB, MOF, MOI, MOS, MS, values_callable


class AllianceORM(Base, ModelORM):
    """DECLARATION"""

    __tablename__ = "alliances"
    id: MOI = mapped_column(Integer, nullable=True)  # placeholder for backend API
    alliance: Mapped[AllianceColor] = mapped_column(
        Enum(AllianceColor, values_callable=values_callable), index=True
    )
    match: MS = mapped_column(String(20), index=True)

    year: MI = mapped_column(Integer, index=True)
    event: MS = mapped_column(String(12), index=True)

    PrimaryKeyConstraint(alliance, match)
    ForeignKeyConstraint(["year"], ["years.year"])
    ForeignKeyConstraint(["event"], ["events.key"])
    ForeignKeyConstraint(["match"], ["matches.key"])

    """GENERAL"""
    offseason: MB = mapped_column(Boolean, index=True)
    week: MI = mapped_column(Integer, index=True)
    elim: MB = mapped_column(Boolean, index=True)

    time: MI = mapped_column(Integer)

    status: Mapped[MatchStatus] = mapped_column(
        Enum(MatchStatus, values_callable=values_callable), index=True
    )

    team_1: MS = mapped_column(String(6), index=True)
    team_2: MS = mapped_column(String(6), index=True)
    team_3: MOS = mapped_column(String(6), index=True)
    dq: MS = mapped_column(String(20))
    surrogate: MS = mapped_column(String(20))

    """OUTCOME"""
    winner: Mapped[Optional[MatchWinner]] = mapped_column(
        Enum(MatchWinner, values_callable=values_callable), nullable=True, default=None
    )
    score: MOI = mapped_column(Integer, nullable=True, default=None)
    no_foul: MOI = mapped_column(Integer, nullable=True, default=None)
    foul: MOI = mapped_column(Integer, nullable=True, default=None)
    auto: MOI = mapped_column(Integer, nullable=True, default=None)
    teleop: MOI = mapped_column(Integer, nullable=True, default=None)
    endgame: MOI = mapped_column(Integer, nullable=True, default=None)
    rp_1: MOB = mapped_column(Boolean, nullable=True, default=None)
    rp_2: MOB = mapped_column(Boolean, nullable=True, default=None)
    tiebreaker: MOI = mapped_column(Integer, nullable=True, default=None)
    match_comp_1: MOI = mapped_column(Integer, nullable=True, default=None)
    match_comp_2: MOI = mapped_column(Integer, nullable=True, default=None)
    match_comp_3: MOI = mapped_column(Integer, nullable=True, default=None)
    match_comp_4: MOI = mapped_column(Integer, nullable=True, default=None)
    match_comp_5: MOI = mapped_column(Integer, nullable=True, default=None)
    match_comp_6: MOI = mapped_column(Integer, nullable=True, default=None)
    match_comp_7: MOI = mapped_column(Integer, nullable=True, default=None)
    match_comp_8: MOI = mapped_column(Integer, nullable=True, default=None)
    match_comp_9: MOI = mapped_column(Integer, nullable=True, default=None)
    match_comp_10: MOI = mapped_column(Integer, nullable=True, default=None)
    match_comp_11: MOI = mapped_column(Integer, nullable=True, default=None)
    match_comp_12: MOI = mapped_column(Integer, nullable=True, default=None)

    """EPA"""
    epa_winner: Mapped[Optional[MatchWinner]] = mapped_column(
        Enum(MatchWinner, values_callable=values_callable), nullable=True, default=None
    )
    epa_win_prob: MOF = mapped_column(Float, nullable=True, default=None)
    score_pred: MOF = mapped_column(Float, nullable=True, default=None)
    rp_1_pred: MOF = mapped_column(Float, nullable=True, default=None)
    rp_2_pred: MOF = mapped_column(Float, nullable=True, default=None)

    # auto_epa_sum: MOF = mapped_column(Float, nullable=True, default=None)
    # teleop_epa_sum: MOF = mapped_column(Float, nullable=True, default=None)
    # endgame_epa_sum: MOF = mapped_column(Float, nullable=True, default=None)
    # comp_1_epa_sum: MOF = mapped_column(Float, nullable=True, default=None)
    # comp_2_epa_sum: MOF = mapped_column(Float, nullable=True, default=None)
    # comp_3_epa_sum: MOF = mapped_column(Float, nullable=True, default=None)
    # comp_4_epa_sum: MOF = mapped_column(Float, nullable=True, default=None)
    # comp_5_epa_sum: MOF = mapped_column(Float, nullable=True, default=None)
    # comp_6_epa_sum: MOF = mapped_column(Float, nullable=True, default=None)
    # comp_7_epa_sum: MOF = mapped_column(Float, nullable=True, default=None)
    # comp_8_epa_sum: MOF = mapped_column(Float, nullable=True, default=None)
    # comp_9_epa_sum: MOF = mapped_column(Float, nullable=True, default=None)
    # comp_10_epa_sum: MOF = mapped_column(Float, nullable=True, default=None)


_Alliance = generate_attr_class("Alliance", AllianceORM)


class Alliance(_Alliance, Model):
    def to_dict(self: "Alliance") -> Dict[str, Any]:
        return attr.asdict(self)

    def sort(self: "Alliance") -> int:
        return self.time or 0

    def pk(self: "Alliance") -> str:
        return f"{self.match}_{self.alliance}"

    def __hash__(self: "Alliance") -> int:
        return hash(self.pk())

    def __str__(self: "Alliance") -> str:
        # Only refresh DB if these change (during 1 min partial update)
        return (
            f"{self.match}_{self.alliance}_{self.score}_{self.teleop}_{self.score_pred}"
        )

    """HELPER FUNCTIONS"""

    def get_teams(self: "Alliance") -> List[str]:
        return [x for x in [self.team_1, self.team_2, self.team_3] if x is not None]

    def get_surrogates(self: "Alliance") -> List[str]:
        return [x for x in self.surrogate.split(",") if x != ""]

    def get_dqs(self: "Alliance") -> List[str]:
        return [x for x in self.dq.split(",") if x != ""]
