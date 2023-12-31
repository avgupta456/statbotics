from typing import Any, Dict

import attr
from sqlalchemy import Boolean, Enum, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.schema import ForeignKeyConstraint, PrimaryKeyConstraint

from src.db.main import Base
from src.db.models.main import Model, ModelORM, generate_attr_class
from src.db.models.types import MB, MI, MOF, MOI, MOS, MS, values_callable
from src.types.enums import EventStatus, EventType


class EventORM(Base, ModelORM):
    """DECLARATION"""

    __tablename__ = "events"
    key: MS = mapped_column(String(20), index=True)
    year: MI = mapped_column(Integer, index=True)

    PrimaryKeyConstraint(key)
    ForeignKeyConstraint(["year"], ["years.year"])

    """GENERAL"""
    name: MS = mapped_column(String(100))
    time: MI = mapped_column(Integer)
    country: MOS = mapped_column(String(30), nullable=True)
    district: MOS = mapped_column(String(10), nullable=True)
    state: MOS = mapped_column(String(10), nullable=True)
    start_date: MS = mapped_column(String(10))
    end_date: MS = mapped_column(String(10))

    type: Mapped[EventType] = mapped_column(
        Enum(EventType, values_callable=values_callable)
    )
    week: MI = mapped_column(Integer)
    offseason: MB = mapped_column(Boolean)

    # Link to livestream, full link (unlike Match) to handle Twitch/YT
    video: MOS = mapped_column(String(50), nullable=True)

    status: Mapped[EventStatus] = mapped_column(
        Enum(EventStatus, values_callable=values_callable)
    )

    # -1 = upcoming event, 0 = schedule release, x = match x concluded
    current_match: MOI = mapped_column(Integer, nullable=True, default=None)
    qual_matches: MOI = mapped_column(Integer, nullable=True, default=None)

    """EPA"""
    epa_max: MOF = mapped_column(Float, nullable=True, default=None)
    epa_top_8: MOF = mapped_column(Float, nullable=True, default=None)
    epa_top_24: MOF = mapped_column(Float, nullable=True, default=None)
    epa_mean: MOF = mapped_column(Float, nullable=True, default=None)
    epa_sd: MOF = mapped_column(Float, nullable=True, default=None)

    """STATS"""
    count: MI = mapped_column(Integer, default=0)
    epa_conf: MOF = mapped_column(Float, nullable=True, default=None)
    epa_acc: MOF = mapped_column(Float, nullable=True, default=None)
    epa_mse: MOF = mapped_column(Float, nullable=True, default=None)

    epa_score_rmse: MOF = mapped_column(Float, nullable=True, default=None)
    epa_score_mae: MOF = mapped_column(Float, nullable=True, default=None)
    epa_score_error: MOF = mapped_column(Float, nullable=True, default=None)

    rp_count: MI = mapped_column(Integer, default=0)
    epa_rp_1_error: MOF = mapped_column(Float, nullable=True, default=None)
    epa_rp_1_acc: MOF = mapped_column(Float, nullable=True, default=None)
    epa_rp_1_ll: MOF = mapped_column(Float, nullable=True, default=None)
    epa_rp_1_f1: MOF = mapped_column(Float, nullable=True, default=None)

    epa_rp_2_error: MOF = mapped_column(Float, nullable=True, default=None)
    epa_rp_2_acc: MOF = mapped_column(Float, nullable=True, default=None)
    epa_rp_2_ll: MOF = mapped_column(Float, nullable=True, default=None)
    epa_rp_2_f1: MOF = mapped_column(Float, nullable=True, default=None)


_Event = generate_attr_class("Event", EventORM)


class Event(_Event, Model):
    def to_dict(self: "Event") -> Dict[str, Any]:
        return attr.asdict(
            self, filter=attr.filters.exclude(attr.fields(Event).current_match)
        )

    def pk(self: "Event") -> str:
        return self.key

    def __hash__(self: "Event") -> int:
        return hash(self.pk())

    def __str__(self: "Event") -> str:
        # Only refresh DB if these change (during 1 min partial update)
        return "_".join(
            [self.key, self.status, str(self.current_match), str(self.qual_matches)]
        )
