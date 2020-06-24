from classes import (
    sql,
    read,
    write
)

from tba import (
    read_tba,
)

from scripts import (
    process_tba,
    process_avg,
    process_elo,
    process_opr,
    search,
)

start_year = 2002
end_year = 2020
clean = False

TBA = read_tba.ReadTBA()
SQL = sql.SQL(clean=clean, echo=False)
SQL_Read = read.SQL_Read(SQL)
SQL_Write = write.SQL_Write(SQL, SQL_Read)

# process_tba.main(start_year, end_year, TBA, SQL_Write, SQL_Read, clean=clean)
# process_avg.main(start_year, end_year, TBA, SQL_Write, SQL_Read, clean=clean)
# process_elo.main(start_year, end_year, TBA, SQL_Write, SQL_Read, clean)
# process_opr.main(start_year, end_year, TBA, SQL_Write, SQL_Read, clean)
search.search(SQL_Read)
