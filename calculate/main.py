from helper import setup

from process import (
    process_tba,
    process_avg,
    process_elo,
    process_opr,
    process_push
)

start_year = 2002
end_year = 2020
clean = False
cache = True

TBA, SQL, SQL_Read, SQL_Write = setup.setup(clean)
# process_tba.main(start_year, end_year, TBA, SQL_Write, SQL_Read, clean, cache) # 16 minutes  # noqa 502
# process_avg.main(start_year, end_year, TBA, SQL_Write, SQL_Read, clean) # 5 seconds  # noqa 502
# process_elo.main(start_year, end_year, TBA, SQL_Write, SQL_Read, clean) # 16 minutes  # noqa 502
# process_opr.main(start_year, end_year, TBA, SQL_Write, SQL_Read, clean) # 18 minutes  # noqa 502
process_push.main(SQL, SQL_Read)  # 10 minutes
