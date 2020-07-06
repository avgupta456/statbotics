from classes import sql, read, write
from tba import read_tba


def setup(clean):
    TBA = read_tba.ReadTBA()
    SQL = sql.SQL(clean=clean, echo=False)
    SQL_Read = read.SQL_Read(SQL)
    SQL_Write = write.SQL_Write(SQL, SQL_Read)
    return TBA, SQL, SQL_Read, SQL_Write


def getSQL_Read():
    return read.SQL_Read(sql.SQL(clean=False, echo=False))
