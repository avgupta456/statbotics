import datetime

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

start = datetime.datetime.now()

start_year = 2002
end_year = 2005

TBA = read_tba.ReadTBA()
SQL = sql.SQL(clean=True)
SQL_Read = read.SQL_Read(SQL)
SQL_Write = write.SQL_Write(SQL)

process.process(start_year, end_year, TBA, SQL_Write)
search.search(SQL_Read)

end = datetime.datetime.now()
print("\nLog Time: " + str(end-start))
