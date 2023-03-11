from datetime import timedelta
from typing import Callable, List, Optional

from src.data.nepa import (
    epa_to_unitless_epa as _epa_to_unitless_epa,
    get_epa_to_norm_epa_func,
)
from src.db.models import TeamEvent
from src.db.read import get_team_events as _get_team_events
from src.site.models import APITeamEvent
from src.utils.alru_cache import alru_cache


def unpack_team_event(
    team_event: TeamEvent,
    epa_to_unitless_epa: Callable[[float], float],
    epa_to_norm_epa: Callable[[float], float],
) -> APITeamEvent:
    return APITeamEvent(
        num=team_event.team,
        team=team_event.team_name or str(team_event.team),
        event=team_event.event,
        event_name=team_event.event_name or "",
        week=team_event.week or -1,
        time=team_event.time,
        num_teams=team_event.num_teams or -1,
        start_total_epa=team_event.epa_start or 0,
        start_rp_1_epa=team_event.rp_1_epa_start or 0,
        start_rp_2_epa=team_event.rp_2_epa_start or 0,
        total_epa=team_event.epa_end or 0,
        unitless_epa=epa_to_unitless_epa(team_event.epa_end or 0),
        norm_epa=epa_to_norm_epa(team_event.epa_end or 0),
        auto_epa=team_event.auto_epa_end or 0,
        teleop_epa=team_event.teleop_epa_end or 0,
        endgame_epa=team_event.endgame_epa_end or 0,
        rp_1_epa=team_event.rp_1_epa_end or 0,
        rp_2_epa=team_event.rp_2_epa_end or 0,
        wins=team_event.wins,
        losses=team_event.losses,
        ties=team_event.ties,
        count=team_event.count,
        qual_wins=team_event.qual_wins,
        qual_losses=team_event.qual_losses,
        qual_ties=team_event.qual_ties,
        qual_count=team_event.qual_count,
        rank=team_event.rank or -1,
        rps=team_event.rps or 0,
        rps_per_match=team_event.rps_per_match or 0,
        offseason=team_event.offseason,
    )


@alru_cache(ttl=timedelta(minutes=1))
async def get_team_events(
    year: int,
    score_mean: float,
    score_sd: float,
    event: Optional[str] = None,
    team: Optional[int] = None,
    epa_to_norm_epa: Optional[Callable[[float], float]] = None,
    no_cache: bool = False,
) -> List[APITeamEvent]:
    team_event_objs: List[TeamEvent] = _get_team_events(
        year=year, team=team, event=event
    )

    if epa_to_norm_epa is None:
        epa_to_norm_epa = get_epa_to_norm_epa_func(year)

    def epa_to_unitless_epa(epa: float) -> float:
        return _epa_to_unitless_epa(epa, score_mean, score_sd)

    team_events = [
        unpack_team_event(x, epa_to_unitless_epa, epa_to_norm_epa)
        for x in team_event_objs
    ]
    return (True, sorted(team_events, key=lambda x: x.time))  # type: ignore
