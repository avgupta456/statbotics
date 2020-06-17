from scripts.logging import printStats

from elo import elo


def process_elo(start_year, end_year, SQL_Write, SQL_Read):
    teams = {}
    for team in SQL_Read.getTeams():
        teams[team.getNumber()] = team

    start, mean_reversion = elo.start_rating(), elo.mean_reversion()

    team_years_all = {}
    for year in range(start_year, end_year + 1):
        print(year)
        team_years = {}
        team_matches = {}
        team_elos = {}
        for teamYear in SQL_Read.getTeamYears(year=year):
            num = teamYear.getTeam()
            team_years[num] = teamYear
            team_matches[num] = []
            elo_2yr = mean_reversion
            if year-2 in team_years_all and \
                    num in team_years_all[year-2] and \
                    team_years_all[year-2][num].elo_max is not None:
                elo_2yr = team_years_all[year-2][num].elo_max
            elo_1yr = mean_reversion
            if year-1 in team_years_all and \
                    num in team_years_all[year-1] and \
                    team_years_all[year-1][num].elo_max is not None:
                elo_1yr = team_years_all[year-1][num].elo_max
            start_rating = elo.existing_rating(elo_1yr, elo_2yr)
            team_elos[num] = start if year == 2002 else start_rating
            teamYear.elo_start = team_elos[num]
            # print(teamYear, teamYear.start_rating)
        matches = SQL_Read.getMatches_year(year=year)
        for match in matches:
            red, blue = match.getTeams()
            red_elo_pre = [team_elos[t] for t in red]
            blue_elo_pre = [team_elos[t] for t in blue]
            match.setRedEloPre(red_elo_pre)
            match.setBlueEloPre(blue_elo_pre)
            red_elo_post, blue_elo_post = elo.update_rating(
                year, red_elo_pre, blue_elo_pre, match.red_score,
                match.blue_score, match.playoff)
            match.setRedEloPost(red_elo_post)
            match.setBlueEloPost(blue_elo_post)
            for i in range(len(red)):
                team_elos[red[i]] = red_elo_post[i]
                team_matches[red[i]].append(red_elo_post[i])
            for i in range(len(blue)):
                team_elos[blue[i]] = blue_elo_post[i]
                team_matches[blue[i]].append(blue_elo_post[i])
            win_prob = elo.win_probability(red_elo_pre, blue_elo_pre)
            match.elo_win_prob = win_prob
            match.elo_winner = "Red" if win_prob > 0.5 else "Blue"
        for team in team_matches:
            elos = team_matches[team]
            if elos == []:
                SQL_Write.remove(team_years[team])
                team_years.pop(team)
            else:
                team_years[team].elo_max = max(elos[min(len(elos)-1, 8):])
                team_years[team].elo_mean = round(sum(elos)/len(elos), 3)
                team_years[team].elo_end = team_elos[team]
                team_years[team].elo_diff = team_years[team].elo_end \
                    - team_years[team].elo_start
        team_years_all[year] = team_years
    SQL_Write.commit()


def main(start_year, end_year, SQL_Write, SQL_Read):
    process_elo(start_year, end_year, SQL_Write, SQL_Read)
    printStats(SQL_Write=SQL_Write, SQL_Read=SQL_Read)
