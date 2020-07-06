from helper import setup

from process import (
    process_tba,
    process_avg,
    process_elo,
    process_opr,
)

from push import (
    clean as push_clean
)

start_year = 2002
end_year = 2020
clean = True
cache = True

TBA, SQL, SQL_Read, SQL_Write = setup.setup(clean)
process_tba.main(start_year, end_year, TBA, SQL_Write, SQL_Read, clean, cache) # 14 minutes  # noqa 502
process_avg.main(start_year, end_year, TBA, SQL_Write, SQL_Read, clean) # 7 seconds  # noqa 502
process_elo.main(start_year, end_year, TBA, SQL_Write, SQL_Read, clean) # ~30 minutes  # noqa 502
process_opr.main(start_year, end_year, TBA, SQL_Write, SQL_Read, clean)
push_clean.push()
