from classes import (
    sql,
    read,
    write
)

from tba import (
    read_tba,
)

from scripts import (
    process,
    process_elo,
    process_opr,
    search,
)

start_year = 2002
end_year = 2020
clean = True

TBA = read_tba.ReadTBA()
SQL = sql.SQL(clean=clean, echo=False)
SQL_Read = read.SQL_Read(SQL)
SQL_Write = write.SQL_Write(SQL, SQL_Read)

process.main(start_year, end_year, TBA, SQL_Write, SQL_Read, clean=clean)
# process_elo.main(start_year, end_year, SQL_Write, SQL_Read)
# process_opr.main(start_year, end_year, SQL_Write, SQL_Read)
search.search(SQL_Read)
