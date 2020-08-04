from helper import setup
from process import process_avg, process_elo, process_opr, process_push, process_tba

start_year = 2002
end_year = 2020
clean = False
cache = True

TBA, SQL, SQL_Read, SQL_Write = setup.setup(clean)
# process_tba.main(start_year, end_year, TBA, SQL_Write, SQL_Read, clean, cache)  # 18 minutes
# process_avg.main(start_year, end_year, TBA, SQL_Write, SQL_Read, clean)  # 5 seconds
# process_elo.main(start_year, end_year, TBA, SQL_Write, SQL_Read, clean)  # 13 minutes
# process_opr.main(start_year, end_year, TBA, SQL_Write, SQL_Read, clean)  # 13 minutes
# process_push.main(SQL, SQL_Read)  # 14 minutes
