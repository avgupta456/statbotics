from scripts.logging import printStats
from helper import constants
from opr import opr


def process_opr(start_year, end_year, SQL_Write, SQL_Read):
    return


def test(SQL_Read):
    event = SQL_Read.getEvent_byKey('2020txpla')
    teams, oprs = opr.getOPR(event)
    for i in range(len(teams)):
        print(str(teams[i]) + "\t" + str(round(oprs[i][0]/constants.sd[2020], 2))
              + "\t" + str(event.getTeamEvent(teams[i]).elo_pre_playoffs))


def main(start_year, end_year, SQL_Write, SQL_Read):
    process_opr(start_year, end_year, SQL_Read, SQL_Write)
    test(SQL_Read)
    printStats(SQL_Write=SQL_Write, SQL_Read=SQL_Read)
