import statistics

from scripts.logging import printStats
from helper import constants
from opr import opr


def process_opr(start_year, end_year, SQL_Read, SQL_Write):
    teams = {}
    for team in SQL_Read.getTeams():
        teams[team.getNumber()] = team

    team_years_all = {}
    for year in range(start_year, end_year + 1):
        print(year)
        team_years = {}
        team_oprs = {}
        mean_score = constants.mean[year]
        prior_opr_global = mean_score / 3
        for teamYear in SQL_Read.getTeamYears(year=year):
            num = teamYear.getTeam()
            prior_opr = prior_opr_global
            if year-1 in team_years_all and \
                    num in team_years_all[year-1] and \
                    team_years_all[year-1][num].opr_end is not None:
                prior_opr = team_years_all[year-1][num].opr_end
                prior_opr = prior_opr/constants.mean[year-1]*mean_score
                prior_opr = 0.90 * prior_opr + 0.10 * prior_opr_global
            teamYear.opr_start = prior_opr
            team_years[num] = teamYear
            team_oprs[num] = prior_opr

        team_events = {}
        events = SQL_Read.getEvents(year=year)
        for event in events:
            matches = len(event.getMatches(playoffs=False))
            if matches == 0:
                for team_event in event.team_events:
                    num = team_event.getTeam()
                    team_event.opr_start = team_oprs[num]
                    team_event.opr_end = team_oprs[num]
            else:
                teams, oprs = opr.getOPR(event), []
                for team_event in event.team_events:
                    num = team_event.getTeam()
                    if num not in teams:
                        continue
                    team_opr = teams[num]
                    team_event.opr_start = team_oprs[num]
                    team_event.opr_end = team_opr
                    team_oprs[num] = team_opr
                    oprs.append(teams[num])
                    if num not in team_events:
                        team_events[num] = []
                    team_events[num].append(team_opr)

                oprs.sort(reverse=True)
                event.opr_max = oprs[0]
                event.opr_top8 = -1 if len(oprs) < 8 else oprs[7]
                event.opr_top24 = -1 if len(oprs) < 24 else oprs[23]
                event.opr_mean = round(sum(oprs)/len(oprs), 2)
                event.opr_sd = round(statistics.pstdev(oprs), 2)

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

        # for faster feedback, could be removed
        SQL_Write.commit()
    SQL_Write.commit()


def test(start_year, end_year, SQL_Read, SQL_Write):
    event = SQL_Read.getEvent_byKey('2019gal')
    oprs = sorted(opr.getOPR(event).items(), key=lambda x: x[1], reverse=True)
    for (num, team_opr) in oprs:
        print(str(num)+"\t"+str(team_opr))


def main(start_year, end_year, SQL_Write, SQL_Read):
    process_opr(start_year, end_year, SQL_Read, SQL_Write)
    test(start_year, end_year, SQL_Read, SQL_Write)
    printStats(SQL_Write=SQL_Write, SQL_Read=SQL_Read)
