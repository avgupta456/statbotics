import statistics

from process.logging import printStats


def process(start_year, end_year, SQL_Write, SQL_Read):
    for year in range(start_year, end_year + 1):
        year_obj = SQL_Read.getYear(year)
        matches = []
        for event in SQL_Read.getEvents(year=year, week=1):
            matches.extend(event.matches)
        matches = sorted(matches)

        scores, autos, teleops, ones, twos = [], [], [], [], []
        endgames, fouls, no_fouls, rp_1s, rp_2s = [], [], [], [], []

        for match in matches:
            scores.extend([match.red_score, match.blue_score])
            autos.extend([match.red_auto, match.blue_auto])
            teleops.extend([match.red_teleop, match.blue_teleop])
            ones.extend([match.red_1, match.blue_1])
            twos.extend([match.red_2, match.blue_2])
            endgames.extend([match.red_endgame, match.blue_endgame])
            fouls.extend([match.red_fouls, match.blue_fouls])
            no_fouls.extend([match.red_no_fouls, match.blue_no_fouls])
            rp_1s.extend([match.red_rp_1, match.blue_rp_1])
            rp_2s.extend([match.red_rp_2, match.blue_rp_2])

        year_obj.score_mean = round(sum(scores) / len(scores), 2)
        year_obj.score_sd = round(statistics.pstdev(scores), 2)
        year_obj.auto_mean = round(sum(autos) / len(autos), 2)
        year_obj.teleop_mean = round(sum(teleops) / len(teleops), 2)
        year_obj.one_mean = round(sum(ones) / len(ones), 2)
        year_obj.two_mean = round(sum(twos) / len(twos), 2)
        year_obj.endgame_mean = round(sum(endgames) / len(endgames), 2)
        year_obj.foul_mean = round(sum(fouls) / len(fouls), 2)
        year_obj.no_foul_mean = round(sum(no_fouls) / len(no_fouls), 2)
        year_obj.rp_1_mean = round(sum(rp_1s) / len(rp_1s), 4)
        year_obj.rp_2_mean = round(sum(rp_2s) / len(rp_2s), 4)
        print(year, len(matches))
        SQL_Write.commit()


def test(start_year, end_year, SQL_Write, SQL_Read):
    return


def main(start_year, end_year, TBA, SQL_Write, SQL_Read, clean):
    process(start_year, end_year, SQL_Write, SQL_Read)
    test(start_year, end_year, SQL_Write, SQL_Read)
    printStats(SQL_Write=SQL_Write, SQL_Read=SQL_Read)
