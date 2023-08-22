from sqlalchemy import Float, Integer
from sqlalchemy.orm import mapped_column

from src.db.main import Base
from src.db.models.main import Model, ModelORM, generate_attr_class
from src.db.models.types import MF, MI, MOF


class YearORM(Base, ModelORM):
    """DECLARATION"""

    __tablename__ = "years"
    year: MI = mapped_column(Integer, index=True, primary_key=True)

    """EPA"""
    epa_1p: MOF = mapped_column(Float, nullable=True, default=None)
    epa_10p: MOF = mapped_column(Float, nullable=True, default=None)
    epa_25p: MOF = mapped_column(Float, nullable=True, default=None)
    epa_75p: MOF = mapped_column(Float, nullable=True, default=None)

    auto_epa_1p: MOF = mapped_column(Float, nullable=True, default=None)
    auto_epa_10p: MOF = mapped_column(Float, nullable=True, default=None)
    auto_epa_25p: MOF = mapped_column(Float, nullable=True, default=None)
    auto_epa_75p: MOF = mapped_column(Float, nullable=True, default=None)

    teleop_epa_1p: MOF = mapped_column(Float, nullable=True, default=None)
    teleop_epa_10p: MOF = mapped_column(Float, nullable=True, default=None)
    teleop_epa_25p: MOF = mapped_column(Float, nullable=True, default=None)
    teleop_epa_75p: MOF = mapped_column(Float, nullable=True, default=None)

    endgame_epa_1p: MOF = mapped_column(Float, nullable=True, default=None)
    endgame_epa_10p: MOF = mapped_column(Float, nullable=True, default=None)
    endgame_epa_25p: MOF = mapped_column(Float, nullable=True, default=None)
    endgame_epa_75p: MOF = mapped_column(Float, nullable=True, default=None)

    comp_1_epa_1p: MOF = mapped_column(Float, nullable=True, default=None)
    comp_1_epa_10p: MOF = mapped_column(Float, nullable=True, default=None)
    comp_1_epa_25p: MOF = mapped_column(Float, nullable=True, default=None)
    comp_1_epa_75p: MOF = mapped_column(Float, nullable=True, default=None)

    comp_2_epa_1p: MOF = mapped_column(Float, nullable=True, default=None)
    comp_2_epa_10p: MOF = mapped_column(Float, nullable=True, default=None)
    comp_2_epa_25p: MOF = mapped_column(Float, nullable=True, default=None)
    comp_2_epa_75p: MOF = mapped_column(Float, nullable=True, default=None)

    comp_3_epa_1p: MOF = mapped_column(Float, nullable=True, default=None)
    comp_3_epa_10p: MOF = mapped_column(Float, nullable=True, default=None)
    comp_3_epa_25p: MOF = mapped_column(Float, nullable=True, default=None)
    comp_3_epa_75p: MOF = mapped_column(Float, nullable=True, default=None)

    comp_4_epa_1p: MOF = mapped_column(Float, nullable=True, default=None)
    comp_4_epa_10p: MOF = mapped_column(Float, nullable=True, default=None)
    comp_4_epa_25p: MOF = mapped_column(Float, nullable=True, default=None)
    comp_4_epa_75p: MOF = mapped_column(Float, nullable=True, default=None)

    comp_5_epa_1p: MOF = mapped_column(Float, nullable=True, default=None)
    comp_5_epa_10p: MOF = mapped_column(Float, nullable=True, default=None)
    comp_5_epa_25p: MOF = mapped_column(Float, nullable=True, default=None)
    comp_5_epa_75p: MOF = mapped_column(Float, nullable=True, default=None)

    comp_6_epa_1p: MOF = mapped_column(Float, nullable=True, default=None)
    comp_6_epa_10p: MOF = mapped_column(Float, nullable=True, default=None)
    comp_6_epa_25p: MOF = mapped_column(Float, nullable=True, default=None)
    comp_6_epa_75p: MOF = mapped_column(Float, nullable=True, default=None)

    comp_7_epa_1p: MOF = mapped_column(Float, nullable=True, default=None)
    comp_7_epa_10p: MOF = mapped_column(Float, nullable=True, default=None)
    comp_7_epa_25p: MOF = mapped_column(Float, nullable=True, default=None)
    comp_7_epa_75p: MOF = mapped_column(Float, nullable=True, default=None)

    comp_8_epa_1p: MOF = mapped_column(Float, nullable=True, default=None)
    comp_8_epa_10p: MOF = mapped_column(Float, nullable=True, default=None)
    comp_8_epa_25p: MOF = mapped_column(Float, nullable=True, default=None)
    comp_8_epa_75p: MOF = mapped_column(Float, nullable=True, default=None)

    comp_9_epa_1p: MOF = mapped_column(Float, nullable=True, default=None)
    comp_9_epa_10p: MOF = mapped_column(Float, nullable=True, default=None)
    comp_9_epa_25p: MOF = mapped_column(Float, nullable=True, default=None)
    comp_9_epa_75p: MOF = mapped_column(Float, nullable=True, default=None)

    comp_10_epa_1p: MOF = mapped_column(Float, nullable=True, default=None)
    comp_10_epa_10p: MOF = mapped_column(Float, nullable=True, default=None)
    comp_10_epa_25p: MOF = mapped_column(Float, nullable=True, default=None)
    comp_10_epa_75p: MOF = mapped_column(Float, nullable=True, default=None)

    """WIN PROB"""
    epa_quals_acc: MOF = mapped_column(Float, nullable=True, default=None)
    epa_quals_mse: MOF = mapped_column(Float, nullable=True, default=None)
    quals_count: MI = mapped_column(Integer, default=0)
    epa_elims_acc: MOF = mapped_column(Float, nullable=True, default=None)
    epa_elims_mse: MOF = mapped_column(Float, nullable=True, default=None)
    elims_count: MI = mapped_column(Integer, default=0)
    epa_champs_acc: MOF = mapped_column(Float, nullable=True, default=None)
    epa_champs_mse: MOF = mapped_column(Float, nullable=True, default=None)
    champs_count: MI = mapped_column(Integer, default=0)
    epa_acc: MOF = mapped_column(Float, nullable=True, default=None)
    epa_mse: MOF = mapped_column(Float, nullable=True, default=None)
    count: MI = mapped_column(Integer, default=0)

    """RP PROB"""
    rp_1_champs_acc: MOF = mapped_column(Float, nullable=True, default=None)
    rp_1_champs_mse: MOF = mapped_column(Float, nullable=True, default=None)
    rp_2_champs_acc: MOF = mapped_column(Float, nullable=True, default=None)
    rp_2_champs_mse: MOF = mapped_column(Float, nullable=True, default=None)
    rp_champs_count: MI = mapped_column(Integer, default=0)
    rp_1_acc: MOF = mapped_column(Float, nullable=True, default=None)
    rp_1_mse: MOF = mapped_column(Float, nullable=True, default=None)
    rp_2_acc: MOF = mapped_column(Float, nullable=True, default=None)
    rp_2_mse: MOF = mapped_column(Float, nullable=True, default=None)
    rp_count: MI = mapped_column(Integer, default=0)

    """CONSTANTS"""
    # TODO: enforce consistent order of score mean, score sd, no_foul, foul, auto, teleop, endgame, rp_1, rp_2, comps
    score_mean: MF = mapped_column(Float, default=0)
    score_sd: MF = mapped_column(Float, default=0)
    foul_mean: MOF = mapped_column(Float, nullable=True, default=None)
    no_foul_mean: MOF = mapped_column(Float, nullable=True, default=None)
    auto_mean: MOF = mapped_column(Float, nullable=True, default=None)
    teleop_mean: MOF = mapped_column(Float, nullable=True, default=None)
    endgame_mean: MOF = mapped_column(Float, nullable=True, default=None)
    rp_1_mean: MOF = mapped_column(Float, nullable=True, default=None)
    rp_2_mean: MOF = mapped_column(Float, nullable=True, default=None)
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


_Year = generate_attr_class("Year", YearORM)


class Year(_Year, Model):
    def pk(self: "Year") -> str:
        return str(self.year)

    def __str__(self: "Year") -> str:
        # Only refresh DB if these change (during 1 min partial update)
        return f"{self.year}_{self.count}"


def create_year_obj(year: int) -> Year:
    return Year(year=year)
