from datetime import timedelta
from typing import Callable, List, Optional

from src.api.models import APITeamEvent
from src.data.nepa import get_epa_to_norm_epa_func
from src.db.models import TeamEvent
from src.db.read import get_team_events as _get_team_events
from src.utils.alru_cache import alru_cache


def unpack_team_event(
    epa_to_norm_epa: Callable[[float], float], team_event: TeamEvent
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
        rank=team_event.rank or -1,
        offseason=team_event.offseason,
    )


@alru_cache(ttl=timedelta(minutes=5))
async def get_team_events(
    year: Optional[int] = None,
    event: Optional[int] = None,
    team: Optional[int] = None,
    epa_to_norm_epa: Optional[Callable[[float], float]] = None,
    no_cache: bool = False,
) -> List[TeamEvent]:
    team_event_objs: List[TeamEvent] = _get_team_events(
        team=team, year=year, event=event
    )

    if epa_to_norm_epa is None:
        epa_to_norm_epa = get_epa_to_norm_epa_func(year)

    team_events = [unpack_team_event(epa_to_norm_epa, x) for x in team_event_objs]
    return (True, sorted(team_events, key=lambda x: x.time))  # type: ignore
