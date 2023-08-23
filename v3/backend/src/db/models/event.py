from typing import Any, Dict

import attr
from sqlalchemy import Boolean, Float, Integer, String
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql.schema import ForeignKeyConstraint, PrimaryKeyConstraint

from src.db.main import Base
from src.db.models.main import Model, ModelORM, generate_attr_class
from src.db.models.types import MB, MI, MOF, MOI, MOS, MS


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

    # 0 is regional, 1 is district, 2 is district champ,
    # 3 is worlds division, 4 is einsteins/FOC
    # 99 is offseason, 100 is preseason
    type: MI = mapped_column(Integer)
    week: MI = mapped_column(Integer)
    offseason: MB = mapped_column(Boolean)

    # Link to livestream, full link (unlike Match) to handle Twitch/YT
    video: MOS = mapped_column(String(50), nullable=True)

    # Choices are 'Upcoming', 'Ongoing', 'Completed'
    status: MS = mapped_column(String(10))

    # -1 = upcoming event, 0 = schedule release, x = match x concluded
    current_match: MOI = mapped_column(Integer, nullable=True, default=None)
    qual_matches: MOI = mapped_column(Integer, nullable=True, default=None)

    """EPA"""
    epa_max: MOF = mapped_column(Float, nullable=True, default=None)
    epa_top8: MOF = mapped_column(Float, nullable=True, default=None)
    epa_top24: MOF = mapped_column(Float, nullable=True, default=None)
    epa_mean: MOF = mapped_column(Float, nullable=True, default=None)
    epa_sd: MOF = mapped_column(Float, nullable=True, default=None)

    """STATS"""
    epa_acc: MOF = mapped_column(Float, nullable=True, default=None)
    epa_mse: MOF = mapped_column(Float, nullable=True, default=None)
    rp_1_acc: MOF = mapped_column(Float, nullable=True, default=None)
    rp_1_mse: MOF = mapped_column(Float, nullable=True, default=None)
    rp_2_acc: MOF = mapped_column(Float, nullable=True, default=None)
    rp_2_mse: MOF = mapped_column(Float, nullable=True, default=None)


_Event = generate_attr_class("Event", EventORM)


class Event(_Event, Model):
    def to_dict(self: "Event") -> Dict[str, Any]:
        return attr.asdict(
            self, filter=attr.filters.exclude(attr.fields(Event).current_match)
        )

    def pk(self: "Event") -> str:
        return self.key

    def __str__(self: "Event") -> str:
        # Only refresh DB if these change (during 1 min partial update)
        return f"{self.key}_{self.status}_{self.current_match}_{self.qual_matches}"
