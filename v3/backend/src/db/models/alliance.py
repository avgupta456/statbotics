from typing import Any, Dict, List, Optional

import numpy as np
from sqlalchemy import Boolean, Enum, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.schema import ForeignKeyConstraint, PrimaryKeyConstraint

from src.breakdown import key_to_name
from src.db.main import Base
from src.db.models.main import Model, ModelORM, generate_attr_class
from src.db.models.types import MB, MI, MOB, MOF, MOI, MOS, MS, values_callable
from src.types.enums import AllianceColor, MatchStatus, MatchWinner


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
    comp_11: MOF = mapped_column(Float, nullable=True, default=None)
    comp_12: MOF = mapped_column(Float, nullable=True, default=None)
    comp_13: MOF = mapped_column(Float, nullable=True, default=None)
    comp_14: MOF = mapped_column(Float, nullable=True, default=None)
    comp_15: MOF = mapped_column(Float, nullable=True, default=None)
    comp_16: MOF = mapped_column(Float, nullable=True, default=None)
    comp_17: MOF = mapped_column(Float, nullable=True, default=None)
    comp_18: MOF = mapped_column(Float, nullable=True, default=None)

    """EPA"""
    epa_winner: Mapped[Optional[MatchWinner]] = mapped_column(
        Enum(MatchWinner, values_callable=values_callable), nullable=True, default=None
    )
    epa_win_prob: MOF = mapped_column(Float, nullable=True, default=None)
    score_pred: MOF = mapped_column(Float, nullable=True, default=None)
    rp_1_pred: MOF = mapped_column(Float, nullable=True, default=None)
    rp_2_pred: MOF = mapped_column(Float, nullable=True, default=None)


_Alliance = generate_attr_class("Alliance", AllianceORM)


class Alliance(_Alliance, Model):
    def sort(self: "Alliance") -> int:
        return self.time or 0

    def pk(self: "Alliance") -> str:
        return f"{self.match}_{self.alliance}"

    def __hash__(self: "Alliance") -> int:
        return hash(self.pk())

    def __str__(self: "Alliance") -> str:
        # Only refresh DB if these change (during 1 min partial update)
        return "_".join(
            [
                self.match,
                self.alliance,
                str(self.score),
                str(self.teleop),
                str(self.score_pred),
            ]
        )

    """HELPER FUNCTIONS"""

    def get_teams(self: "Alliance") -> List[str]:
        return [x for x in [self.team_1, self.team_2, self.team_3] if x is not None]

    def get_surrogates(self: "Alliance") -> List[str]:
        return [x for x in self.surrogate.split(",") if x != ""]

    def get_dqs(self: "Alliance") -> List[str]:
        return [x for x in self.dq.split(",") if x != ""]

    def get_breakdown(self: "Alliance") -> Any:
        if self.year < 2016:
            return np.array([self.score or 0])
        return np.array(
            [
                self.no_foul or 0,
                self.auto or 0,
                self.teleop or 0,
                self.endgame or 0,
                int(self.rp_1 or False),
                int(self.rp_2 or False),
                self.tiebreaker or 0,
                self.comp_1 or 0,
                self.comp_2 or 0,
                self.comp_3 or 0,
                self.comp_4 or 0,
                self.comp_5 or 0,
                self.comp_6 or 0,
                self.comp_7 or 0,
                self.comp_8 or 0,
                self.comp_9 or 0,
                self.comp_10 or 0,
                self.comp_11 or 0,
                self.comp_12 or 0,
                self.comp_13 or 0,
                self.comp_14 or 0,
                self.comp_15 or 0,
                self.comp_16 or 0,
                self.comp_17 or 0,
                self.comp_18 or 0,
            ]
        )

    def to_dict(self: "Alliance") -> Dict[str, Any]:
        clean: Dict[str, Any] = {
            "match": self.match,
            "alliance": self.alliance,
            "year": self.year,
            "event": self.event,
            "offseason": self.offseason,
            "week": self.week,
            "elim": self.elim,
            "time": self.time,
            "status": self.status,
            "teams": self.get_teams(),
            "dq": self.get_dqs(),
            "surrogate": self.get_surrogates(),
            "pred": {
                "winner": self.epa_winner,
                "red_win_prob": self.epa_win_prob,
                "score": self.score_pred,
            },
            "result": {
                "winner": self.winner,
                "score": self.score,
            },
        }

        if self.year >= 2016:
            rp_1_name = key_to_name[self.year]["rp_1"]
            rp_2_name = key_to_name[self.year]["rp_2"]

            clean["pred"][rp_1_name] = self.rp_1_pred
            clean["pred"][rp_2_name] = self.rp_2_pred

            for k in ["auto", "teleop", "endgame", "rp_1", "rp_2", "tiebreaker"] + [
                f"comp_{i}" for i in range(1, 19)
            ]:
                if k not in key_to_name[self.year]:
                    continue
                name = key_to_name[self.year][k]
                clean["result"][name] = getattr(self, k)

        return clean
