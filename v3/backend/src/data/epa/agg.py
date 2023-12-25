from collections import defaultdict
import statistics
from typing import Callable, Dict, List, Optional

from src.db.models import TeamMatch, TeamEvent
from src.data.utils import objs_type
from src.utils.utils import get_team_event_key
from src.epa.unitless import epa_to_unitless_epa, get_epa_to_norm_epa_func


def process_year_epas(
    tms: List[TeamMatch], acc: Callable[[TeamMatch], Optional[float]], default: float
):
    _arr = [acc(tm) for tm in tms if not tm.offseason]
    arr = [x for x in _arr if x is not None]
    _pre_champs_arr = [acc(tm) for tm in tms if acc(tm) if tm.week < 8]
    pre_champs_arr = [x for x in _pre_champs_arr if x is not None]
    pre_champs = pre_champs_arr[-1] if len(pre_champs_arr) > 0 else default
    end = arr[-1] if len(arr) > 0 else default
    max_ = max(arr[8:]) if len(arr) > 8 else end
    return pre_champs, end, max_


def process_year(objs: objs_type) -> objs_type:
    year = objs[0]

    year_num = year.year
    USE_COMPONENTS = year_num >= 2016

    mean = year.score_mean or 0
    sd = year.score_sd or 0

    curr_epas: Dict[str, float] = {}

    event_team_events_dict: Dict[str, List[TeamEvent]] = defaultdict(list)
    for team_event in objs[3].values():
        event_team_events_dict[team_event.event].append(team_event)

    team_team_matches_dict: Dict[str, List[TeamMatch]] = defaultdict(list)
    team_event_team_matches_dict: Dict[str, List[TeamMatch]] = defaultdict(list)
    for team_match in sorted(objs[6].values(), key=lambda tm: tm.sort()):
        team_team_matches_dict[team_match.team].append(team_match)
        team_event_key = get_team_event_key(team_match.team, team_match.event)
        team_event_team_matches_dict[team_event_key].append(team_match)

    # TEAM YEARS
    total_epas: List[float] = []
    country_epas: Dict[str, List[float]] = defaultdict(list)
    district_epas: Dict[str, List[float]] = defaultdict(list)
    state_epas: Dict[str, List[float]] = defaultdict(list)
    for ty in objs[1].values():
        curr_epas[ty.team] = ty.epa_start

        ms = team_team_matches_dict[ty.team]

        ty.epa_pre_champs, ty.epa_end, ty.epa_max = process_year_epas(
            ms, lambda m: m.epa, ty.epa_start
        )

        if USE_COMPONENTS:
            (
                ty.rp_1_epa_pre_champs,
                ty.rp_1_epa_end,
                ty.rp_1_epa_max,
            ) = process_year_epas(ms, lambda m: m.rp_1_epa, ty.rp_1_epa_start or 0)
            (
                ty.rp_2_epa_pre_champs,
                ty.rp_2_epa_end,
                ty.rp_2_epa_max,
            ) = process_year_epas(ms, lambda m: m.rp_2_epa, ty.rp_2_epa_start or 0)

        if not ty.offseason:
            total_epas.append(ty.epa_end)
            country_epas[ty.country or ""].append(ty.epa_end)
            district_epas[ty.district or ""].append(ty.epa_end)
            state_epas[ty.state or ""].append(ty.epa_end)

    total_epas.sort(reverse=True)
    country_epas = {k: sorted(v, reverse=True) for k, v in country_epas.items()}
    district_epas = {k: sorted(v, reverse=True) for k, v in district_epas.items()}
    state_epas = {k: sorted(v, reverse=True) for k, v in state_epas.items()}

    epa_to_norm_epa = get_epa_to_norm_epa_func(total_epas)
    for ty in objs[1].values():
        unitless_epa: float = epa_to_unitless_epa(ty.epa_end, mean, sd)
        ty.unitless_epa_end = round(unitless_epa, 0)

        norm_epa: float = epa_to_norm_epa(ty.epa_end)
        ty.norm_epa_end = round(norm_epa, 4)

        if ty.offseason:
            continue

        epa = ty.epa_end
        ty.total_epa_rank = total_epas.index(epa) + 1
        ty.total_team_count = len(total_epas)
        ty.total_epa_percentile = round(1 - ty.total_epa_rank / ty.total_team_count, 4)

        country_epas_ = country_epas[ty.country or ""]
        ty.country_epa_rank = country_epas_.index(epa) + 1
        ty.country_team_count = len(country_epas_)
        ty.country_epa_percentile = round(
            1 - ty.country_epa_rank / ty.country_team_count, 4
        )

        district_epas_ = district_epas[ty.district or ""]
        ty.district_epa_rank = district_epas_.index(epa) + 1
        ty.district_team_count = len(district_epas_)
        ty.district_epa_percentile = round(
            1 - ty.district_epa_rank / ty.district_team_count, 4
        )

        state_epas_ = state_epas[ty.state or ""]
        ty.state_epa_rank = state_epas_.index(epa) + 1
        ty.state_team_count = len(state_epas_)
        ty.state_epa_percentile = round(1 - ty.state_epa_rank / ty.state_team_count, 4)

    # YEAR
    year = objs[0]
    sorted_epas = sorted(total_epas, reverse=True)
    year.epa_99p = sorted_epas[int(len(sorted_epas) * 0.01)]
    year.epa_90p = sorted_epas[int(len(sorted_epas) * 0.1)]
    year.epa_75p = sorted_epas[int(len(sorted_epas) * 0.25)]
    year.epa_25p = sorted_epas[int(len(sorted_epas) * 0.75)]

    # EVENTS
    for e in objs[2].values():
        tes = sorted(
            event_team_events_dict[e.key], key=lambda te: te.epa_end, reverse=True
        )

        if len(tes) > 0:
            e.epa_max = max([te.epa_end for te in tes])
            e.epa_mean = statistics.mean([te.epa_end for te in tes])
            e.epa_sd = statistics.stdev([te.epa_end for te in tes])

        if len(tes) >= 8:
            e.epa_top8 = tes[7].epa_end

        if len(tes) >= 24:
            e.epa_top24 = tes[23].epa_end

    # TEAM EVENTS
    for te in sorted(objs[3].values(), key=lambda te: te.week):
        team_event_key = get_team_event_key(te.team, te.event)
        tms = sorted(
            team_event_team_matches_dict[team_event_key], key=lambda tm: tm.time
        )
        qual_tms = [tm for tm in tms if not tm.elim]

        te.epa_start = round(curr_epas[te.team], 2)

        if len(tms) > 0:
            te.epa_start = round(tms[0].epa, 2)
            te.epa_end = round(tms[-1].epa, 2)
            te.epa_mean = round(statistics.mean([tm.epa for tm in tms]), 2)
            te.epa_max = round(max([tm.epa for tm in tms]), 2)
            te.epa_diff = round(te.epa_end - te.epa_start, 2)

            curr_epas[te.team] = te.epa_end  # for next event epa_start

        if len(qual_tms) > 0:
            te.epa_pre_elim = round(qual_tms[-1].epa, 2)

        if USE_COMPONENTS:
            rp_1_epas = [tm.rp_1_epa for tm in tms if tm.rp_1_epa is not None]
            if len(rp_1_epas) > 0:
                te.rp_1_epa_start = round(rp_1_epas[0], 4)
                te.rp_1_epa_end = round(rp_1_epas[-1], 4)
                te.rp_1_epa_mean = round(statistics.mean(rp_1_epas), 4)
                te.rp_1_epa_max = round(max(rp_1_epas), 4)

            rp_2_epas = [tm.rp_2_epa for tm in tms if tm.rp_2_epa is not None]
            if len(rp_2_epas) > 0:
                te.rp_2_epa_start = round(rp_2_epas[0], 4)
                te.rp_2_epa_end = round(rp_2_epas[-1], 4)
                te.rp_2_epa_mean = round(statistics.mean(rp_2_epas), 4)
                te.rp_2_epa_max = round(max(rp_2_epas), 4)

    return objs
