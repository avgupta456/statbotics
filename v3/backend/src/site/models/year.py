import attr

from src.site.models.main import APIModel


@attr.s(auto_attribs=True, slots=True)
class PercentileStats(APIModel):
    p99: float
    p90: float
    p75: float
    p25: float


@attr.s(auto_attribs=True, slots=True)
class APIYear(APIModel):
    year: int
    score_mean: float
    score_sd: float
    total_stats: PercentileStats
    auto_stats: PercentileStats
    teleop_stats: PercentileStats
    endgame_stats: PercentileStats
    rp_1_stats: PercentileStats
    rp_2_stats: PercentileStats
    foul_rate: float
