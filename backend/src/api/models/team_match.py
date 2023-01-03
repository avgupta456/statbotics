import attr

from src.api.models.main import APIModel


@attr.s(auto_attribs=True, slots=True)
class APITeamMatch(APIModel):
    match: int
    label: str
    time: int
    playoff: bool
    norm_epa: float
    total_epa: float
    auto_epa: float
    teleop_epa: float
    endgame_epa: float
    rp_1_epa: float
    rp_2_epa: float
