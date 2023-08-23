from typing import Any, Dict, List

from sqlalchemy import Boolean, Float, Integer, String
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql.schema import ForeignKeyConstraint, PrimaryKeyConstraint

from src.db.main import Base
from src.db.models.main import Model, ModelORM, generate_attr_class
from src.db.models.types import MB, MF, MI, MOF, MOI, MOS, MS


class MatchORM(Base, ModelORM):
    """DECLARATION"""

    __tablename__ = "matches"
    key: MS = mapped_column(String(20), index=True)
    year: MI = mapped_column(Integer, index=True)
    event: MS = mapped_column(String(20), index=True)

    PrimaryKeyConstraint(key)
    ForeignKeyConstraint(["year"], ["years.year"])
    ForeignKeyConstraint(["event"], ["events.key"])

    """GENERAL"""
    offseason: MB = mapped_column(Boolean, index=True)
    week: MI = mapped_column(Integer, index=True)
    playoff: MB = mapped_column(Boolean, index=True)

    comp_level: MS = mapped_column(String(10))
    set_number: MI = mapped_column(Integer)
    match_number: MI = mapped_column(Integer)

    time: MI = mapped_column(Integer)  # Enforces ordering
    predicted_time: MOI = mapped_column(Integer, nullable=True)  # For display

    # Choices are 'Upcoming', 'Completed'
    status: MS = mapped_column(String(10), index=True)
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

    """EPA"""
    red_epa_sum: MF = mapped_column(Float, default=0)

    blue_epa_sum: MF = mapped_column(Float, default=0)

    epa_winner: MS = mapped_column(String(4), default="draw")
    epa_win_prob: MF = mapped_column(Float, default=0.5)
    red_rp_1_prob: MOF = mapped_column(Float, nullable=True, default=None)
    red_rp_2_prob: MOF = mapped_column(Float, nullable=True, default=None)
    blue_rp_1_prob: MOF = mapped_column(Float, nullable=True, default=None)
    blue_rp_2_prob: MOF = mapped_column(Float, nullable=True, default=None)

    """OUTCOME"""
    winner: MOS = mapped_column(String(4), nullable=True, default=None)

    red_score: MOI = mapped_column(Integer, nullable=True, default=None)
    red_no_foul: MOI = mapped_column(Integer, nullable=True, default=None)
    red_rp_1: MOI = mapped_column(Integer, nullable=True, default=None)
    red_rp_2: MOI = mapped_column(Integer, nullable=True, default=None)
    red_tiebreaker: MOI = mapped_column(Integer, nullable=True, default=None)

    blue_score: MOI = mapped_column(Integer, nullable=True, default=None)
    blue_no_foul: MOI = mapped_column(Integer, nullable=True, default=None)
    blue_rp_1: MOI = mapped_column(Integer, nullable=True, default=None)
    blue_rp_2: MOI = mapped_column(Integer, nullable=True, default=None)
    blue_tiebreaker: MOI = mapped_column(Integer, nullable=True, default=None)


_Match = generate_attr_class("Match", MatchORM)


class Match(_Match, Model):
    def sort(self: "Match") -> int:
        return self.time or 0

    def pk(self: "Match") -> str:
        return self.key

    def __str__(self: "Match") -> str:
        # Only refresh DB if these change (during 1 min partial update)
        return f"{self.key}_{self.status}_{self.red_score}_{self.blue_score}_{self.red_epa_sum}_{self.blue_epa_sum}_{self.predicted_time}"

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


def create_match_obj(
    key: str,
    year: int,
    event: str,
    offseason: bool,
    week: int,
    playoff: bool,
    comp_level: str,
    set_number: int,
    match_number: int,
    time: int,
    predicted_time: int,
    status: str,
    video: str,
    red_1: str,
    red_2: str,
    red_3: str,
    red_dq: str,
    red_surrogate: str,
    blue_1: str,
    blue_2: str,
    blue_3: str,
    blue_dq: str,
    blue_surrogate: str,
    *args: List[Any],
    **kwawrgs: Dict[str, Any],
) -> Match:
    return Match(
        key=key,
        year=year,
        event=event,
        offseason=offseason,
        week=week,
        playoff=playoff,
        comp_level=comp_level,
        set_number=set_number,
        match_number=match_number,
        time=time,
        predicted_time=predicted_time,
        status=status,
        video=video,
        red_1=red_1,
        red_2=red_2,
        red_3=red_3,
        red_dq=red_dq,
        red_surrogate=red_surrogate,
        blue_1=blue_1,
        blue_2=blue_2,
        blue_3=blue_3,
        blue_dq=blue_dq,
        blue_surrogate=blue_surrogate,
        *args,
        **kwawrgs,
    )
