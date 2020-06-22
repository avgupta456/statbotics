import statistics

from scripts.logging import printStats
from models import opr as opr_model


def process_event(event, year, sd_score):
    oprs = opr_model.get_ixOPR(event)
    opr_acc, opr_mse, mix_acc, mix_mse, count = 0, 0, 0, 0, 0
    for i, m in enumerate(sorted(event.matches)):
        red, blue = m.getRed(), m.getBlue()
        red_oprs, blue_oprs = [], []
        ind = -1 if m.playoff else i-1
        # print(oprs)
        for r in red:
            opr = 0 if r not in oprs or ind >= len(oprs[r]) else oprs[r][ind]
            red_oprs.append(opr)
        for b in blue:
            opr = 0 if b not in oprs or ind >= len(oprs[r]) else oprs[b][ind]
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
    return oprs, stats


def process(start_year, end_year, SQL_Read, SQL_Write):
    teams, means = {}, {}
    for team in SQL_Read.getTeams():
        teams[team.getNumber()] = team

    team_years_all = {}  # master dict
    for year in range(start_year, end_year + 1):
        print(year)
        year_obj = SQL_Read.getYear(year)
        sd_score, mean_score = year_obj.score_sd, year_obj.score_mean
        means[year] = mean_score

        team_years, team_oprs = {}, {}
        opr_acc, opr_mse, mix_acc, mix_mse, count = 0, 0, 0, 0, 0

        # populate starting elo from previous year
        prior_opr_global = mean_score / 3
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
            team_years[num] = teamYear
            team_oprs[num] = prior_opr

        team_events = {}
        events = sorted(SQL_Read.getEvents(year=year))
        for event in events:
            print(event)
            for team_event in event.team_events:
                num = team_event.getTeam()
                if num in teams:
                    team_event.opr_start = team_oprs[num]

            oprs, stats = process_event(event, year, sd_score)
            opr_acc += stats[0]
            opr_mse += stats[1]
            mix_acc += stats[2]
            mix_mse += stats[3]
            count += stats[4]

            for team_event in event.team_events:
                num = team_event.getTeam()
                # 832 2004va didn't play matches
                if num not in oprs:
                    continue
                opr = oprs[num][-1]
                team_event.opr_end = opr
                team_oprs[num] = opr
                if num not in team_events:
                    team_events[num] = []
                team_events[num].append(opr)

            oprs_end = sorted([oprs[t][-1] for t in oprs], reverse=True)
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
        SQL_Write.commit()
    SQL_Write.commit()


def test(start_year, end_year, SQL_Read, SQL_Write):
    event = SQL_Read.getEvent_byKey('2002ca')
    oprs = opr_model.get_OPR(event)
    for team in oprs:
        print(team, oprs[team][-1])


def main(start_year, end_year, TBA, SQL_Write, SQL_Read, clean):
    process(start_year, end_year, SQL_Read, SQL_Write)
    # test(start_year, end_year, SQL_Read, SQL_Write)
    printStats(SQL_Write=SQL_Write, SQL_Read=SQL_Read)
