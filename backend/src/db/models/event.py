from typing import Any, Dict

from sqlalchemy import Enum, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.schema import ForeignKeyConstraint, PrimaryKeyConstraint

from src.breakdown import key_to_name
from src.db.main import Base
from src.db.models.main import Model, ModelORM, generate_attr_class
from src.db.models.types import MI, MOF, MOI, MOS, MS, values_callable
from src.types.enums import EventStatus, EventType


class EventORM(Base, ModelORM):
    """DECLARATION"""

    __tablename__ = "events"
    key: MS = mapped_column(String(20))
    year: MI = mapped_column(Integer, index=True)

    PrimaryKeyConstraint(key)
    ForeignKeyConstraint(["year"], ["years.year"])

    """GENERAL"""
    name: MS = mapped_column(String(100))
    time: MI = mapped_column(Integer)
    country: MOS = mapped_column(String(30), nullable=True)
    state: MOS = mapped_column(String(10), nullable=True)
    district: MOS = mapped_column(String(10), nullable=True)
    start_date: MS = mapped_column(String(10))
    end_date: MS = mapped_column(String(10))

    type: Mapped[EventType] = mapped_column(
        Enum(EventType, values_callable=values_callable)
    )
    week: MI = mapped_column(Integer)

    # Link to livestream, full link (unlike Match) to handle Twitch/YT
    video: MOS = mapped_column(String(50), nullable=True)

    status: Mapped[EventStatus] = mapped_column(
        Enum(EventStatus, values_callable=values_callable)
    )

    num_teams: MI = mapped_column(Integer, nullable=False, default=0)

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
    epa_score_error: MOF = mapped_column(Float, nullable=True, default=None)

    rp_count: MI = mapped_column(Integer, default=0)
    epa_rp_1_error: MOF = mapped_column(Float, nullable=True, default=None)
    epa_rp_1_acc: MOF = mapped_column(Float, nullable=True, default=None)

    epa_rp_2_error: MOF = mapped_column(Float, nullable=True, default=None)
    epa_rp_2_acc: MOF = mapped_column(Float, nullable=True, default=None)

    epa_rp_3_error: MOF = mapped_column(Float, nullable=True, default=None)
    epa_rp_3_acc: MOF = mapped_column(Float, nullable=True, default=None)


_Event = generate_attr_class("Event", EventORM)


class Event(_Event, Model):
    def pk(self: "Event") -> str:
        return self.key

    def __hash__(self: "Event") -> int:
        return hash(self.pk())

    def __str__(self: "Event") -> str:
        # Only refresh DB if these change (during 1 min partial update)
        return "_".join(
            [
                self.key,
                self.status,
                str(self.num_teams),
                str(self.current_match),
                str(self.qual_matches),
            ]
        )

    def get_event_status_str(self: "Event") -> str:
        if self.status != "Ongoing":
            return self.status

        if self.qual_matches == 0:
            return "Scheduled Unreleased"
        elif self.current_match == 0:
            return "Schedule Released"
        elif (self.current_match or -1) < (self.qual_matches or -1):
            return "Qual " + str(self.current_match)
        elif self.current_match == self.qual_matches:
            return "Quals Over"
        else:
            return "Elims Ongoing"

    def to_dict(self: "Event") -> Dict[str, Any]:
        clean: Dict[str, Any] = {
            "key": self.key,
            "year": self.year,
            "name": self.name,
            "time": self.time,
            "country": self.country,
            "state": self.state,
            "district": self.district,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "type": self.type,
            "week": self.week,
            "video": self.video,
            "status": self.status,
            "status_str": self.get_event_status_str(),
            "num_teams": self.num_teams,
            "current_match": self.current_match,
            "qual_matches": self.qual_matches,
            "epa": {
                "max": self.epa_max,
                "top_8": self.epa_top_8,
                "top_24": self.epa_top_24,
                "mean": self.epa_mean,
                "sd": self.epa_sd,
            },
            "metrics": {
                "win_prob": {
                    "count": self.count,
                    "conf": self.epa_conf,
                    "acc": self.epa_acc,
                    "mse": self.epa_mse,
                },
                "score_pred": {
                    "count": 2 * self.count,
                    "rmse": self.epa_score_rmse,
                    "error": self.epa_score_error,
                },
            },
        }

        if self.year >= 2016:
            clean["metrics"]["rp_pred"] = {
                "count": self.rp_count,
                key_to_name[self.year]["rp_1"]: {
                    "error": self.epa_rp_1_error,
                    "acc": self.epa_rp_1_acc,
                },
                key_to_name[self.year]["rp_2"]: {
                    "error": self.epa_rp_2_error,
                    "acc": self.epa_rp_2_acc,
                },
            }
            if self.year >= 2025:
                clean["metrics"]["rp_pred"][key_to_name[self.year]["rp_3"]] = (
                    {
                        "error": self.epa_rp_3_error,
                        "acc": self.epa_rp_3_acc,
                    },
                )

        return clean
