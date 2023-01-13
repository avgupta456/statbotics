import attr

from src.site.models.main import APIModel


@attr.s(auto_attribs=True, slots=True)
class APITeamEvent(APIModel):
    num: int
    team: str
    event: str
    event_name: str
    week: int
    time: int
    num_teams: int
    # For simulation initial conditions
    start_total_epa: float
    start_rp_1_epa: float
    start_rp_2_epa: float
    # For tables and figures
    total_epa: float
    auto_epa: float
    teleop_epa: float
    endgame_epa: float
    rp_1_epa: float
    rp_2_epa: float
    wins: int
    losses: int
    ties: int
    count: int
    rank: int
    rps_per_match: float
    offseason: bool
