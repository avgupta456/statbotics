import statistics
from collections import defaultdict
from typing import Any, Dict, List, Tuple, Union

from db.models.event import Event
from db.models.match import Match
from db.models.team_event import TeamEvent
from db.models.team_match import TeamMatch
from db.models.team_year import TeamYear
from db.models.year import Year
from helper.utils import logistic, logistic_inv
from models import opr as opr_model


def process_event(
    event: Event,
    team_events: List[TeamEvent],
    matches: List[Match],
    year: int,
    mean_score: float,
    sd_score: float,
) -> Tuple[Any, Any, List[Union[int, float]]]:
    matches = sorted(matches, key=lambda m: (m.playoff, m.sort()))
    oprs, ils = opr_model.opr_v2(event, team_events, matches, mean_score)
    opr_acc, opr_mse, mix_acc, mix_mse, count = 0, 0, 0, 0, 0
    rp1_acc, rp1_mse, rp2_acc, rp2_mse, count_rp = 0, 0, 0, 0, 0

    for i, m in enumerate(matches):
        red, blue = m.get_teams()
        red_oprs: List[float] = []
        blue_oprs: List[float] = []
        ind = -1 if m.playoff else i

        for r in red:
            if r in oprs and len(oprs[r]) > 0 and ind <= len(oprs[r]):
                red_oprs.append(round(oprs[r][ind][0], 2))
        for b in blue:
            if b in oprs and len(oprs[b]) > 0 and ind <= len(oprs[b]):
                blue_oprs.append(round(oprs[b][ind][0], 2))

        win_probs = {"red": 1, "blue": 0, "draw": 0.5}
        red_sum, blue_sum = sum(red_oprs), sum(blue_oprs)
        m.red_opr_sum = red_sum
        m.blue_opr_sum = blue_sum

        winner = m.winner or "red"  # in practice, never None
        m.opr_winner = "red" if red_sum > blue_sum else "blue"
        win_prob = opr_model.win_prob(red_sum, blue_sum, sd_score)
        m.opr_win_prob = round(win_prob, 4)
        opr_mse += (win_probs[winner] - win_prob) ** 2
        if m.opr_winner == winner:
            opr_acc += 1

        win_prob = 0.5 * ((m.elo_win_prob or 0) + m.opr_win_prob)
        m.mix_winner = "red" if win_prob > 0.5 else "blue"
        m.mix_win_prob = round(win_prob, 4)
        mix_mse += (win_probs[winner] - win_prob) ** 2
        if m.mix_winner == winner:
            mix_acc += 1

        count += 1

        if year >= 2016 and not m.playoff:
            m.red_ils_1_sum = red_ils_1_sum = round(
                sum([ils[r][ind][0] for r in red]), 2
            )
            m.red_ils_2_sum = red_ils_2_sum = round(
                sum([ils[r][ind][1] for r in red]), 2
            )
            m.blue_ils_1_sum = blue_ils_1_sum = round(
                sum([ils[b][ind][0] for b in blue]), 2
            )
            m.blue_ils_2_sum = blue_ils_2_sum = round(
                sum([ils[b][ind][1] for b in blue]), 2
            )

            m.red_rp_1_prob = red_rp_1_prob = round(logistic(red_ils_1_sum), 4)
            m.red_rp_2_prob = red_rp_2_prob = round(logistic(red_ils_2_sum), 4)
            m.blue_rp_1_prob = blue_rp_1_prob = round(logistic(blue_ils_1_sum), 4)
            m.blue_rp_2_prob = blue_rp_2_prob = round(logistic(blue_ils_2_sum), 4)

            red_rp_1, red_rp_2 = m.red_rp_1, m.red_rp_2
            blue_rp_1, blue_rp_2 = m.blue_rp_1, m.blue_rp_2

            if int(red_rp_1_prob + 0.5) == red_rp_1:
                rp1_acc += 1
            if int(red_rp_2_prob + 0.5) == red_rp_2:
                rp2_acc += 1
            if int(blue_rp_1_prob + 0.5) == blue_rp_1:
                rp1_acc += 1
            if int(blue_rp_2_prob + 0.5) == blue_rp_2:
                rp2_acc += 1

            rp1_mse += (red_rp_1_prob - (red_rp_1 or 0)) ** 2
            rp2_mse += (red_rp_2_prob - (red_rp_2 or 0)) ** 2
            rp1_mse += (blue_rp_1_prob - (blue_rp_1 or 0)) ** 2
            rp2_mse += (blue_rp_2_prob - (blue_rp_2 or 0)) ** 2

            count_rp += 2

    opr_stats = [opr_acc, opr_mse, mix_acc, mix_mse, count]
    rp_stats = [rp1_acc, rp1_mse, rp2_acc, rp2_mse, count_rp]

    event.opr_acc = round(opr_acc / count, 4)
    event.opr_mse = round(opr_mse / count, 4)
    event.mix_acc = round(mix_acc / count, 4)
    event.mix_mse = round(mix_mse / count, 4)

    if count_rp > 0:
        event.rp1_acc = round(rp1_acc / count_rp, 4)
        event.rp1_mse = round(rp1_mse / count_rp, 4)
        event.rp2_acc = round(rp2_acc / count_rp, 4)
        event.rp2_mse = round(rp2_mse / count_rp, 4)

    stats = opr_stats + rp_stats

    return oprs, ils, stats


def process_year(
    year_num: int,
    team_years_all: Dict[int, Dict[int, TeamYear]],
    means: Dict[int, float],
    year: Year,
    team_years: List[TeamYear],
    events: List[Event],
    team_events: List[TeamEvent],
    matches: List[Match],
    team_matches: List[TeamMatch],
) -> Tuple[
    Dict[int, Dict[int, TeamYear]],
    Dict[int, float],
    Year,
    List[TeamYear],
    List[Event],
    List[TeamEvent],
    List[Match],
    List[TeamMatch],
]:
    sd_score = year.score_sd or 1
    mean_score = year.score_mean or 1
    TM = 2 if year_num <= 2004 else 3

    team_years_dict: Dict[int, TeamYear] = {}
    team_oprs_dict: Dict[int, float] = {}

    opr_acc, opr_mse, mix_acc, mix_mse, count = 0, 0, 0, 0, 0
    rp1_acc, rp1_mse, rp2_acc, rp2_mse, count_rp = 0, 0, 0, 0, 0

    # populate starting OPR from previous year
    means[year_num] = mean_score
    prior_opr_global = mean_score / TM
    ils_1_seed = logistic_inv((year.rp_1_mean or 0) / TM)
    ils_2_seed = logistic_inv((year.rp_2_mean or 0) / TM)
    team_ils_1: Dict[int, float] = {}
    team_ils_2: Dict[int, float] = {}

    for team_year_obj in team_years:
        num = team_year_obj.team
        prior_opr = prior_opr_global

        if year_num in [2022, 2023]:
            # For 2022 and 2023, use past year team competed (up to 2019)
            for past_year in range(2019, year_num):
                past_team_year = team_years_all.get(past_year, {}).get(num, None)
                if past_team_year is not None and past_team_year.opr_end is not None:
                    prior_opr = past_team_year.opr_end / means[past_year] * mean_score
        else:
            # Otherwise use the most recent years (regardless of team activity)
            team_year_1 = team_years_all.get(year_num - 1, {}).get(num, None)
            if team_year_1 is not None and team_year_1.opr_end is not None:
                prior_opr = team_year_1.opr_end / means[year_num - 1] * mean_score

        prior_opr = round(0.80 * prior_opr + 0.20 * prior_opr_global, 2)
        team_year_obj.opr_start = prior_opr
        team_year_obj.opr_end = prior_opr  # will be overwritten
        team_year_obj.opr = prior_opr  # copies opr_end

        if year_num >= 2016:
            rate = prior_opr / prior_opr_global
            team_year_obj.opr_auto = rate * (year.auto_mean or 0) / TM
            team_year_obj.opr_teleop = rate * (year.teleop_mean or 0) / TM
            team_year_obj.opr_1 = rate * (year.rp_1_mean or 0) / TM
            team_year_obj.opr_2 = rate * (year.rp_2_mean or 0) / TM
            team_year_obj.opr_endgame = rate * (year.endgame_mean or 0) / TM
            team_year_obj.opr_fouls = rate * (year.fouls_mean or 0) / TM
            team_year_obj.opr_no_fouls = rate * (year.no_fouls_mean or 0) / TM
            team_year_obj.opr = rate * (year.no_fouls_mean or 0) / TM  # copies opr_no_fouls

        boost = ((team_year_obj.elo_start or 0) - 1500) * 0.001
        team_ils_1[num] = max(-1 / 3, ils_1_seed + boost)
        team_ils_2[num] = max(-1 / 3, ils_2_seed + boost)
        if year_num >= 2016:
            team_year_obj.ils_1 = round(team_ils_1[num], 2)
            team_year_obj.ils_2 = round(team_ils_2[num], 2)

        team_years_dict[num] = team_year_obj
        team_oprs_dict[num] = prior_opr

    team_team_events: Dict[int, List[Dict[str, float]]] = defaultdict(list)
    event_team_events: Dict[str, List[TeamEvent]] = defaultdict(list)
    filtered_team_events = [t for t in team_events if t.status != "Upcoming"]
    for team_event in filtered_team_events:
        event_team_events[team_event.event].append(team_event)

    matches_dict: Dict[str, List[Match]] = defaultdict(list)
    filtered_matches = [m for m in matches if m.status == "Completed"]
    for match in filtered_matches:
        matches_dict[match.event].append(match)

    t_team_match_dict = Dict[str, Dict[int, List[TeamMatch]]]
    team_matches_dict: t_team_match_dict = defaultdict(lambda: defaultdict(list))
    filtered_team_matches = [m for m in team_matches if m.status == "Completed"]
    for team_match in filtered_team_matches:
        event_key, team_id = team_match.event, team_match.team
        team_matches_dict[event_key][team_id].append(team_match)

    filtered_events = [e for e in events if e.status != "Upcoming"]
    for event in filtered_events:
        event_matches = matches_dict[event.key]
        if len(event_matches) == 0:
            continue

        for team_event in event_team_events[event.key]:
            num = team_event.team
            if num not in team_oprs_dict or num not in team_years_dict:
                continue

            team_event.opr_start = team_oprs_dict[num]
            team_event.opr_end = team_oprs_dict[num]  # overwritten later
            if year_num >= 2016:
                team_event.opr_auto = team_years_dict[num].opr_auto
                team_event.opr_teleop = team_years_dict[num].opr_teleop
                team_event.opr_1 = team_years_dict[num].opr_1
                team_event.opr_2 = team_years_dict[num].opr_2
                team_event.opr_endgame = team_years_dict[num].opr_endgame
                team_event.opr_fouls = team_years_dict[num].opr_fouls
                team_event.opr_no_fouls = team_years_dict[num].opr_no_fouls
                team_event.ils_1_start = round(team_ils_1[num], 2)
                team_event.ils_2_start = round(team_ils_2[num], 2)
                team_event.ils_1_end = team_ils_1[num]  # overwritten later
                team_event.ils_2_end = team_ils_2[num]  # overwritten later

        oprs, ils, stats = process_event(
            event,
            event_team_events[event.key],
            event_matches,
            year_num,
            mean_score,
            sd_score,
        )

        opr_acc += stats[0]
        opr_mse += stats[1]
        mix_acc += stats[2]
        mix_mse += stats[3]
        count += stats[4]
        rp1_acc += stats[5]
        rp1_mse += stats[6]
        rp2_acc += stats[7]
        rp2_mse += stats[8]
        count_rp += stats[9]

        for team_event in event_team_events[event.key]:
            num = team_event.team
            if num not in oprs:
                continue

            opr = round(oprs[num][-1][0], 2)
            ils_1 = round(ils[num][-1][0], 2)
            ils_2 = round(ils[num][-1][1], 2)

            event_dict = {
                "opr_end": opr,
                "opr_auto": round(oprs[num][-1][1], 2),
                "opr_teleop": round(oprs[num][-1][2], 2),
                "opr_1": round(oprs[num][-1][3], 2),
                "opr_2": round(oprs[num][-1][4], 2),
                "opr_endgame": round(oprs[num][-1][5], 2),
                "opr_fouls": round(oprs[num][-1][6], 2),
                "opr_no_fouls": round(oprs[num][-1][7], 2),
                "ils_1_end": ils_1,
                "ils_2_end": ils_2,
            }

            team_event.opr_end = event_dict["opr_end"]
            if year_num >= 2016:
                team_event.opr_auto = event_dict["opr_auto"]
                team_event.opr_teleop = event_dict["opr_teleop"]
                team_event.opr_1 = event_dict["opr_1"]
                team_event.opr_2 = event_dict["opr_2"]
                team_event.opr_endgame = event_dict["opr_endgame"]
                team_event.opr_fouls = event_dict["opr_fouls"]
                team_event.opr_no_fouls = event_dict["opr_no_fouls"]
                team_event.ils_1_end = event_dict["ils_1_end"]
                team_event.ils_2_end = event_dict["ils_2_end"]
            team_team_events[num].append(event_dict)

            team_oprs_dict[num] = opr
            team_ils_1[num] = ils_1
            team_ils_2[num] = ils_2

            team_matches_temp = sorted(
                team_matches_dict[event.key][num], key=lambda m: (m.playoff, m.sort())
            )
            for i, m in enumerate(team_matches_temp):
                index = min(i, len(oprs[num]) - 1)
                m.opr = round(oprs[num][index][0], 2)
                if year_num >= 2016:
                    m.opr_auto = round(oprs[num][index][1], 2)
                    m.opr_teleop = round(oprs[num][index][2], 2)
                    m.opr_one = round(oprs[num][index][3], 2)
                    m.opr_two = round(oprs[num][index][4], 2)
                    m.opr_endgame = round(oprs[num][index][5], 2)
                    m.opr_fouls = round(oprs[num][index][6], 2)
                    m.opr_no_fouls = round(oprs[num][index][7], 2)
                    m.ils_1 = round(ils[num][index][0], 2)
                    m.ils_2 = round(ils[num][index][1], 2)

        oprs_end = sorted([round(oprs[t][-1][0], 2) for t in oprs], reverse=True)
        event.opr_max = oprs_end[0]
        event.opr_top8 = None if len(oprs_end) < 8 else oprs_end[7]
        event.opr_top24 = None if len(oprs_end) < 24 else oprs_end[23]
        event.opr_mean = round(sum(oprs_end) / len(oprs_end), 2)
        event.opr_sd = round(statistics.pstdev(oprs_end), 2)

    opr_str = "opr_end" if year_num < 2016 else "opr_no_fouls"

    best_oprs: List[float] = []
    for num in team_years_dict:
        if len(team_team_events[num]) == 0:
            continue

        obj = team_years_dict[num]
        best_event = sorted(
            team_team_events[num],
            key=lambda x: x[opr_str],
        )[-1]

        obj.opr_end = best_event["opr_end"]
        obj.opr = best_event["opr_end"]  # copies opr_end
        if year_num >= 2016:
            obj.opr_auto = best_event["opr_auto"]
            obj.opr_teleop = best_event["opr_teleop"]
            obj.opr_1 = best_event["opr_1"]
            obj.opr_2 = best_event["opr_2"]
            obj.opr_endgame = best_event["opr_endgame"]
            obj.opr_fouls = best_event["opr_fouls"]
            obj.opr_no_fouls = best_event["opr_no_fouls"]
            obj.opr = best_event["opr_no_fouls"]  # copies opr_no_fouls
            obj.ils_1 = team_ils_1[num]
            obj.ils_2 = team_ils_2[num]

        best_oprs.append(best_event[opr_str])

    best_oprs.sort(reverse=True)
    team_year_count = len(best_oprs)
    for num in team_years_dict:
        if len(team_team_events[num]) == 0:
            continue

        obj = team_years_dict[num]
        value = (obj.opr_end if year_num < 2016 else obj.opr_no_fouls) or 0
        obj.opr_rank = rank = best_oprs.index(value) + 1
        obj.opr_percentile = round(rank / team_year_count, 4)

    team_years_all[year_num] = team_years_dict

    if len(best_oprs) > 0:
        year.opr_max = best_oprs[0]
        year.opr_1p = best_oprs[round(0.01 * team_year_count)]
        year.opr_5p = best_oprs[round(0.05 * team_year_count)]
        year.opr_10p = best_oprs[round(0.10 * team_year_count)]
        year.opr_25p = best_oprs[round(0.25 * team_year_count)]
        year.opr_median = best_oprs[round(0.50 * team_year_count)]
        year.opr_mean = round(sum(best_oprs) / team_year_count, 2)
        year.opr_sd = round(statistics.pstdev(best_oprs), 2)

    year.opr_acc = None if count == 0 else round(opr_acc / count, 4)
    year.opr_mse = None if count == 0 else round(opr_mse / count, 4)
    year.mix_acc = None if count == 0 else round(mix_acc / count, 4)
    year.mix_mse = None if count == 0 else round(mix_mse / count, 4)
    year.rp1_acc = None if count_rp == 0 or year_num < 2016 else round(rp1_acc / count_rp, 4)
    year.rp1_mse = None if count_rp == 0 or year_num < 2016 else round(rp1_mse / count_rp, 4)
    year.rp2_acc = None if count_rp == 0 or year_num < 2016 else round(rp2_acc / count_rp, 4)
    year.rp2_mse = None if count_rp == 0 or year_num < 2016 else round(rp2_mse / count_rp, 4)

    return (
        team_years_all,
        means,
        year,
        team_years,
        events,
        team_events,
        matches,
        team_matches,
    )
