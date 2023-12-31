from typing import Any, Dict

import numpy as np
from sqlalchemy import Float, Integer
from sqlalchemy.orm import mapped_column

from src.breakdown import key_to_name
from src.db.main import Base
from src.db.models.main import Model, ModelORM, generate_attr_class
from src.db.models.types import MF, MI, MOF


class YearORM(Base, ModelORM):
    """DECLARATION"""

    __tablename__ = "years"
    year: MI = mapped_column(Integer, index=True, primary_key=True)

    """CONSTANTS"""
    score_mean: MF = mapped_column(Float, default=0)
    score_sd: MF = mapped_column(Float, default=0)
    foul_mean: MOF = mapped_column(Float, nullable=True, default=None)
    no_foul_mean: MOF = mapped_column(Float, nullable=True, default=None)
    auto_mean: MOF = mapped_column(Float, nullable=True, default=None)
    teleop_mean: MOF = mapped_column(Float, nullable=True, default=None)
    endgame_mean: MOF = mapped_column(Float, nullable=True, default=None)
    rp_1_mean: MOF = mapped_column(Float, nullable=True, default=None)
    rp_2_mean: MOF = mapped_column(Float, nullable=True, default=None)
    tiebreaker_mean: MOF = mapped_column(Float, nullable=True, default=None)
    comp_1_mean: MOF = mapped_column(Float, nullable=True, default=None)
    comp_2_mean: MOF = mapped_column(Float, nullable=True, default=None)
    comp_3_mean: MOF = mapped_column(Float, nullable=True, default=None)
    comp_4_mean: MOF = mapped_column(Float, nullable=True, default=None)
    comp_5_mean: MOF = mapped_column(Float, nullable=True, default=None)
    comp_6_mean: MOF = mapped_column(Float, nullable=True, default=None)
    comp_7_mean: MOF = mapped_column(Float, nullable=True, default=None)
    comp_8_mean: MOF = mapped_column(Float, nullable=True, default=None)
    comp_9_mean: MOF = mapped_column(Float, nullable=True, default=None)
    comp_10_mean: MOF = mapped_column(Float, nullable=True, default=None)
    comp_11_mean: MOF = mapped_column(Float, nullable=True, default=None)
    comp_12_mean: MOF = mapped_column(Float, nullable=True, default=None)
    comp_13_mean: MOF = mapped_column(Float, nullable=True, default=None)
    comp_14_mean: MOF = mapped_column(Float, nullable=True, default=None)
    comp_15_mean: MOF = mapped_column(Float, nullable=True, default=None)
    comp_16_mean: MOF = mapped_column(Float, nullable=True, default=None)
    comp_17_mean: MOF = mapped_column(Float, nullable=True, default=None)
    comp_18_mean: MOF = mapped_column(Float, nullable=True, default=None)

    """EPA"""
    epa_99p: MOF = mapped_column(Float, nullable=True, default=None)
    epa_90p: MOF = mapped_column(Float, nullable=True, default=None)
    epa_75p: MOF = mapped_column(Float, nullable=True, default=None)
    epa_25p: MOF = mapped_column(Float, nullable=True, default=None)

    auto_epa_99p: MOF = mapped_column(Float, nullable=True, default=None)
    auto_epa_90p: MOF = mapped_column(Float, nullable=True, default=None)
    auto_epa_75p: MOF = mapped_column(Float, nullable=True, default=None)
    auto_epa_25p: MOF = mapped_column(Float, nullable=True, default=None)

    teleop_epa_99p: MOF = mapped_column(Float, nullable=True, default=None)
    teleop_epa_90p: MOF = mapped_column(Float, nullable=True, default=None)
    teleop_epa_75p: MOF = mapped_column(Float, nullable=True, default=None)
    teleop_epa_25p: MOF = mapped_column(Float, nullable=True, default=None)

    endgame_epa_99p: MOF = mapped_column(Float, nullable=True, default=None)
    endgame_epa_90p: MOF = mapped_column(Float, nullable=True, default=None)
    endgame_epa_75p: MOF = mapped_column(Float, nullable=True, default=None)
    endgame_epa_25p: MOF = mapped_column(Float, nullable=True, default=None)

    rp_1_epa_99p: MOF = mapped_column(Float, nullable=True, default=None)
    rp_1_epa_90p: MOF = mapped_column(Float, nullable=True, default=None)
    rp_1_epa_75p: MOF = mapped_column(Float, nullable=True, default=None)
    rp_1_epa_25p: MOF = mapped_column(Float, nullable=True, default=None)

    rp_2_epa_99p: MOF = mapped_column(Float, nullable=True, default=None)
    rp_2_epa_90p: MOF = mapped_column(Float, nullable=True, default=None)
    rp_2_epa_75p: MOF = mapped_column(Float, nullable=True, default=None)
    rp_2_epa_25p: MOF = mapped_column(Float, nullable=True, default=None)

    comp_1_epa_99p: MOF = mapped_column(Float, nullable=True, default=None)
    comp_1_epa_90p: MOF = mapped_column(Float, nullable=True, default=None)
    comp_1_epa_75p: MOF = mapped_column(Float, nullable=True, default=None)
    comp_1_epa_25p: MOF = mapped_column(Float, nullable=True, default=None)

    comp_2_epa_99p: MOF = mapped_column(Float, nullable=True, default=None)
    comp_2_epa_90p: MOF = mapped_column(Float, nullable=True, default=None)
    comp_2_epa_75p: MOF = mapped_column(Float, nullable=True, default=None)
    comp_2_epa_25p: MOF = mapped_column(Float, nullable=True, default=None)

    comp_3_epa_99p: MOF = mapped_column(Float, nullable=True, default=None)
    comp_3_epa_90p: MOF = mapped_column(Float, nullable=True, default=None)
    comp_3_epa_75p: MOF = mapped_column(Float, nullable=True, default=None)
    comp_3_epa_25p: MOF = mapped_column(Float, nullable=True, default=None)

    comp_4_epa_99p: MOF = mapped_column(Float, nullable=True, default=None)
    comp_4_epa_90p: MOF = mapped_column(Float, nullable=True, default=None)
    comp_4_epa_75p: MOF = mapped_column(Float, nullable=True, default=None)
    comp_4_epa_25p: MOF = mapped_column(Float, nullable=True, default=None)

    comp_5_epa_99p: MOF = mapped_column(Float, nullable=True, default=None)
    comp_5_epa_90p: MOF = mapped_column(Float, nullable=True, default=None)
    comp_5_epa_75p: MOF = mapped_column(Float, nullable=True, default=None)
    comp_5_epa_25p: MOF = mapped_column(Float, nullable=True, default=None)

    comp_6_epa_99p: MOF = mapped_column(Float, nullable=True, default=None)
    comp_6_epa_90p: MOF = mapped_column(Float, nullable=True, default=None)
    comp_6_epa_75p: MOF = mapped_column(Float, nullable=True, default=None)
    comp_6_epa_25p: MOF = mapped_column(Float, nullable=True, default=None)

    comp_7_epa_99p: MOF = mapped_column(Float, nullable=True, default=None)
    comp_7_epa_90p: MOF = mapped_column(Float, nullable=True, default=None)
    comp_7_epa_75p: MOF = mapped_column(Float, nullable=True, default=None)
    comp_7_epa_25p: MOF = mapped_column(Float, nullable=True, default=None)

    comp_8_epa_99p: MOF = mapped_column(Float, nullable=True, default=None)
    comp_8_epa_90p: MOF = mapped_column(Float, nullable=True, default=None)
    comp_8_epa_75p: MOF = mapped_column(Float, nullable=True, default=None)
    comp_8_epa_25p: MOF = mapped_column(Float, nullable=True, default=None)

    comp_9_epa_99p: MOF = mapped_column(Float, nullable=True, default=None)
    comp_9_epa_90p: MOF = mapped_column(Float, nullable=True, default=None)
    comp_9_epa_75p: MOF = mapped_column(Float, nullable=True, default=None)
    comp_9_epa_25p: MOF = mapped_column(Float, nullable=True, default=None)

    comp_10_epa_99p: MOF = mapped_column(Float, nullable=True, default=None)
    comp_10_epa_90p: MOF = mapped_column(Float, nullable=True, default=None)
    comp_10_epa_75p: MOF = mapped_column(Float, nullable=True, default=None)
    comp_10_epa_25p: MOF = mapped_column(Float, nullable=True, default=None)

    comp_11_epa_99p: MOF = mapped_column(Float, nullable=True, default=None)
    comp_11_epa_90p: MOF = mapped_column(Float, nullable=True, default=None)
    comp_11_epa_75p: MOF = mapped_column(Float, nullable=True, default=None)
    comp_11_epa_25p: MOF = mapped_column(Float, nullable=True, default=None)

    comp_12_epa_99p: MOF = mapped_column(Float, nullable=True, default=None)
    comp_12_epa_90p: MOF = mapped_column(Float, nullable=True, default=None)
    comp_12_epa_75p: MOF = mapped_column(Float, nullable=True, default=None)
    comp_12_epa_25p: MOF = mapped_column(Float, nullable=True, default=None)

    comp_13_epa_99p: MOF = mapped_column(Float, nullable=True, default=None)
    comp_13_epa_90p: MOF = mapped_column(Float, nullable=True, default=None)
    comp_13_epa_75p: MOF = mapped_column(Float, nullable=True, default=None)
    comp_13_epa_25p: MOF = mapped_column(Float, nullable=True, default=None)

    comp_14_epa_99p: MOF = mapped_column(Float, nullable=True, default=None)
    comp_14_epa_90p: MOF = mapped_column(Float, nullable=True, default=None)
    comp_14_epa_75p: MOF = mapped_column(Float, nullable=True, default=None)
    comp_14_epa_25p: MOF = mapped_column(Float, nullable=True, default=None)

    comp_15_epa_99p: MOF = mapped_column(Float, nullable=True, default=None)
    comp_15_epa_90p: MOF = mapped_column(Float, nullable=True, default=None)
    comp_15_epa_75p: MOF = mapped_column(Float, nullable=True, default=None)
    comp_15_epa_25p: MOF = mapped_column(Float, nullable=True, default=None)

    comp_16_epa_99p: MOF = mapped_column(Float, nullable=True, default=None)
    comp_16_epa_90p: MOF = mapped_column(Float, nullable=True, default=None)
    comp_16_epa_75p: MOF = mapped_column(Float, nullable=True, default=None)
    comp_16_epa_25p: MOF = mapped_column(Float, nullable=True, default=None)

    comp_17_epa_99p: MOF = mapped_column(Float, nullable=True, default=None)
    comp_17_epa_90p: MOF = mapped_column(Float, nullable=True, default=None)
    comp_17_epa_75p: MOF = mapped_column(Float, nullable=True, default=None)
    comp_17_epa_25p: MOF = mapped_column(Float, nullable=True, default=None)

    comp_18_epa_99p: MOF = mapped_column(Float, nullable=True, default=None)
    comp_18_epa_90p: MOF = mapped_column(Float, nullable=True, default=None)
    comp_18_epa_75p: MOF = mapped_column(Float, nullable=True, default=None)
    comp_18_epa_25p: MOF = mapped_column(Float, nullable=True, default=None)

    """WIN PROB PRED"""
    count: MI = mapped_column(Integer, default=0)
    epa_conf: MOF = mapped_column(Float, nullable=True, default=None)
    epa_acc: MOF = mapped_column(Float, nullable=True, default=None)
    epa_mse: MOF = mapped_column(Float, nullable=True, default=None)
    champs_count: MI = mapped_column(Integer, default=0)
    epa_champs_conf: MOF = mapped_column(Float, nullable=True, default=None)
    epa_champs_acc: MOF = mapped_column(Float, nullable=True, default=None)
    epa_champs_mse: MOF = mapped_column(Float, nullable=True, default=None)

    """SCORE PRED"""

    epa_score_rmse: MOF = mapped_column(Float, nullable=True, default=None)
    epa_score_mae: MOF = mapped_column(Float, nullable=True, default=None)
    epa_score_error: MOF = mapped_column(Float, nullable=True, default=None)
    epa_champs_score_rmse: MOF = mapped_column(Float, nullable=True, default=None)
    epa_champs_score_mae: MOF = mapped_column(Float, nullable=True, default=None)
    epa_champs_score_error: MOF = mapped_column(Float, nullable=True, default=None)

    """RP PRED"""
    rp_count: MI = mapped_column(Integer, default=0)
    epa_rp_1_error: MOF = mapped_column(Float, nullable=True, default=None)
    epa_rp_1_acc: MOF = mapped_column(Float, nullable=True, default=None)
    epa_rp_1_ll: MOF = mapped_column(Float, nullable=True, default=None)
    epa_rp_1_f1: MOF = mapped_column(Float, nullable=True, default=None)
    epa_rp_2_error: MOF = mapped_column(Float, nullable=True, default=None)
    epa_rp_2_acc: MOF = mapped_column(Float, nullable=True, default=None)
    epa_rp_2_ll: MOF = mapped_column(Float, nullable=True, default=None)
    epa_rp_2_f1: MOF = mapped_column(Float, nullable=True, default=None)
    champs_rp_count: MI = mapped_column(Integer, default=0)
    epa_champs_rp_1_error: MOF = mapped_column(Float, nullable=True, default=None)
    epa_champs_rp_1_acc: MOF = mapped_column(Float, nullable=True, default=None)
    epa_champs_rp_1_ll: MOF = mapped_column(Float, nullable=True, default=None)
    epa_champs_rp_1_f1: MOF = mapped_column(Float, nullable=True, default=None)
    epa_champs_rp_2_error: MOF = mapped_column(Float, nullable=True, default=None)
    epa_champs_rp_2_acc: MOF = mapped_column(Float, nullable=True, default=None)
    epa_champs_rp_2_ll: MOF = mapped_column(Float, nullable=True, default=None)
    epa_champs_rp_2_f1: MOF = mapped_column(Float, nullable=True, default=None)


_Year = generate_attr_class("Year", YearORM)


class Year(_Year, Model):
    def pk(self: "Year") -> str:
        return str(self.year)

    def __hash__(self: "Year") -> int:
        return hash(self.pk())

    def __str__(self: "Year") -> str:
        # Only refresh DB if these change (during 1 min partial update)
        return "_".join([str(self.year), str(self.count)])

    def get_foul_rate(self: "Year") -> float:
        return (self.foul_mean or 0) / (self.no_foul_mean or 1)

    def get_mean_components(self: "Year") -> Any:
        if self.year < 2016:
            return np.array([self.score_mean])
        return np.array(
            [
                self.no_foul_mean,
                self.auto_mean,
                self.teleop_mean,
                self.endgame_mean,
                self.rp_1_mean,
                self.rp_2_mean,
                self.tiebreaker_mean,
                self.comp_1_mean,
                self.comp_2_mean,
                self.comp_3_mean,
                self.comp_4_mean,
                self.comp_5_mean,
                self.comp_6_mean,
                self.comp_7_mean,
                self.comp_8_mean,
                self.comp_9_mean,
                self.comp_10_mean,
                self.comp_11_mean,
                self.comp_12_mean,
                self.comp_13_mean,
                self.comp_14_mean,
                self.comp_15_mean,
                self.comp_16_mean,
                self.comp_17_mean,
                self.comp_18_mean,
            ]
        )

    def to_dict(self) -> Dict[str, Any]:
        clean: Dict[str, Any] = {
            "year": self.year,
            "score_mean": self.score_mean,
            "score_sd": self.score_sd,
            "percentiles": {
                "total_points": {
                    99: self.epa_99p,
                    90: self.epa_90p,
                    75: self.epa_75p,
                    25: self.epa_25p,
                },
            },
            "breakdown": {},
            "metrics": {
                "win_prob": {
                    "season": {
                        "count": self.count,
                        "conf": self.epa_conf,
                        "acc": self.epa_acc,
                        "mse": self.epa_mse,
                    },
                    "champs": {
                        "count": self.champs_count,
                        "conf": self.epa_champs_conf,
                        "acc": self.epa_champs_acc,
                        "mse": self.epa_champs_mse,
                    },
                },
            },
        }

        if self.year >= 2016:
            clean["breakdown"] = {
                "foul_mean": self.foul_mean,
                "no_foul_mean": self.no_foul_mean,
            }
            for k in ["auto", "teleop", "endgame", "rp_1", "rp_2", "tiebreaker"] + [
                f"comp_{i}" for i in range(1, 19)
            ]:
                if k not in key_to_name[self.year]:
                    continue
                name = key_to_name[self.year][k]
                clean["breakdown"][f"{name}_mean"] = getattr(self, f"{k}_mean")
                if k != "tiebreaker":
                    clean["percentiles"][name] = {
                        99: getattr(self, f"{k}_epa_99p"),
                        90: getattr(self, f"{k}_epa_90p"),
                        75: getattr(self, f"{k}_epa_75p"),
                        25: getattr(self, f"{k}_epa_25p"),
                    }

            clean["metrics"]["score_pred"] = {
                "season": {
                    "count": 2 * self.count,
                    "rmse": self.epa_score_rmse,
                    "mae": self.epa_score_mae,
                    "error": self.epa_score_error,
                },
                "champs": {
                    "count": 2 * self.champs_count,
                    "rmse": self.epa_champs_score_rmse,
                    "mae": self.epa_champs_score_mae,
                    "error": self.epa_champs_score_error,
                },
            }

            clean["metrics"]["rp_pred"] = {
                "season": {
                    "count": self.rp_count,
                    key_to_name[self.year]["rp_1"]: {
                        "error": self.epa_rp_1_error,
                        "acc": self.epa_rp_1_acc,
                        "ll": self.epa_rp_1_ll,
                        "f1": self.epa_rp_1_f1,
                    },
                    key_to_name[self.year]["rp_2"]: {
                        "error": self.epa_rp_2_error,
                        "acc": self.epa_rp_2_acc,
                        "ll": self.epa_rp_2_ll,
                        "f1": self.epa_rp_2_f1,
                    },
                },
                "champs": {
                    "count": self.champs_rp_count,
                    key_to_name[self.year]["rp_1"]: {
                        "error": self.epa_champs_rp_1_error,
                        "acc": self.epa_champs_rp_1_acc,
                        "ll": self.epa_champs_rp_1_ll,
                        "f1": self.epa_champs_rp_1_f1,
                    },
                    key_to_name[self.year]["rp_2"]: {
                        "error": self.epa_champs_rp_2_error,
                        "acc": self.epa_champs_rp_2_acc,
                        "ll": self.epa_champs_rp_2_ll,
                        "f1": self.epa_champs_rp_2_f1,
                    },
                },
            }

        return clean
