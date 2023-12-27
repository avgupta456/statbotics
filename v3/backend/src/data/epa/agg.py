from collections import defaultdict
import statistics
from typing import Callable, Dict, List, Optional

from src.types.enums import AllianceColor
from src.db.models import TeamMatch, TeamEvent
from src.data.utils import objs_type
from src.utils.utils import get_team_event_key
from src.epa.unitless import epa_to_unitless_epa, get_epa_to_norm_epa_func
from src.utils.utils import r


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

    # ALLIANCES
    matches = objs[4]
    alliances = objs[5]
    for a in alliances.values():
        is_red = a.alliance == AllianceColor.RED
        m = matches[a.match]
        if m.epa_win_prob is not None:
            a.epa_win_prob = m.epa_win_prob if is_red else r(1 - m.epa_win_prob, 4)
        a.epa_winner = m.epa_winner
        a.score_pred = m.epa_red_score_pred if is_red else m.epa_blue_score_pred
        if USE_COMPONENTS:
            a.rp_1_pred = m.epa_red_rp_1_pred if is_red else m.epa_blue_rp_1_pred
            a.rp_2_pred = m.epa_red_rp_2_pred if is_red else m.epa_blue_rp_2_pred

    # TEAM YEARS
    total_epas: List[float] = []
    country_epas: Dict[str, List[float]] = defaultdict(list)
    district_epas: Dict[str, List[float]] = defaultdict(list)
    state_epas: Dict[str, List[float]] = defaultdict(list)
    for ty in objs[1].values():
        curr_epas[ty.team] = ty.epa_start

        ms = team_team_matches_dict[ty.team]

        ty.epa_pre_champs, ty.epa, ty.epa_max = process_year_epas(
            ms, lambda m: m.post_epa, ty.epa_start
        )

        if not ty.offseason:
            total_epas.append(ty.epa)
            country_epas[ty.country or ""].append(ty.epa)
            district_epas[ty.district or ""].append(ty.epa)
            state_epas[ty.state or ""].append(ty.epa)

    total_epas.sort(reverse=True)
    country_epas = {k: sorted(v, reverse=True) for k, v in country_epas.items()}
    district_epas = {k: sorted(v, reverse=True) for k, v in district_epas.items()}
    state_epas = {k: sorted(v, reverse=True) for k, v in state_epas.items()}

    epa_to_norm_epa = get_epa_to_norm_epa_func(total_epas)
    for ty in objs[1].values():
        unitless_epa: float = epa_to_unitless_epa(ty.epa, mean, sd)
        ty.unitless_epa = r(unitless_epa)

        norm_epa: float = epa_to_norm_epa(ty.epa)
        ty.norm_epa = r(norm_epa)

        if ty.offseason:
            continue

        epa = ty.epa
        ty.total_epa_rank = total_epas.index(epa) + 1
        ty.total_team_count = len(total_epas)
        ty.total_epa_percentile = r(1 - ty.total_epa_rank / ty.total_team_count, 4)

        country_epas_ = country_epas[ty.country or ""]
        ty.country_epa_rank = country_epas_.index(epa) + 1
        ty.country_team_count = len(country_epas_)
        ty.country_epa_percentile = r(
            1 - ty.country_epa_rank / ty.country_team_count, 4
        )

        district_epas_ = district_epas[ty.district or ""]
        ty.district_epa_rank = district_epas_.index(epa) + 1
        ty.district_team_count = len(district_epas_)
        ty.district_epa_percentile = r(
            1 - ty.district_epa_rank / ty.district_team_count, 4
        )

        state_epas_ = state_epas[ty.state or ""]
        ty.state_epa_rank = state_epas_.index(epa) + 1
        ty.state_team_count = len(state_epas_)
        ty.state_epa_percentile = r(1 - ty.state_epa_rank / ty.state_team_count, 4)

    # YEAR
    year = objs[0]
    sorted_epas = sorted(total_epas, reverse=True)
    year.epa_99p = sorted_epas[int(len(sorted_epas) * 0.01)]
    year.epa_90p = sorted_epas[int(len(sorted_epas) * 0.1)]
    year.epa_75p = sorted_epas[int(len(sorted_epas) * 0.25)]
    year.epa_25p = sorted_epas[int(len(sorted_epas) * 0.75)]

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
            e.epa_mean = statistics.mean([te.epa for te in tes])
            e.epa_sd = statistics.stdev([te.epa for te in tes])

        if len(tes) >= 8:
            e.epa_top8 = tes[7].epa

        if len(tes) >= 24:
            e.epa_top24 = tes[23].epa

    return objs
