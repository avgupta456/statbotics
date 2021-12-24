from datetime import datetime
from collections import defaultdict
import statistics
from typing import Any, Dict, List, Tuple, Union

from db.models.event import Event
from db.models.match import Match
from db.models.team_event import TeamEvent
from db.models.team_match import TeamMatch
from db.models.team_year import TeamYear
from db.read.event import get_events as get_events_db
from db.read.match import get_matches as get_matches_db
from db.read.team_event import get_team_events as get_team_events_db
from db.read.team_match import get_team_matches as get_team_matches_db
from db.read.team_year import get_team_years as get_team_years_db
from db.read.year import get_years as get_years_db
from db.write.main import (
    update_events as update_events_db,
    update_matches as update_matches_db,
    update_team_events as update_team_events_db,
    update_team_matches as update_team_matches_db,
    update_team_years as update_team_years_db,
    update_years as update_years_db,
)

from helper.utils import logistic, logistic_inv
from models import opr as opr_model


def process_event(
    event: Event,
    team_events: List[TeamEvent],
    quals: List[Match],
    playoffs: List[Match],
    year: int,
    mean_score: float,
    sd_score: float,
) -> Tuple[Any, Any, List[Union[int, float]]]:
    oprs, ils = opr_model.opr_v2(event, team_events, quals, playoffs, mean_score)
    opr_acc, opr_mse, mix_acc, mix_mse, count = 0, 0, 0, 0, 0
    rp1_acc, rp1_mse, rp2_acc, rp2_mse, count_rp = 0, 0, 0, 0, 0

    for i, m in enumerate(sorted(quals) + sorted(playoffs)):
        red, blue = m.get_teams()
        red_oprs: List[float] = []
        blue_oprs: List[float] = []
        ind = -1 if m.playoff == 1 else i

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
        m.opr_win_prob = opr_model.win_prob(red_sum, blue_sum, sd_score)
        opr_mse += (win_probs[winner] - m.opr_win_prob) ** 2
        if m.opr_winner == winner:
            opr_acc += 1

        m.mix_win_prob = 0.5 * (m.elo_win_prob + m.opr_win_prob)
        m.mix_winner = "red" if m.mix_win_prob > 0.5 else "blue"

        mix_mse += (win_probs[winner] - m.mix_win_prob) ** 2
        if m.mix_winner == winner:
            mix_acc += 1

        count += 1

        if year >= 2016 and m.playoff == 0:
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

            m.red_rp_1_prob = red_rp_1_prob = logistic(red_ils_1_sum)
            m.red_rp_2_prob = red_rp_2_prob = logistic(red_ils_2_sum)
            m.blue_rp_1_prob = blue_rp_1_prob = logistic(blue_ils_1_sum)
            m.blue_rp_2_prob = blue_rp_2_prob = logistic(blue_ils_2_sum)

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

            rp1_mse += (red_rp_1_prob - red_rp_1) ** 2
            rp2_mse += (red_rp_2_prob - red_rp_2) ** 2
            rp1_mse += (blue_rp_1_prob - blue_rp_1) ** 2
            rp2_mse += (blue_rp_2_prob - blue_rp_2) ** 2

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


def process(start_year: int, end_year: int):
    team_years_all: Dict[int, Dict[int, TeamYear]] = {}  # master dictionary
    means: Dict[int, float] = {}

    if start_year > 2003:
        team_years_2 = {}
        for team_year in get_team_years_db(start_year - 2):
            team_years_2[team_year.team_id] = team_year
        team_years_all[start_year - 2] = team_years_2

    if start_year > 2002:
        team_years_1 = {}
        for team_year in get_team_years_db(start_year - 1):
            team_years_1[team_year.team_id] = team_year
        team_years_all[start_year - 1] = team_years_1
        means[start_year - 1] = get_years_db(start_year - 1)[0].score_mean

    for year in range(start_year, end_year + 1):
        print("Year:", year)
        start = datetime.now()
        year_obj = get_years_db(year)[0]
        sd_score = year_obj.score_sd
        mean_score = year_obj.score_mean
        TM = 2 if year <= 2004 else 3

        team_years: Dict[int, TeamYear] = {}
        team_oprs: Dict[int, float] = {}

        opr_acc, opr_mse, mix_acc, mix_mse, count = 0, 0, 0, 0, 0
        rp1_acc, rp1_mse, rp2_acc, rp2_mse, count_rp = 0, 0, 0, 0, 0

        # populate starting OPR from previous year
        means[year] = mean_score
        prior_opr_global = mean_score / TM
        ils_1_seed = logistic_inv(year_obj.rp_1_mean / TM)
        ils_2_seed = logistic_inv(year_obj.rp_2_mean / TM)
        team_ils_1, team_ils_2 = {}, {}

        team_year_objs = get_team_years_db(year)
        for team_year_obj in team_year_objs:
            num = team_year_obj.team_id
            prior_opr = prior_opr_global
            if (
                year - 1 in team_years_all
                and num in team_years_all[year - 1]
                and team_years_all[year - 1][num].opr_end is not None
            ):
                prior_opr = team_years_all[year - 1][num].opr_end
                prior_opr = prior_opr / means[year - 1] * mean_score
                prior_opr = round(0.90 * prior_opr + 0.10 * prior_opr_global, 2)
            team_year_obj.opr_start = prior_opr
            team_year_obj.opr_end = prior_opr  # will be overwritten

            rate = prior_opr / prior_opr_global
            team_year_obj.opr_auto = rate * year_obj.auto_mean / TM
            team_year_obj.opr_teleop = rate * year_obj.teleop_mean / TM
            team_year_obj.opr_1 = rate * year_obj.rp_1_mean / TM
            team_year_obj.opr_2 = rate * year_obj.rp_2_mean / TM
            team_year_obj.opr_endgame = rate * year_obj.endgame_mean / TM
            # TODO: standardize 'foul' vs 'fouls'
            team_year_obj.opr_fouls = rate * year_obj.foul_mean / TM
            team_year_obj.opr_no_fouls = rate * year_obj.no_foul_mean / TM

            boost = (team_year_obj.elo_start - 1500) * 0.001
            team_year_obj.ils_1 = team_ils_1[num] = max(-1 / 3, ils_1_seed + boost)
            team_year_obj.ils_2 = team_ils_2[num] = max(-1 / 3, ils_2_seed + boost)

            team_years[num] = team_year_obj
            team_oprs[num] = prior_opr

        team_team_events: Dict[int, List[Dict[str, float]]] = defaultdict(list)

        events = sorted(get_events_db(year))
        team_events = get_team_events_db(year)
        event_team_events: Dict[int, List[TeamEvent]] = defaultdict(list)
        for team_event in team_events:
            event_team_events[team_event.event_id].append(team_event)

        team_matches = get_team_matches_db(year=year)
        t_team_match_dict = Dict[int, Dict[int, List[TeamMatch]]]
        team_matches_dict: t_team_match_dict = defaultdict(lambda: defaultdict(list))
        for team_match in team_matches:
            event_id, team_id = team_match.event_id, team_match.team_id
            team_matches_dict[event_id][team_id].append(team_match)

        matches = get_matches_db(year=year)
        matches_dict: Dict[int, List[Match]] = defaultdict(list)
        for match in matches:
            matches_dict[match.event_id].append(match)

        for event in events:
            for team_event in event_team_events[event.id]:
                num = team_event.team_id
                team_event.opr_start = team_oprs[num]
                team_event.opr_end = team_oprs[num]  # overwritten later
                team_event.opr_auto = team_years[num].opr_auto
                team_event.opr_teleop = team_years[num].opr_teleop
                team_event.opr_1 = team_years[num].opr_1
                team_event.opr_2 = team_years[num].opr_2
                team_event.opr_endgame = team_years[num].opr_endgame
                team_event.opr_fouls = team_years[num].opr_fouls
                team_event.opr_no_fouls = team_years[num].opr_no_fouls
                team_event.ils_1_start = team_ils_1[num]
                team_event.ils_2_start = team_ils_2[num]
                team_event.ils_1_end = team_ils_1[num]  # overwritten later
                team_event.ils_2_end = team_ils_2[num]  # overwritten later

            event_matches = matches_dict[event.id]
            quals = sorted([m for m in event_matches if m.playoff == 0])
            playoffs = sorted([m for m in event_matches if m.playoff == 1])
            oprs, ils, stats = process_event(
                event,
                event_team_events[event.id],
                quals,
                playoffs,
                year,
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

            for team_event in event_team_events[event.id]:
                num = team_event.team_id
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

                team_oprs[num] = opr
                team_ils_1[num] = ils_1
                team_ils_2[num] = ils_2

                team_matches = sorted(team_matches_dict[event.id][num])
                for i, m in enumerate(team_matches):
                    index = min(i, len(team_matches) - 1, len(oprs[num]) - 1)
                    m.opr_score = round(oprs[num][index][0], 2)
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
            event.opr_top8 = -1 if len(oprs_end) < 8 else oprs_end[7]
            event.opr_top24 = -1 if len(oprs_end) < 24 else oprs_end[23]
            event.opr_mean = round(sum(oprs_end) / len(oprs_end), 2)
            event.opr_sd = round(statistics.pstdev(oprs_end), 2)

        update_events_db(events)
        del events
        update_team_events_db(team_events)
        del team_events

        update_matches_db(matches)
        del matches
        update_team_matches_db(team_matches)
        del team_matches

        best_oprs: List[float] = []
        for num in team_years:
            if len(team_team_events[num]) == 0:
                continue

            obj = team_years[num]
            best_event = sorted(
                team_team_events[num],
                key=lambda x: x["opr_end" if year < 2016 else "opr_no_fouls"],
            )[-1]

            obj.opr_end = best_event["opr_end"]
            obj.opr_auto = best_event["opr_auto"]
            obj.opr_teleop = best_event["opr_teleop"]
            obj.opr_1 = best_event["opr_1"]
            obj.opr_2 = best_event["opr_2"]
            obj.opr_endgame = best_event["opr_endgame"]
            obj.opr_fouls = best_event["opr_fouls"]
            obj.opr_no_fouls = best_event["opr_no_fouls"]
            obj.ils_1 = team_ils_1[num]
            obj.ils_2 = team_ils_2[num]

            best_oprs.append(best_event["opr_end" if year < 2016 else "opr_no_fouls"])

        best_oprs.sort(reverse=True)
        team_year_count = len(best_oprs)
        for num in team_years:
            if len(team_team_events[num]) == 0:
                continue

            obj = team_years[num]
            obj.opr_rank = rank = (
                best_oprs.index(obj.opr_end if year < 2016 else obj.opr_no_fouls) + 1
            )
            obj.opr_percentile = round(rank / team_year_count, 4)

        team_years_all[year] = team_years
        if year - 2 in team_years_all:
            team_years_all.pop(year - 2)

        year_obj.opr_max = best_oprs[0]
        year_obj.opr_1p = best_oprs[round(0.01 * team_year_count)]
        year_obj.opr_5p = best_oprs[round(0.05 * team_year_count)]
        year_obj.opr_10p = best_oprs[round(0.10 * team_year_count)]
        year_obj.opr_25p = best_oprs[round(0.25 * team_year_count)]
        year_obj.opr_median = best_oprs[round(0.50 * team_year_count)]
        year_obj.opr_mean = round(sum(best_oprs) / team_year_count, 2)
        year_obj.opr_sd = round(statistics.pstdev(best_oprs), 2)

        year_obj.opr_acc = round(opr_acc / count, 4)
        year_obj.opr_mse = round(opr_mse / count, 4)
        year_obj.mix_acc = round(mix_acc / count, 4)
        year_obj.mix_mse = round(mix_mse / count, 4)
        year_obj.rp1_acc = -1 if year < 2016 else round(rp1_acc / count_rp, 4)
        year_obj.rp1_mse = -1 if year < 2016 else round(rp1_mse / count_rp, 4)
        year_obj.rp2_acc = -1 if year < 2016 else round(rp2_acc / count_rp, 4)
        year_obj.rp2_mse = -1 if year < 2016 else round(rp2_mse / count_rp, 4)

        update_years_db([year_obj])
        update_team_years_db(team_year_objs)
        del team_year_objs

        end = datetime.now()
        print(year, end - start)


def main(start_year: int, end_year: int):
    process(start_year, end_year)
