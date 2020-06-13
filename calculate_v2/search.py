from classes import (
    sql,
    read,
)

SQL = sql.SQL(clean=False)
SQL_Read = read.SQL_Read(SQL)

print(SQL_Read.getTeam(254).getName())
