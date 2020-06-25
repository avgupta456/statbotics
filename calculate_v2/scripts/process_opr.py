import statistics

from scripts.logging import printStats
from models import opr as opr_model


def process_event(event, quals, playoffs, year, sd_score):
    test = opr_model.opr_v2(event, quals, playoffs)
    oprs = opr_model.opr_v1(event, quals, playoffs)

    opr_acc, opr_mse, mix_acc, mix_mse, count = 0, 0, 0, 0, 0
    for i, m in enumerate(sorted(quals+playoffs)):
        red, blue = m.getRed(), m.getBlue()
        red_oprs, blue_oprs = [], []
        ind = -1 if m.playoff == 1 else i

        for r in red:
            opr = 0 if r not in oprs else oprs[r][ind][0]
            red_oprs.append(opr)
        for b in blue:
            opr = 0 if b not in oprs else oprs[b][ind][0]
            blue_oprs.append(opr)

        m.setRedOpr(red_oprs)
        m.setBlueOpr(blue_oprs)

        win_probs = {"red": 1, "blue": 0, "draw": 0.5}
        red_sum, blue_sum = sum(red_oprs), sum(blue_oprs)
        m.opr_winner = "red" if red_sum > blue_sum else "blue"
        m.opr_win_prob = opr_model.win_prob(red_sum, blue_sum, year, sd_score)
        opr_mse += (win_probs[m.winner] - m.opr_win_prob) ** 2
        if m.opr_winner == m.winner:
            opr_acc += 1

        m.mix_win_prob = 0.5 * (m.elo_win_prob+m.opr_win_prob)
        m.mix_winner = "red" if m.mix_win_prob > 0.5 else "blue"
        mix_mse += (win_probs[m.winner] - m.mix_win_prob) ** 2
        if m.winner == m.mix_winner:
            mix_acc += 1

        count += 1

    stats = [opr_acc, opr_mse, mix_acc, mix_mse, count]
    return test, oprs, stats


def process(start_year, end_year, SQL_Read, SQL_Write):
    teams, means = {}, {}
    for team in SQL_Read.getTeams():
        teams[team.getNumber()] = team

    team_years_all = {}  # master dict
    for year in range(start_year, end_year + 1):
        print(year)
        year_obj = SQL_Read.getYear(year)
        sd_score = year_obj.score_sd

        team_years, team_oprs = {}, {}
        opr_acc, opr_mse, mix_acc, mix_mse, count = 0, 0, 0, 0, 0

        # populate starting elo from previous year
        mean_score = year_obj.score_mean
        prior_opr_global = mean_score / 3
        means[year] = mean_score
        for teamYear in SQL_Read.getTeamYears(year=year):
            num = teamYear.getTeam()
            prior_opr = prior_opr_global
            if year-1 in team_years_all and \
                    num in team_years_all[year-1] and \
                    team_years_all[year-1][num].opr_end is not None:
                prior_opr = team_years_all[year-1][num].opr_end
                prior_opr = prior_opr/means[year-1]*mean_score
                prior_opr = 0.90 * prior_opr + 0.10 * prior_opr_global
            teamYear.opr_start = prior_opr

            rate = prior_opr/prior_opr_global
            TM = 2 if year <= 2004 else 3
            teamYear.opr_auto = rate * year_obj.auto_mean/TM
            teamYear.opr_teleop = rate * year_obj.teleop_mean/TM
            teamYear.opr_1 = rate * year_obj.one_mean/TM
            teamYear.opr_2 = rate * year_obj.two_mean/TM
            teamYear.opr_endgame = rate * year_obj.endgame_mean/TM
            teamYear.opr_fouls = year_obj.foul_mean/TM  # no rate
            teamYear.opr_no_fouls = rate * year_obj.no_foul_mean/TM

            team_years[num] = teamYear
            team_oprs[num] = prior_opr

        team_events = {}
        events = sorted(SQL_Read.getEvents(year=year))
        for event in events:
            for team_event in event.team_events:
                num = team_event.getTeam()
                if num in teams:
                    team_event.opr_start = team_oprs[num]
                    team_event.opr_auto = team_years[num].opr_auto
                    team_event.opr_teleop = team_years[num].opr_teleop
                    team_event.opr_1 = team_years[num].opr_1
                    team_event.opr_2 = team_years[num].opr_2
                    team_event.opr_endgame = team_years[num].opr_endgame
                    team_event.opr_fouls = team_years[num].opr_fouls
                    team_event.opr_no_fouls = team_years[num].opr_no_fouls

            quals = sorted(SQL_Read.getMatches(event=event.getId(), playoff=False))  # noqa 502
            playoffs = sorted(SQL_Read.getMatches(event=event.getId(), playoff=True))  # noqa 502
            oprs, stats = process_event(event, quals, playoffs, year, sd_score)
            opr_acc += stats[0]
            opr_mse += stats[1]
            mix_acc += stats[2]
            mix_mse += stats[3]
            count += stats[4]

            for team_event in event.team_events:
                num = team_event.getTeam()
                if num not in oprs:
                    continue

                if year < 2016:
                    team_event.opr_auto = team_years[num].opr_auto = oprs[num][-1][1]  # noqa 502
                    team_event.opr_teleop = team_years[num].opr_teleop = oprs[num][-1][2]  # noqa 502
                    team_event.opr_1 = team_years[num].opr_1 = oprs[num][-1][3]
                    team_event.opr_2 = team_years[num].opr_2 = oprs[num][-1][4]
                    team_event.opr_endgame = team_years[num].opr_endgame = oprs[num][-1][5]  # noqa 502
                    team_event.opr_fouls = team_years[num].opr_fouls = oprs[num][-1][6]  # noqa 502
                    team_event.opr_no_fouls = team_years[num].opr_no_fouls = oprs[num][-1][7]  # noqa 502
                else:
                    team_event.opr_auto = team_years[num].opr_auto = -1
                    team_event.opr_teleop = team_years[num].opr_teleop = -1
                    team_event.opr_1 = team_years[num].opr_1 = -1
                    team_event.opr_2 = team_years[num].opr_2 = -1
                    team_event.opr_endgame = team_years[num].opr_endgame = -1
                    team_event.opr_fouls = team_years[num].opr_fouls = -1
                    team_event.opr_no_fouls = team_years[num].opr_no_fouls = -1

                opr = oprs[num][-1][0]
                team_event.opr_end = opr
                team_oprs[num] = opr
                if num not in team_events:
                    team_events[num] = []
                team_events[num].append(opr)

            oprs_end = sorted([oprs[t][-1][0] for t in oprs], reverse=True)
            event.opr_max = oprs_end[0]
            event.opr_top8 = -1 if len(oprs_end) < 8 else oprs_end[7]
            event.opr_top24 = -1 if len(oprs_end) < 24 else oprs_end[23]
            event.opr_mean = round(sum(oprs_end)/len(oprs_end), 2)
            event.opr_sd = round(statistics.pstdev(oprs_end), 2)

        oprs = []
        for num in team_years:
            # 1771 in 2004 only played in elims shrug
            if num not in team_events:
                continue
            team_years[num].opr_end = team_events[num][-1]
            oprs.append(max(team_events[num]))
        team_years_all[year] = team_years

        oprs.sort(reverse=True)
        year_obj = SQL_Read.getYear(year=year)
        year_obj.opr_max = oprs[0]
        year_obj.opr_1p = oprs[round(0.01*len(oprs))]
        year_obj.opr_5p = oprs[round(0.05*len(oprs))]
        year_obj.opr_10p = oprs[round(0.10*len(oprs))]
        year_obj.opr_25p = oprs[round(0.25*len(oprs))]
        year_obj.opr_median = oprs[round(0.50*len(oprs))]
        year_obj.opr_mean = round(sum(oprs)/len(oprs), 2)
        year_obj.opr_sd = round(statistics.pstdev(oprs), 2)

        year_obj.opr_acc = round(opr_acc/count, 4)
        year_obj.opr_mse = round(opr_mse/count, 4)
        year_obj.mix_acc = round(mix_acc/count, 4)
        year_obj.mix_mse = round(mix_mse/count, 4)

        # for faster feedback, could be removed
        # SQL_Write.commit()
        printStats(SQL_Write=SQL_Write, SQL_Read=SQL_Read)

    # SQL_Write.commit()
    printStats(SQL_Write=SQL_Write, SQL_Read=SQL_Read)


def test(start_year, end_year, SQL_Read, SQL_Write):
    event = SQL_Read.getEvent_byKey('2002ca')
    oprs = opr_model.get_OPR(event)
    for team in oprs:
        print(team, oprs[team][-1])


def main(start_year, end_year, TBA, SQL_Write, SQL_Read, clean):
    process(start_year, end_year, SQL_Read, SQL_Write)
    # test(start_year, end_year, SQL_Read, SQL_Write)
    printStats(SQL_Write=SQL_Write, SQL_Read=SQL_Read)
