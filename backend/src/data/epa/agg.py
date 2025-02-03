import statistics
from collections import defaultdict
from typing import Callable, Dict, List, Optional, Tuple

from src.data.utils import objs_type
from src.db.models import TeamEvent, TeamMatch
from src.models.epa.unitless import epa_to_unitless_epa, get_epa_to_norm_epa_func
from src.utils.utils import get_team_event_key, r


def process_year_epas(
    tms: List[TeamMatch], acc: Callable[[TeamMatch], Optional[float]], default: float
):
    _arr = [acc(tm) for tm in tms]
    arr = [x for x in _arr if x is not None]
    _pre_champs_arr = [acc(tm) for tm in tms if acc(tm) if tm.week < 8]
    pre_champs_arr = [x for x in _pre_champs_arr if x is not None]
    pre_champs = pre_champs_arr[-1] if len(pre_champs_arr) > 0 else default
    end = arr[-1] if len(arr) > 0 else default
    max_ = max(arr[8:]) if len(arr) > 8 else end
    return pre_champs, end, max_


def process_year(objs: objs_type) -> objs_type:
    year = objs[0]

    mean = year.score_mean or 0
    sd = year.score_sd or 0

    curr_epas: Dict[int, float] = {}

    event_team_events_dict: Dict[str, List[TeamEvent]] = defaultdict(list)
    for team_event in objs[3].values():
        event_team_events_dict[team_event.event].append(team_event)

    team_team_matches_dict: Dict[int, List[TeamMatch]] = defaultdict(list)
    team_event_team_matches_dict: Dict[str, List[TeamMatch]] = defaultdict(list)
    for team_match in sorted(objs[5].values(), key=lambda tm: tm.sort()):
        team_team_matches_dict[team_match.team].append(team_match)
        team_event_key = get_team_event_key(team_match.team, team_match.event)
        team_event_team_matches_dict[team_event_key].append(team_match)

    # TEAM YEARS
    epa_list: List[float] = []
    total_epas: List[Tuple[int, float]] = []
    country_epas: Dict[str, List[Tuple[int, float]]] = defaultdict(list)
    state_epas: Dict[str, List[Tuple[int, float]]] = defaultdict(list)
    district_epas: Dict[str, List[Tuple[int, float]]] = defaultdict(list)
    for ty in objs[1].values():
        curr_epas[ty.team] = ty.epa_start

        ms = team_team_matches_dict[ty.team]

        ty.epa_pre_champs, ty.epa, ty.epa_max = process_year_epas(
            ms, lambda m: m.post_epa, ty.epa_start
        )

        epa_list.append(ty.epa)
        total_epas.append((ty.team, ty.epa))
        country_epas[ty.country or ""].append((ty.team, ty.epa))
        district_epas[ty.district or ""].append((ty.team, ty.epa))
        state_epas[ty.state or ""].append((ty.team, ty.epa))

    epa_list.sort(reverse=True)

    def epa_tups_to_teams(v: List[Tuple[int, float]]):
        return [x[0] for x in sorted(v, reverse=True, key=lambda x: x[1])]

    sorted_teams = epa_tups_to_teams(total_epas)
    country_sorted_teams = {k: epa_tups_to_teams(v) for k, v in country_epas.items()}
    state_sorted_teams = {k: epa_tups_to_teams(v) for k, v in state_epas.items()}
    district_sorted_teams = {k: epa_tups_to_teams(v) for k, v in district_epas.items()}

    epa_to_norm_epa = get_epa_to_norm_epa_func(epa_list)
    for ty in objs[1].values():
        unitless_epa: float = epa_to_unitless_epa(ty.epa, mean, sd)
        ty.unitless_epa = r(unitless_epa)

        norm_epa: float = epa_to_norm_epa(ty.epa)
        ty.norm_epa = r(norm_epa)

        team = ty.team
        total_epa_rank = sorted_teams.index(team) + 1
        total_team_count = len(total_epas)
        ty.total_epa_percentile = r(1 - total_epa_rank / total_team_count, 4)
        ty.total_epa_rank = total_epa_rank
        ty.total_team_count = total_team_count

        country_epas_ = country_sorted_teams[ty.country or ""]
        country_epa_rank = country_epas_.index(team) + 1
        country_team_count = len(country_epas_)
        ty.country_epa_percentile = r(1 - country_epa_rank / country_team_count, 4)
        ty.country_epa_rank = country_epa_rank
        ty.country_team_count = country_team_count

        state_epas_ = state_sorted_teams[ty.state or ""]
        state_epa_rank = state_epas_.index(team) + 1
        state_team_count = len(state_epas_)
        ty.state_epa_percentile = r(1 - state_epa_rank / state_team_count, 4)
        ty.state_epa_rank = state_epa_rank
        ty.state_team_count = state_team_count

        district_epas_ = district_sorted_teams[ty.district or ""]
        district_epa_rank = district_epas_.index(team) + 1
        district_team_count = len(district_epas_)
        ty.district_epa_percentile = r(1 - district_epa_rank / district_team_count, 4)
        ty.district_epa_rank = district_epa_rank
        ty.district_team_count = district_team_count

    # YEAR
    def get_percentiles(arr: List[float]) -> Tuple[float, float, float, float]:
        sorted_arr = sorted(arr, reverse=True)
        return (
            sorted_arr[int(len(sorted_arr) * 0.01)],
            sorted_arr[int(len(sorted_arr) * 0.1)],
            sorted_arr[int(len(sorted_arr) * 0.25)],
            sorted_arr[int(len(sorted_arr) * 0.75)],
        )

    year = objs[0]
    sorted_epas = sorted(epa_list, reverse=True)
    year.epa_99p, year.epa_90p, year.epa_75p, year.epa_25p = get_percentiles(
        sorted_epas
    )

    if year.year >= 2016:
        for key in ["auto", "teleop", "endgame", "rp_1", "rp_2", "rp_3"] + [
            f"comp_{i}" for i in range(1, 19)
        ]:
            raw_epas = [getattr(ty, f"{key}_epa") for ty in objs[1].values()]
            epas: List[float] = [epa for epa in raw_epas if epa is not None]
            p99, p90, p75, p25 = get_percentiles(epas)
            setattr(year, f"{key}_epa_99p", p99)
            setattr(year, f"{key}_epa_90p", p90)
            setattr(year, f"{key}_epa_75p", p75)
            setattr(year, f"{key}_epa_25p", p25)

    # TEAM EVENTS
    for te in sorted(objs[3].values(), key=lambda te: te.week):
        unitless_epa: float = epa_to_unitless_epa(te.epa, mean, sd)
        te.unitless_epa = r(unitless_epa)

        norm_epa: float = epa_to_norm_epa(te.epa)
        te.norm_epa = r(norm_epa)

        team_event_key = get_team_event_key(te.team, te.event)
        tms = sorted(
            team_event_team_matches_dict[team_event_key], key=lambda tm: tm.time
        )
        qual_tms = [tm for tm in tms if not tm.elim]

        te.epa_start = r(curr_epas[te.team], 2)

        if len(tms) > 0:
            te.epa_start = r(tms[0].epa, 2)
            te.epa_mean = r(statistics.mean([tm.epa for tm in tms]), 2)
            te.epa_max = r(max([tm.epa for tm in tms]), 2)

            curr_epas[te.team] = te.epa  # for next event epa_start

        if len(qual_tms) > 0:
            te.epa_pre_elim = r(qual_tms[-1].epa, 2)

    # EVENTS
    for e in objs[2].values():
        tes = sorted(event_team_events_dict[e.key], key=lambda te: te.epa, reverse=True)
        if len(tes) > 0:
            e.epa_max = max([te.epa for te in tes])
            e.epa_mean = r(statistics.mean([te.epa for te in tes]), 2)
            if len(tes) >= 2:
                e.epa_sd = r(statistics.stdev([te.epa for te in tes]), 2)

        if len(tes) >= 8:
            e.epa_top_8 = tes[7].epa

        if len(tes) >= 24:
            e.epa_top_24 = tes[23].epa

    return objs
