from typing import Any, Dict, List, Optional, Tuple

import numpy as np
from sqlalchemy import Boolean, Enum, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.schema import ForeignKeyConstraint, PrimaryKeyConstraint

from src.breakdown import key_to_name
from src.db.main import Base
from src.db.models.main import Model, ModelORM, generate_attr_class
from src.db.models.types import MB, MI, MOB, MOF, MOI, MOS, MS, values_callable
from src.types.enums import CompLevel, MatchStatus, MatchWinner
from src.utils.utils import get_match_name


class MatchORM(Base, ModelORM):
    """DECLARATION"""

    __tablename__ = "matches"
    key: MS = mapped_column(String(20))
    year: MI = mapped_column(Integer, index=True)
    event: MS = mapped_column(String(12), index=True)

    PrimaryKeyConstraint(key)
    ForeignKeyConstraint(["year"], ["years.year"])
    ForeignKeyConstraint(["event"], ["events.key"])

    """GENERAL"""
    week: MI = mapped_column(Integer)
    elim: MB = mapped_column(Boolean)

    comp_level: Mapped[CompLevel] = mapped_column(
        Enum(CompLevel, values_callable=values_callable)
    )
    set_number: MI = mapped_column(Integer)
    match_number: MI = mapped_column(Integer)

    time: MI = mapped_column(Integer)  # Enforces ordering
    predicted_time: MOI = mapped_column(Integer, nullable=True)  # For display

    status: Mapped[MatchStatus] = mapped_column(
        Enum(MatchStatus, values_callable=values_callable)
    )
    video: MOS = mapped_column(String(20), nullable=True)

    red_1: MI = mapped_column(Integer, index=True)
    red_2: MI = mapped_column(Integer, index=True)
    red_3: MOI = mapped_column(Integer, index=True, nullable=True)
    red_dq: MS = mapped_column(String(20))
    red_surrogate: MS = mapped_column(String(20))

    blue_1: MI = mapped_column(Integer, index=True)
    blue_2: MI = mapped_column(Integer, index=True)
    blue_3: MOI = mapped_column(Integer, index=True, nullable=True)
    blue_dq: MS = mapped_column(String(20))
    blue_surrogate: MS = mapped_column(String(20))

    """OUTCOME"""
    winner: Mapped[Optional[MatchWinner]] = mapped_column(
        Enum(MatchWinner, values_callable=values_callable), nullable=True, default=None
    )

    red_score: MOI = mapped_column(Integer, nullable=True, default=None)
    red_no_foul: MOI = mapped_column(Integer, nullable=True, default=None)
    red_foul: MOI = mapped_column(Integer, nullable=True, default=None)
    red_auto: MOI = mapped_column(Integer, nullable=True, default=None)
    red_teleop: MOI = mapped_column(Integer, nullable=True, default=None)
    red_endgame: MOI = mapped_column(Integer, nullable=True, default=None)
    red_rp_1: MOB = mapped_column(Boolean, nullable=True, default=None)
    red_rp_2: MOB = mapped_column(Boolean, nullable=True, default=None)
    red_rp_3: MOB = mapped_column(Boolean, nullable=True, default=None)
    red_tiebreaker: MOI = mapped_column(Integer, nullable=True, default=None)
    red_comp_1: MOF = mapped_column(Float, nullable=True, default=None)
    red_comp_2: MOF = mapped_column(Float, nullable=True, default=None)
    red_comp_3: MOF = mapped_column(Float, nullable=True, default=None)
    red_comp_4: MOF = mapped_column(Float, nullable=True, default=None)
    red_comp_5: MOF = mapped_column(Float, nullable=True, default=None)
    red_comp_6: MOF = mapped_column(Float, nullable=True, default=None)
    red_comp_7: MOF = mapped_column(Float, nullable=True, default=None)
    red_comp_8: MOF = mapped_column(Float, nullable=True, default=None)
    red_comp_9: MOF = mapped_column(Float, nullable=True, default=None)
    red_comp_10: MOF = mapped_column(Float, nullable=True, default=None)
    red_comp_11: MOF = mapped_column(Float, nullable=True, default=None)
    red_comp_12: MOF = mapped_column(Float, nullable=True, default=None)
    red_comp_13: MOF = mapped_column(Float, nullable=True, default=None)
    red_comp_14: MOF = mapped_column(Float, nullable=True, default=None)
    red_comp_15: MOF = mapped_column(Float, nullable=True, default=None)
    red_comp_16: MOF = mapped_column(Float, nullable=True, default=None)
    red_comp_17: MOF = mapped_column(Float, nullable=True, default=None)
    red_comp_18: MOF = mapped_column(Float, nullable=True, default=None)

    blue_score: MOI = mapped_column(Integer, nullable=True, default=None)
    blue_no_foul: MOI = mapped_column(Integer, nullable=True, default=None)
    blue_foul: MOI = mapped_column(Integer, nullable=True, default=None)
    blue_auto: MOI = mapped_column(Integer, nullable=True, default=None)
    blue_teleop: MOI = mapped_column(Integer, nullable=True, default=None)
    blue_endgame: MOI = mapped_column(Integer, nullable=True, default=None)
    blue_rp_1: MOB = mapped_column(Boolean, nullable=True, default=None)
    blue_rp_2: MOB = mapped_column(Boolean, nullable=True, default=None)
    blue_rp_3: MOB = mapped_column(Boolean, nullable=True, default=None)
    blue_tiebreaker: MOI = mapped_column(Integer, nullable=True, default=None)
    blue_comp_1: MOF = mapped_column(Float, nullable=True, default=None)
    blue_comp_2: MOF = mapped_column(Float, nullable=True, default=None)
    blue_comp_3: MOF = mapped_column(Float, nullable=True, default=None)
    blue_comp_4: MOF = mapped_column(Float, nullable=True, default=None)
    blue_comp_5: MOF = mapped_column(Float, nullable=True, default=None)
    blue_comp_6: MOF = mapped_column(Float, nullable=True, default=None)
    blue_comp_7: MOF = mapped_column(Float, nullable=True, default=None)
    blue_comp_8: MOF = mapped_column(Float, nullable=True, default=None)
    blue_comp_9: MOF = mapped_column(Float, nullable=True, default=None)
    blue_comp_10: MOF = mapped_column(Float, nullable=True, default=None)
    blue_comp_11: MOF = mapped_column(Float, nullable=True, default=None)
    blue_comp_12: MOF = mapped_column(Float, nullable=True, default=None)
    blue_comp_13: MOF = mapped_column(Float, nullable=True, default=None)
    blue_comp_14: MOF = mapped_column(Float, nullable=True, default=None)
    blue_comp_15: MOF = mapped_column(Float, nullable=True, default=None)
    blue_comp_16: MOF = mapped_column(Float, nullable=True, default=None)
    blue_comp_17: MOF = mapped_column(Float, nullable=True, default=None)
    blue_comp_18: MOF = mapped_column(Float, nullable=True, default=None)

    """EPA"""
    epa_winner: Mapped[Optional[MatchWinner]] = mapped_column(
        Enum(MatchWinner, values_callable=values_callable), nullable=True, default=None
    )
    epa_win_prob: MOF = mapped_column(Float, nullable=True, default=None)
    epa_red_score_pred: MOF = mapped_column(Float, nullable=True, default=None)
    epa_blue_score_pred: MOF = mapped_column(Float, nullable=True, default=None)
    epa_red_rp_1_pred: MOF = mapped_column(Float, nullable=True, default=None)
    epa_red_rp_2_pred: MOF = mapped_column(Float, nullable=True, default=None)
    epa_red_rp_3_pred: MOF = mapped_column(Float, nullable=True, default=None)
    epa_blue_rp_1_pred: MOF = mapped_column(Float, nullable=True, default=None)
    epa_blue_rp_2_pred: MOF = mapped_column(Float, nullable=True, default=None)
    epa_blue_rp_3_pred: MOF = mapped_column(Float, nullable=True, default=None)


_Match = generate_attr_class("Match", MatchORM)


class Match(_Match, Model):
    def sort(self: "Match") -> int:
        return self.time or 0

    def pk(self: "Match") -> str:
        return self.key

    def __hash__(self: "Match") -> int:
        return hash(self.pk())

    def __str__(self: "Match") -> str:
        # Only refresh DB if these change (during 1 min partial update)
        return "_".join(
            [
                self.key,
                self.status,
                str(self.red_score),
                str(self.blue_score),
                str(self.red_teleop),
                str(self.blue_teleop),
                str(self.epa_red_score_pred),
                str(self.epa_blue_score_pred),
                str(self.predicted_time),
            ]
        )

    """HELPER FUNCTIONS"""

    def get_red(self: "Match") -> List[int]:
        return [x for x in [self.red_1, self.red_2, self.red_3] if x is not None]

    def get_blue(self: "Match") -> List[int]:
        return [x for x in [self.blue_1, self.blue_2, self.blue_3] if x is not None]

    def get_red_surrogates(self: "Match") -> List[int]:
        return [int(x) for x in self.red_surrogate.split(",") if x != ""]

    def get_blue_surrogates(self: "Match") -> List[int]:
        return [int(x) for x in self.blue_surrogate.split(",") if x != ""]

    def get_red_dqs(self: "Match") -> List[int]:
        return [int(x) for x in self.red_dq.split(",") if x != ""]

    def get_blue_dqs(self: "Match") -> List[int]:
        return [int(x) for x in self.blue_dq.split(",") if x != ""]

    def get_teams(self: "Match") -> List[List[int]]:
        return [self.get_red(), self.get_blue()]

    def get_winner(self: "Match") -> Optional[MatchWinner]:
        # For calculating win prediction metrics
        if self.winner is not None:
            return self.winner

        if self.red_score is None or self.blue_score is None:
            return None

        if self.red_score > self.blue_score:
            return MatchWinner.RED
        elif self.blue_score > self.red_score:
            return MatchWinner.BLUE
        else:
            return MatchWinner.TIE

    def get_breakdown(self: "Match", alliance: str) -> Any:
        if self.year < 2016:
            return np.array([getattr(self, f"{alliance}_score") or 0], dtype=np.float32)
        return np.array(
            [
                getattr(self, f"{alliance}_no_foul") or 0,
                getattr(self, f"{alliance}_auto") or 0,
                getattr(self, f"{alliance}_teleop") or 0,
                getattr(self, f"{alliance}_endgame") or 0,
                int(getattr(self, f"{alliance}_rp_1") or False),
                int(getattr(self, f"{alliance}_rp_2") or False),
                int(getattr(self, f"{alliance}_rp_3") or False),
                getattr(self, f"{alliance}_tiebreaker") or 0,
                getattr(self, f"{alliance}_comp_1") or 0,
                getattr(self, f"{alliance}_comp_2") or 0,
                getattr(self, f"{alliance}_comp_3") or 0,
                getattr(self, f"{alliance}_comp_4") or 0,
                getattr(self, f"{alliance}_comp_5") or 0,
                getattr(self, f"{alliance}_comp_6") or 0,
                getattr(self, f"{alliance}_comp_7") or 0,
                getattr(self, f"{alliance}_comp_8") or 0,
                getattr(self, f"{alliance}_comp_9") or 0,
                getattr(self, f"{alliance}_comp_10") or 0,
                getattr(self, f"{alliance}_comp_11") or 0,
                getattr(self, f"{alliance}_comp_12") or 0,
                getattr(self, f"{alliance}_comp_13") or 0,
                getattr(self, f"{alliance}_comp_14") or 0,
                getattr(self, f"{alliance}_comp_15") or 0,
                getattr(self, f"{alliance}_comp_16") or 0,
                getattr(self, f"{alliance}_comp_17") or 0,
                getattr(self, f"{alliance}_comp_18") or 0,
            ],
            dtype=np.float32,
        )

    def get_breakdowns(self: "Match") -> Tuple[Any, Any]:
        return self.get_breakdown("red"), self.get_breakdown("blue")

    def to_dict(self: "Match") -> Dict[str, Any]:
        clean: Dict[str, Any] = {
            "key": self.key,
            "year": self.year,
            "event": self.event,
            "week": self.week,
            "elim": self.elim,
            "comp_level": self.comp_level,
            "set_number": self.set_number,
            "match_number": self.match_number,
            "match_name": get_match_name(self.key),
            "time": self.time,
            "predicted_time": self.predicted_time,
            "status": self.status,
            "video": self.video,
            "alliances": {
                "red": {
                    "team_keys": self.get_red(),
                    "surrogate_team_keys": self.get_red_surrogates(),
                    "dq_team_keys": self.get_red_dqs(),
                },
                "blue": {
                    "team_keys": self.get_blue(),
                    "surrogate_team_keys": self.get_blue_surrogates(),
                    "dq_team_keys": self.get_blue_dqs(),
                },
            },
            "pred": {
                "winner": self.epa_winner,
                "red_win_prob": self.epa_win_prob,
                "red_score": self.epa_red_score_pred,
                "blue_score": self.epa_blue_score_pred,
            },
            "result": {
                "winner": self.winner,
                "red_score": self.red_score,
                "blue_score": self.blue_score,
                "red_no_foul": self.red_no_foul,
                "blue_no_foul": self.blue_no_foul,
            },
        }

        if self.year >= 2016:
            rps = ["rp_1", "rp_2"]
            if self.year == 2025:
                rps += ["rp_3"]

            for rp in rps:
                rp_name = key_to_name[self.year][rp]
                clean["pred"][f"red_{rp_name}"] = getattr(self, f"epa_red_{rp}_pred")
                clean["pred"][f"blue_{rp_name}"] = getattr(self, f"epa_blue_{rp}_pred")
            for rp in rps:
                clean["pred"][f"red_{rp}"] = getattr(self, f"epa_red_{rp}_pred")
                clean["pred"][f"blue_{rp}"] = getattr(self, f"epa_blue_{rp}_pred")
            pairs = list(key_to_name[self.year].items())
            pairs += [(rp, rp) for rp in rps]
            for key, name in pairs:
                clean["result"][f"red_{name}"] = getattr(self, f"red_{key}")
                clean["result"][f"blue_{name}"] = getattr(self, f"blue_{key}")

        return clean
