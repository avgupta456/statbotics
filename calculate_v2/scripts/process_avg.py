import statistics

from scripts.logging import printStats


def process(start_year, end_year, SQL_Write, SQL_Read):
    for year in range(start_year, end_year + 1):
        year_obj = SQL_Read.getYear(year)
        matches = []
        for event in SQL_Read.getEvents(year=year, week=1):
            matches.extend(event.matches)
        matches = sorted(matches)
        scores, autos, teleop1s, teleop2s, teleop21s, \
            teleop22s, teleop23s, endgames, fouls, no_fouls \
            = [], [], [], [], [], [], [], [], [], []
        for match in matches:
            scores.extend([match.red_score, match.blue_score])
            autos.extend([match.red_auto, match.blue_auto])
            teleop1s.extend([match.red_teleop_1, match.blue_teleop_1])
            teleop2s.extend([match.red_teleop_2, match.blue_teleop_2])
            teleop21s.extend([match.red_teleop_2_1, match.blue_teleop_2_1])
            teleop22s.extend([match.red_teleop_2_2, match.blue_teleop_2_2])
            teleop23s.extend([match.red_teleop_2_3, match.blue_teleop_2_3])
            endgames.extend([match.red_endgame, match.blue_endgame])
            fouls.extend([match.red_fouls, match.blue_fouls])
            no_fouls.extend([match.red_no_fouls, match.blue_no_fouls])

        year_obj.score_mean = round(sum(scores)/len(scores), 2)
        year_obj.score_sd = round(statistics.pstdev(scores), 2)
        year_obj.auto_mean = round(sum(autos)/len(autos), 2)
        year_obj.teleop1_mean = round(sum(teleop1s)/len(teleop1s), 2)
        year_obj.teleop2_mean = round(sum(teleop2s)/len(teleop2s), 2)
        year_obj.teleop21_mean = round(sum(teleop21s)/len(teleop21s), 2)
        year_obj.teleop22_mean = round(sum(teleop22s)/len(teleop22s), 2)
        year_obj.teleop23_mean = round(sum(teleop23s)/len(teleop23s), 2)
        year_obj.endgame_mean = round(sum(endgames)/len(endgames), 2)
        year_obj.foul_mean = round(sum(fouls)/len(fouls), 2)
        year_obj.no_foul_mean = round(sum(no_fouls)/len(no_fouls), 2)
        print(year, len(matches))
        SQL_Write.commit()


def test(start_year, end_year, SQL_Write, SQL_Read):
    return


def main(start_year, end_year, TBA, SQL_Write, SQL_Read, clean):
    process(start_year, end_year, SQL_Write, SQL_Read)
    test(start_year, end_year, SQL_Write, SQL_Read)
    printStats(SQL_Write=SQL_Write, SQL_Read=SQL_Read)
