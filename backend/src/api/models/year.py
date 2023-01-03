import attr

from src.api.models.main import APIModel


@attr.s(auto_attribs=True, slots=True)
class PercentileStats:
    p99: float
    p95: float
    p90: float
    p75: float
    p50: float
    p25: float
    mean: float
    sd: float


@attr.s(auto_attribs=True, slots=True)
class APIYear(APIModel):
    year: int
    total_stats: PercentileStats
    auto_stats: PercentileStats
    teleop_stats: PercentileStats
    endgame_stats: PercentileStats
    rp_1_stats: PercentileStats
    rp_2_stats: PercentileStats
    foul_rate: float
