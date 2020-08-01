import statistics
from collections import defaultdict

from helper.utils import clean, logistic, logistic_inv
from models import opr as opr_model
from process.logging import printStats


def process_event(event, quals, playoffs, year, sd_score, team_ils_1, team_ils_2):
    oprs, ils = opr_model.opr_v2(event, quals, playoffs)
    opr_acc, opr_mse, mix_acc, mix_mse, count = 0, 0, 0, 0, 0
    rp1_acc, rp1_mse, rp2_acc, rp2_mse, count_rp = 0, 0, 0, 0, 0

    for i, m in enumerate(sorted(quals) + sorted(playoffs)):
        red, blue = m.getRed(), m.getBlue()
        red_oprs, blue_oprs = [], []
        ind = -1 if m.playoff == 1 else i

        for r in red:
            if r in oprs and len(oprs[r]) > 0 and ind <= len(oprs[r]):
                red_oprs.append(clean(oprs[r][ind][0]))
        for b in blue:
            if b in oprs and len(oprs[b]) > 0 and ind <= len(oprs[b]):
                blue_oprs.append(clean(oprs[b][ind][0]))

        win_probs = {"red": 1, "blue": 0, "draw": 0.5}
        red_sum, blue_sum = sum(red_oprs), sum(blue_oprs)
        m.red_opr_sum, m.blue_opr_sum = red_sum, blue_sum
        m.opr_winner = "red" if red_sum > blue_sum else "blue"
        m.opr_win_prob = opr_model.win_prob(red_sum, blue_sum, year, sd_score)
        opr_mse += (win_probs[m.winner] - m.opr_win_prob) ** 2
        if m.opr_winner == m.winner:
            opr_acc += 1

        m.mix_win_prob = 0.5 * (m.elo_win_prob + m.opr_win_prob)
        m.mix_winner = "red" if m.mix_win_prob > 0.5 else "blue"
        mix_mse += (win_probs[m.winner] - m.mix_win_prob) ** 2
        if m.winner == m.mix_winner:
            mix_acc += 1

        count += 1

        """ILS STATS"""
        if year >= 2016 and m.playoff == 0:
            # only predict on quals as elims don't have Ranking Points
            m.red_ils_1_sum = red_ils_1_sum = sum([clean(ils[r][ind][0]) for r in red])
            m.red_ils_2_sum = red_ils_2_sum = sum([clean(ils[r][ind][1]) for r in red])
            m.blue_ils_1_sum = blue_ils_1_sum = sum(
                [clean(ils[b][ind][0]) for b in blue]
            )
            m.blue_ils_2_sum = blue_ils_2_sum = sum(
                [clean(ils[b][ind][1]) for b in blue]
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

    return oprs, ils, team_ils_1, team_ils_2, stats


def process(start_year, end_year, SQL_Read, SQL_Write):
    teams, means = {}, {}
    for team in SQL_Read.getTeams():
        teams[team.id] = team

    team_years_all = {}  # master dictionary

    if start_year > 2003:
        team_years_2 = {}
        teamYears2 = SQL_Read.getTeamYears(year=start_year - 2)
        for teamYear in teamYears2:
            team_years_2[teamYear.team_id] = teamYear
        team_years_all[start_year - 2] = team_years_2

    if start_year > 2002:
        team_years_1 = {}
        teamYears1 = SQL_Read.getTeamYears(year=start_year - 1)
        for teamYear in teamYears1:
            team_years_1[teamYear.team_id] = teamYear
        team_years_all[start_year - 1] = team_years_1
        means[start_year - 1] = SQL_Read.getYear(year=start_year - 1).score_mean

    for year in range(start_year, end_year + 1):
        print(year)
        year_obj = SQL_Read.getYear(year)
        sd_score = year_obj.score_sd
        TM = 2 if year <= 2004 else 3

        team_years, team_oprs = {}, {}
        opr_acc, opr_mse, mix_acc, mix_mse, count = 0, 0, 0, 0, 0
        rp1_acc, rp1_mse, rp2_acc, rp2_mse, count_rp = 0, 0, 0, 0, 0

        # populate starting elo from previous year
        mean_score = year_obj.score_mean
        means[year] = mean_score
        prior_opr_global = mean_score / TM
        ils_1_seed = logistic_inv(year_obj.rp_1_mean / TM)
        ils_2_seed = logistic_inv(year_obj.rp_2_mean / TM)
        team_ils_1, team_ils_2 = {}, {}
        temp = 0
        for teamYear in SQL_Read.getTeamYears(year=year):
            num = teamYear.team_id
            prior_opr = prior_opr_global
            if (
                year - 1 in team_years_all
                and num in team_years_all[year - 1]
                and team_years_all[year - 1][num].opr_end is not None
            ):
                prior_opr = team_years_all[year - 1][num].opr_end
                prior_opr = prior_opr / means[year - 1] * mean_score
                prior_opr = 0.90 * prior_opr + 0.10 * prior_opr_global
            teamYear.opr_start = prior_opr
            teamYear.opr_end = prior_opr  # will be overwritten

            rate = prior_opr / prior_opr_global
            teamYear.opr_auto = rate * year_obj.auto_mean / TM
            teamYear.opr_teleop = rate * year_obj.teleop_mean / TM
            teamYear.opr_1 = rate * year_obj.one_mean / TM
            teamYear.opr_2 = rate * year_obj.two_mean / TM
            teamYear.opr_endgame = rate * year_obj.endgame_mean / TM
            teamYear.opr_fouls = year_obj.foul_mean / TM  # no rate
            teamYear.opr_no_fouls = rate * year_obj.no_foul_mean / TM

            boost = (teamYear.elo_start - 1500) * 0.001
            teamYear.ils_1 = team_ils_1[num] = max(-1 / 3, ils_1_seed + boost)
            teamYear.ils_2 = team_ils_2[num] = max(-1 / 3, ils_2_seed + boost)

            team_years[num] = teamYear
            team_oprs[num] = prior_opr

            temp += 1
            if temp % 1000 == 0:
                SQL_Write.add()

        team_events = defaultdict(list)
        events = sorted(SQL_Read.getEvents(year=year))
        for event in events:
            for team_event in event.team_events:
                num = team_event.team_id
                if num in teams:
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

            quals = sorted(SQL_Read.getMatches(event=event.id, playoff=False))
            playoffs = sorted(SQL_Read.getMatches(event=event.id, playoff=True))
            oprs, ils, team_ils_1, team_ils_2, stats = process_event(
                event, quals, playoffs, year, sd_score, team_ils_1, team_ils_2
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

            for team_event in event.team_events:
                num = team_event.team_id
                if num not in oprs:
                    continue

                opr = clean(oprs[num][-1][0])
                ils_1 = clean(ils[num][-1][0])
                ils_2 = clean(ils[num][-1][1])

                event_dict = {
                    "opr_end": opr,
                    "opr_auto": clean(oprs[num][-1][1]),
                    "opr_teleop": clean(oprs[num][-1][2]),
                    "opr_1": clean(oprs[num][-1][3]),
                    "opr_2": clean(oprs[num][-1][4]),
                    "opr_endgame": clean(oprs[num][-1][5]),
                    "opr_fouls": clean(oprs[num][-1][6]),
                    "opr_no_fouls": clean(oprs[num][-1][7]),
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
                team_events[num].append(event_dict)

                team_oprs[num] = opr
                team_ils_1[num] = ils_1
                team_ils_2[num] = ils_2

                for i, m in enumerate(sorted(team_event.team_matches)):
                    index = -1 if m.match.playoff else i
                    m.opr_score = clean(oprs[num][index][0])
                    m.opr_auto = clean(oprs[num][index][1])
                    m.opr_teleop = clean(oprs[num][index][2])
                    m.opr_1 = clean(oprs[num][index][3])
                    m.opr_2 = clean(oprs[num][index][4])
                    m.opr_endgame = clean(oprs[num][index][5])
                    m.opr_fouls = clean(oprs[num][index][6])
                    m.opr_no_fouls = clean(oprs[num][index][7])
                    m.ils_1 = clean(ils[num][index][0])
                    m.ils_2 = clean(ils[num][index][1])

            oprs_end = sorted([clean(oprs[t][-1][0]) for t in oprs], reverse=True)
            event.opr_max = oprs_end[0]
            event.opr_top8 = -1 if len(oprs_end) < 8 else oprs_end[7]
            event.opr_top24 = -1 if len(oprs_end) < 24 else oprs_end[23]
            event.opr_mean = round(sum(oprs_end) / len(oprs_end), 2)
            event.opr_sd = round(statistics.pstdev(oprs_end), 2)

            SQL_Write.add()

        oprs = []
        for num in team_years:
            # 1771 in 2004 only played in elims shrug
            if num not in team_events:
                continue
            best_event = sorted(team_events[num], key=lambda e: e["opr_end"])[-1]
            team_years[num].opr_end = best_event["opr_end"]
            team_years[num].opr_auto = best_event["opr_auto"]
            team_years[num].opr_teleop = best_event["opr_teleop"]
            team_years[num].opr_1 = best_event["opr_1"]
            team_years[num].opr_2 = best_event["opr_2"]
            team_years[num].opr_endgame = best_event["opr_endgame"]
            team_years[num].opr_fouls = best_event["opr_fouls"]
            team_years[num].opr_no_fouls = best_event["opr_no_fouls"]
            team_years[num].ils_1 = team_ils_1[num]
            team_years[num].ils_2 = team_ils_2[num]
            oprs.append(best_event["opr_end"])

        team_years_all[year] = team_years
        # keeps memory down
        if year - 2 in team_years_all:
            team_years_all.pop(year - 2)

        oprs.sort(reverse=True)
        year_obj = SQL_Read.getYear(year=year)
        year_obj.opr_max = oprs[0]
        year_obj.opr_1p = oprs[round(0.01 * len(oprs))]
        year_obj.opr_5p = oprs[round(0.05 * len(oprs))]
        year_obj.opr_10p = oprs[round(0.10 * len(oprs))]
        year_obj.opr_25p = oprs[round(0.25 * len(oprs))]
        year_obj.opr_median = oprs[round(0.50 * len(oprs))]
        year_obj.opr_mean = round(sum(oprs) / len(oprs), 2)
        year_obj.opr_sd = round(statistics.pstdev(oprs), 2)

        year_obj.opr_acc = round(opr_acc / count, 4)
        year_obj.opr_mse = round(opr_mse / count, 4)
        year_obj.mix_acc = round(mix_acc / count, 4)
        year_obj.mix_mse = round(mix_mse / count, 4)
        year_obj.rp1_acc = -1 if year < 2016 else round(rp1_acc / count_rp, 4)
        year_obj.rp1_mse = -1 if year < 2016 else round(rp1_mse / count_rp, 4)
        year_obj.rp2_acc = -1 if year < 2016 else round(rp2_acc / count_rp, 4)
        year_obj.rp2_mse = -1 if year < 2016 else round(rp2_mse / count_rp, 4)

        # for faster feedback, could be removed
        SQL_Write.commit()
        printStats(SQL_Write=SQL_Write, SQL_Read=SQL_Read)

    SQL_Write.commit()
    printStats(SQL_Write=SQL_Write, SQL_Read=SQL_Read)


def test(start_year, end_year, SQL_Read, SQL_Write):
    event = SQL_Read.getEvent_byKey("2002ca")
    oprs = opr_model.get_OPR(event)
    for team in oprs:
        print(team, oprs[team][-1])


def main(start_year, end_year, TBA, SQL_Write, SQL_Read, clean):
    process(start_year, end_year, SQL_Read, SQL_Write)
    # test(start_year, end_year, SQL_Read, SQL_Write)
    printStats(SQL_Write=SQL_Write, SQL_Read=SQL_Read)
