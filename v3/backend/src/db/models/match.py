from typing import Any, Dict, List, Optional

from sqlalchemy import Boolean, Enum, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.schema import ForeignKeyConstraint, PrimaryKeyConstraint

from src.breakdown import key_to_name
from src.db.main import Base
from src.db.models.main import Model, ModelORM, generate_attr_class
from src.db.models.types import MB, MI, MOB, MOF, MOI, MOS, MS, values_callable
from src.types.enums import CompLevel, MatchStatus, MatchWinner


class MatchORM(Base, ModelORM):
    """DECLARATION"""

    __tablename__ = "matches"
    key: MS = mapped_column(String(20), index=True)
    year: MI = mapped_column(Integer, index=True)
    event: MS = mapped_column(String(12), index=True)

    PrimaryKeyConstraint(key)
    ForeignKeyConstraint(["year"], ["years.year"])
    ForeignKeyConstraint(["event"], ["events.key"])

    """GENERAL"""
    offseason: MB = mapped_column(Boolean, index=True)
    week: MI = mapped_column(Integer, index=True)
    elim: MB = mapped_column(Boolean, index=True)

    comp_level: Mapped[CompLevel] = mapped_column(
        Enum(CompLevel, values_callable=values_callable)
    )
    set_number: MI = mapped_column(Integer)
    match_number: MI = mapped_column(Integer)

    time: MI = mapped_column(Integer)  # Enforces ordering
    predicted_time: MOI = mapped_column(Integer, nullable=True)  # For display

    status: Mapped[MatchStatus] = mapped_column(
        Enum(MatchStatus, values_callable=values_callable), index=True
    )
    video: MOS = mapped_column(String(20), nullable=True)

    red_1: MS = mapped_column(String(6), index=True)
    red_2: MS = mapped_column(String(6), index=True)
    red_3: MOS = mapped_column(String(6), index=True, nullable=True)
    red_dq: MS = mapped_column(String(20))
    red_surrogate: MS = mapped_column(String(20))

    blue_1: MS = mapped_column(String(6), index=True)
    blue_2: MS = mapped_column(String(6), index=True)
    blue_3: MOS = mapped_column(String(6), index=True, nullable=True)
    blue_dq: MS = mapped_column(String(20))
    blue_surrogate: MS = mapped_column(String(20))

    """OUTCOME"""
    winner: Mapped[Optional[MatchWinner]] = mapped_column(
        Enum(MatchWinner, values_callable=values_callable), nullable=True, default=None
    )

    red_score: MOI = mapped_column(Integer, nullable=True, default=None)
    red_no_foul: MOI = mapped_column(Integer, nullable=True, default=None)
    red_rp_1: MOB = mapped_column(Boolean, nullable=True, default=None)
    red_rp_2: MOB = mapped_column(Boolean, nullable=True, default=None)

    blue_score: MOI = mapped_column(Integer, nullable=True, default=None)
    blue_no_foul: MOI = mapped_column(Integer, nullable=True, default=None)
    blue_rp_1: MOB = mapped_column(Boolean, nullable=True, default=None)
    blue_rp_2: MOB = mapped_column(Boolean, nullable=True, default=None)

    """EPA"""
    epa_winner: Mapped[Optional[MatchWinner]] = mapped_column(
        Enum(MatchWinner, values_callable=values_callable), nullable=True, default=None
    )
    epa_win_prob: MOF = mapped_column(Float, nullable=True, default=None)
    epa_red_score_pred: MOF = mapped_column(Float, nullable=True, default=None)
    epa_blue_score_pred: MOF = mapped_column(Float, nullable=True, default=None)
    epa_red_rp_1_pred: MOF = mapped_column(Float, nullable=True, default=None)
    epa_red_rp_2_pred: MOF = mapped_column(Float, nullable=True, default=None)
    epa_blue_rp_1_pred: MOF = mapped_column(Float, nullable=True, default=None)
    epa_blue_rp_2_pred: MOF = mapped_column(Float, nullable=True, default=None)


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
                str(self.epa_red_score_pred),
                str(self.epa_blue_score_pred),
                str(self.predicted_time),
            ]
        )

    """HELPER FUNCTIONS"""

    def get_red(self: "Match") -> List[str]:
        return [x for x in [self.red_1, self.red_2, self.red_3] if x is not None]

    def get_blue(self: "Match") -> List[str]:
        return [x for x in [self.blue_1, self.blue_2, self.blue_3] if x is not None]

    def get_red_surrogates(self: "Match") -> List[str]:
        return [x for x in self.red_surrogate.split(",") if x != ""]

    def get_blue_surrogates(self: "Match") -> List[str]:
        return [x for x in self.blue_surrogate.split(",") if x != ""]

    def get_red_dqs(self: "Match") -> List[str]:
        return [x for x in self.red_dq.split(",") if x != ""]

    def get_blue_dqs(self: "Match") -> List[str]:
        return [x for x in self.blue_dq.split(",") if x != ""]

    def get_teams(self: "Match") -> List[List[str]]:
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

    def to_dict(self: "Match") -> Dict[str, Any]:
        clean: Dict[str, Any] = {
            "key": self.key,
            "year": self.year,
            "event": self.event,
            "offseason": self.offseason,
            "week": self.week,
            "elim": self.elim,
            "comp_level": self.comp_level,
            "set_number": self.set_number,
            "match_number": self.match_number,
            "time": self.time,
            "predicted_time": self.predicted_time,
            "status": self.status,
            "video": self.video,
            "teams": {
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
            rp_1_name = key_to_name[self.year]["rp_1"]
            rp_2_name = key_to_name[self.year]["rp_2"]

            clean["pred"][f"red_{rp_1_name}"] = self.epa_red_rp_1_pred
            clean["pred"][f"red_{rp_2_name}"] = self.epa_red_rp_2_pred
            clean["pred"][f"blue_{rp_1_name}"] = self.epa_blue_rp_1_pred
            clean["pred"][f"blue_{rp_2_name}"] = self.epa_blue_rp_2_pred

            clean["result"][f"red_{rp_1_name}"] = self.red_rp_1
            clean["result"][f"red_{rp_2_name}"] = self.red_rp_2
            clean["result"][f"blue_{rp_1_name}"] = self.blue_rp_1
            clean["result"][f"blue_{rp_2_name}"] = self.blue_rp_2

        return clean
