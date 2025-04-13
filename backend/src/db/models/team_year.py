from typing import Any, Dict, Tuple

from sqlalchemy import Boolean, Float, Integer, String
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql.schema import ForeignKeyConstraint, PrimaryKeyConstraint

from src.breakdown import key_to_name
from src.constants import CURR_YEAR
from src.db.main import Base
from src.db.models.main import Model, ModelORM, generate_attr_class
from src.db.models.types import MB, MF, MI, MOF, MOI, MOS, MS
from src.models.epa.math import get_skew_normal_95_conf_interval


class TeamYearORM(Base, ModelORM):
    """DECLARATION"""

    __tablename__ = "team_years"
    id: MOI = mapped_column(Integer, nullable=True)  # placeholder for backend API
    year: MI = mapped_column(Integer, index=True)
    team: MI = mapped_column(Integer, index=True)

    # force unique (team, year)
    PrimaryKeyConstraint(team, year)
    ForeignKeyConstraint(["year"], ["years.year"])
    ForeignKeyConstraint(["team"], ["teams.team"])

    """API COMPLETENESS"""
    name: MS = mapped_column(String(100))
    country: MOS = mapped_column(String(30))
    state: MOS = mapped_column(String(10))
    district: MOS = mapped_column(String(10))
    rookie_year: MOI = mapped_column(Integer, nullable=True)

    """PRE JOINS (FOR FRONTEND LOAD TIME)"""
    competing_this_week: MB = mapped_column(Boolean)
    next_event_key: MOS = mapped_column(String(10), nullable=True)
    next_event_name: MOS = mapped_column(String(100), nullable=True)
    next_event_week: MOI = mapped_column(Integer, nullable=True)

    """EPA"""
    epa_start: MF = mapped_column(Float, default=0)
    epa_pre_champs: MF = mapped_column(Float, default=0)
    epa_max: MF = mapped_column(Float, default=0)

    epa: MF = mapped_column(Float, index=True, default=0)
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

    """STATS"""
    wins: MI = mapped_column(Integer, default=0)  # competition season only
    losses: MI = mapped_column(Integer, default=0)
    ties: MI = mapped_column(Integer, default=0)
    count: MI = mapped_column(Integer, default=0)
    winrate: MF = mapped_column(Float, default=0)

    district_points: MOI = mapped_column(Integer, nullable=True, default=None)
    district_rank: MOI = mapped_column(Integer, nullable=True, default=None)

    total_epa_rank: MOI = mapped_column(Integer, nullable=True, default=None)
    total_epa_percentile: MOF = mapped_column(Float, nullable=True, default=None)
    total_team_count: MOI = mapped_column(Integer, nullable=True, default=None)

    country_epa_rank: MOI = mapped_column(Integer, nullable=True, default=None)
    country_epa_percentile: MOF = mapped_column(Float, nullable=True, default=None)
    country_team_count: MOI = mapped_column(Integer, nullable=True, default=None)

    state_epa_rank: MOI = mapped_column(Integer, nullable=True, default=None)
    state_epa_percentile: MOF = mapped_column(Float, nullable=True, default=None)
    state_team_count: MOI = mapped_column(Integer, nullable=True, default=None)

    district_epa_rank: MOI = mapped_column(Integer, nullable=True, default=None)
    district_epa_percentile: MOF = mapped_column(Float, nullable=True, default=None)
    district_team_count: MOI = mapped_column(Integer, nullable=True, default=None)


_TeamYear = generate_attr_class("TeamYear", TeamYearORM)


class TeamYear(_TeamYear, Model):
    def sort(self: "TeamYear") -> Tuple[int, int]:
        return (self.team, self.year)

    def pk(self: "TeamYear") -> str:
        return f"{self.team}_{self.year}"

    def __hash__(self: "TeamYear") -> int:
        return hash(self.pk())

    def __str__(self: "TeamYear") -> str:
        # Only refresh DB if these change (during 1 min partial update)
        return "_".join(
            [str(self.team), str(self.year), str(self.count), str(self.epa)]
        )

    def to_dict(self: "TeamYear") -> Dict[str, Any]:
        lower, upper = get_skew_normal_95_conf_interval(
            0, 1, self.epa_skew, self.epa_n, 2
        )

        clean: Dict[str, Any] = {
            "team": self.team,
            "year": self.year,
            "name": self.name,
            "country": self.country,
            "state": self.state,
            "district": self.district,
            "rookie_year": self.rookie_year,
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
                    "pre_champs": self.epa_pre_champs,
                    "max": self.epa_max,
                },
                "ranks": {
                    "total": {
                        "rank": self.total_epa_rank,
                        "percentile": self.total_epa_percentile,
                        "team_count": self.total_team_count,
                    },
                    "country": {
                        "rank": self.country_epa_rank,
                        "percentile": self.country_epa_percentile,
                        "team_count": self.country_team_count,
                    },
                    "state": {
                        "rank": self.state_epa_rank,
                        "percentile": self.state_epa_percentile,
                        "team_count": self.state_team_count,
                    },
                    "district": {
                        "rank": self.district_epa_rank,
                        "percentile": self.district_epa_percentile,
                        "team_count": self.district_team_count,
                    },
                },
            },
            "record": {
                "wins": self.wins,
                "losses": self.losses,
                "ties": self.ties,
                "count": self.count,
                "winrate": self.winrate,
            },
            "district_points": self.district_points,
            "district_rank": self.district_rank,
        }

        clean["epa"]["breakdown"]["total_points"] = self.epa
        if self.year >= 2016:
            pairs = list(key_to_name[self.year].items())
            pairs += [("rp_1", "rp_1"), ("rp_2", "rp_2")]
            if self.year >= 2025:
                pairs += [("rp_3", "rp_3")]
            for key, name in pairs:
                clean["epa"]["breakdown"][name] = getattr(self, f"{key}_epa")

        if self.year == CURR_YEAR:
            clean["competing"] = {
                "this_week": self.competing_this_week,
                "next_event_key": self.next_event_key,
                "next_event_name": self.next_event_name,
                "next_event_week": self.next_event_week,
            }

        return clean
