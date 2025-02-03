from typing import Any, Dict, Tuple

from sqlalchemy import Boolean, Enum, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.schema import ForeignKeyConstraint, PrimaryKeyConstraint

from src.breakdown import key_to_name
from src.db.main import Base
from src.db.models.main import Model, ModelORM, generate_attr_class
from src.db.models.types import MB, MF, MI, MOB, MOF, MOI, MOS, MS, values_callable
from src.models.epa.math import get_skew_normal_95_conf_interval
from src.types.enums import EventStatus, EventType


class TeamEventORM(Base, ModelORM):
    """DECLARATIONS"""

    __tablename__ = "team_events"
    id: MOI = mapped_column(Integer, nullable=True)  # placeholder for backend API
    team: MI = mapped_column(Integer, index=True)
    year: MI = mapped_column(Integer, index=True)
    event: MS = mapped_column(String(12), index=True)

    PrimaryKeyConstraint(team, event)
    ForeignKeyConstraint(["team"], ["teams.team"])
    ForeignKeyConstraint(["year"], ["years.year"])
    ForeignKeyConstraint(["team", "year"], ["team_years.team", "team_years.year"])
    ForeignKeyConstraint(["event"], ["events.key"])

    """GENERAL"""
    time: MI = mapped_column(Integer)

    """API COMPLETENESS"""
    team_name: MS = mapped_column(String(100))
    event_name: MS = mapped_column(String(100))
    country: MOS = mapped_column(String(30), nullable=True)
    state: MOS = mapped_column(String(10), nullable=True)
    district: MOS = mapped_column(String(10), nullable=True)
    type: Mapped[EventType] = mapped_column(
        Enum(EventType, values_callable=values_callable)
    )
    week: MI = mapped_column(Integer)

    status: Mapped[EventStatus] = mapped_column(
        Enum(EventStatus, values_callable=values_callable)
    )
    first_event: MB = mapped_column(Boolean)

    """STATS"""
    wins: MI = mapped_column(Integer, default=0)
    losses: MI = mapped_column(Integer, default=0)
    ties: MI = mapped_column(Integer, default=0)
    count: MI = mapped_column(Integer, default=0)
    winrate: MF = mapped_column(Float, default=0)
    qual_wins: MI = mapped_column(Integer, default=0)
    qual_losses: MI = mapped_column(Integer, default=0)
    qual_ties: MI = mapped_column(Integer, default=0)
    qual_count: MI = mapped_column(Integer, default=0)
    qual_winrate: MF = mapped_column(Float, default=0)
    rps: MI = mapped_column(Integer, default=0)
    rps_per_match: MF = mapped_column(Float, default=0)
    rank: MOI = mapped_column(Integer, nullable=True, default=None)
    num_teams: MOI = mapped_column(Integer, nullable=True, default=None)
    elim_alliance: MOS = mapped_column(String(30), nullable=True, default=None)
    is_captain: MOB = mapped_column(Boolean, nullable=True, default=None)
    district_points: MOI = mapped_column(Integer, nullable=True, default=None)

    """EPA"""
    epa_start: MF = mapped_column(Float, default=0)
    epa_pre_elim: MF = mapped_column(Float, default=0)
    epa_mean: MF = mapped_column(Float, default=0)
    epa_max: MF = mapped_column(Float, default=0)

    epa: MF = mapped_column(Float, default=0)
    epa_sd: MF = mapped_column(Float, default=0)
    epa_skew: MF = mapped_column(Float, default=0)
    epa_n: MF = mapped_column(Float, default=0)
    auto_epa: MOF = mapped_column(Float, default=None)
    teleop_epa: MOF = mapped_column(Float, default=None)
    endgame_epa: MOF = mapped_column(Float, default=None)
    rp_1_epa: MOF = mapped_column(Float, default=None)
    rp_2_epa: MOF = mapped_column(Float, default=None)
    rp_3_epa: MOF = mapped_column(Float, default=None)
    tiebreaker_epa: MOF = mapped_column(Float, default=None)
    comp_1_epa: MOF = mapped_column(Float, default=None)
    comp_2_epa: MOF = mapped_column(Float, default=None)
    comp_3_epa: MOF = mapped_column(Float, default=None)
    comp_4_epa: MOF = mapped_column(Float, default=None)
    comp_5_epa: MOF = mapped_column(Float, default=None)
    comp_6_epa: MOF = mapped_column(Float, default=None)
    comp_7_epa: MOF = mapped_column(Float, default=None)
    comp_8_epa: MOF = mapped_column(Float, default=None)
    comp_9_epa: MOF = mapped_column(Float, default=None)
    comp_10_epa: MOF = mapped_column(Float, default=None)
    comp_11_epa: MOF = mapped_column(Float, default=None)
    comp_12_epa: MOF = mapped_column(Float, default=None)
    comp_13_epa: MOF = mapped_column(Float, default=None)
    comp_14_epa: MOF = mapped_column(Float, default=None)
    comp_15_epa: MOF = mapped_column(Float, default=None)
    comp_16_epa: MOF = mapped_column(Float, default=None)
    comp_17_epa: MOF = mapped_column(Float, default=None)
    comp_18_epa: MOF = mapped_column(Float, default=None)

    unitless_epa: MF = mapped_column(Float, default=0)
    norm_epa: MOF = mapped_column(Float, default=0)


_TeamEvent = generate_attr_class("TeamEvent", TeamEventORM)


class TeamEvent(_TeamEvent, Model):
    def sort(self: "TeamEvent") -> Tuple[int, int]:
        return (self.team, self.time)

    def pk(self: "TeamEvent") -> str:
        return f"{self.team}_{self.event}"

    def __hash__(self: "TeamEvent") -> int:
        return hash(self.pk())

    def __str__(self: "TeamEvent") -> str:
        # Only refresh DB if these change (during 1 min partial update)
        return "_".join(
            [
                str(self.team),
                self.event,
                str(self.status),
                str(self.count),
                str(self.epa),
                str(self.rank),
            ]
        )

    def to_dict(self: "TeamEvent") -> Dict[str, Any]:
        lower, upper = get_skew_normal_95_conf_interval(
            0, 1, self.epa_skew, self.epa_n, 2
        )

        elim_wins = self.wins - self.qual_wins
        elim_losses = self.losses - self.qual_losses
        elim_ties = self.ties - self.qual_ties
        elim_count = self.count - self.qual_count
        elim_winrate = 0
        if elim_count > 0:
            elim_winrate = (elim_wins + elim_ties / 2) / elim_count

        clean: Dict[str, Any] = {
            "team": self.team,
            "year": self.year,
            "event": self.event,
            "time": self.time,
            "team_name": self.team_name,
            "event_name": self.event_name,
            "country": self.country,
            "state": self.state,
            "district": self.district,
            "type": self.type,
            "week": self.week,
            "status": self.status,
            "first_event": self.first_event,
            "epa": {
                "total_points": {
                    "mean": self.epa,
                    "sd": self.epa_sd,
                },
                "unitless": self.unitless_epa,
                "norm": self.norm_epa,
                "conf": [lower, upper],
                "breakdown": {},
                "stats": {
                    "start": self.epa_start,
                    "pre_elim": self.epa_pre_elim,
                    "mean": self.epa_mean,
                    "max": self.epa_max,
                },
            },
            "record": {
                "qual": {
                    "wins": self.qual_wins,
                    "losses": self.qual_losses,
                    "ties": self.qual_ties,
                    "count": self.qual_count,
                    "winrate": self.qual_winrate,
                    "rps": self.rps,
                    "rps_per_match": self.rps_per_match,
                    "rank": self.rank,
                    "num_teams": self.num_teams,
                },
                "elim": {
                    "wins": elim_wins,
                    "losses": elim_losses,
                    "ties": elim_ties,
                    "count": elim_count,
                    "winrate": elim_winrate,
                    "alliance": self.elim_alliance,
                    "is_captain": self.is_captain,
                },
                "total": {
                    "wins": self.wins,
                    "losses": self.losses,
                    "ties": self.ties,
                    "count": self.count,
                    "winrate": self.winrate,
                },
            },
            "district_points": self.district_points,
        }

        clean["epa"]["breakdown"]["total_points"] = self.epa
        if self.year >= 2016:
            pairs = list(key_to_name[self.year].items())
            pairs += [("rp_1", "rp_1"), ("rp_2", "rp_2")]
            if self.year >= 2025:
                pairs += [("rp_3", "rp_3")]
            for key, name in pairs:
                clean["epa"]["breakdown"][name] = getattr(self, f"{key}_epa")

        return clean
