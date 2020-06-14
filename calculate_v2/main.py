from classes import (
    sql,
    read,
    write
)

from tba import (
    read_tba,
)

import process
import search

# possible stack overflow, do in chunks
# recommend 2002 - 2015, 2016 - 2020
start_year = 2002
end_year = 2020
clean = False

TBA = read_tba.ReadTBA()
SQL = sql.SQL(clean=clean, echo=False)
SQL_Read = read.SQL_Read(SQL)
SQL_Write = write.SQL_Write(SQL, SQL_Read)

process.process(start_year, end_year, TBA, SQL_Write, SQL_Read, clean=clean)
process.post_process(TBA, SQL_Write, SQL_Read)
search.search(SQL_Read)
