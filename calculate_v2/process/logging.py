import datetime

start = datetime.datetime.now()


def printStats(TBA=None, SQL_Write=None, SQL_Read=None, print_sql=False):
    print()

    if TBA is not None:
        print("TBA Calls: " + str(TBA.getStats()[0]))
        print("TBA Cache: " + str(TBA.getStats()[1]))
        print()

    if SQL_Write is not None:
        print("SQL Writes: " + str(SQL_Write.getStats()[0]))
        print("SQL Commits: " + str(SQL_Write.getStats()[1]))

    if SQL_Read is not None:
        print("SQL Reads: " + str(SQL_Read.getStats()))

    if SQL_Write is not None or SQL_Read is not None:
        print()

    if print_sql:
        print("Total Teams: " + str(SQL_Read.getTotalTeams()))
        print("Total Years: " + str(SQL_Read.getTotalYears()))
        print("Total TeamYears: " + str(SQL_Read.getTotalTeamYears()))
        print("Total Events: " + str(SQL_Read.getTotalEvents()))
        print("Total TeamEvents: " + str(SQL_Read.getTotalTeamEvents()))
        print("Total Matches: " + str(SQL_Read.getTotalMatches()))
        print("Total TeamMatches: " + str(SQL_Read.getTotalTeamMatches()))
        print()

    print("Time Elapsed: " + str(datetime.datetime.now()-start))
    print()
