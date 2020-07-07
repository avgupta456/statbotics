from classes import sql, read, write
from tba import read_tba


def setup(clean=False):
    TBA = read_tba.ReadTBA()
    SQL = sql.SQL(clean=clean, echo=False, local=True, cloud=False)
    SQL_Read = read.SQL_Read(SQL, cloud=False)
    SQL_Write = write.SQL_Write(SQL, SQL_Read, cloud=False)
    return TBA, SQL, SQL_Read, SQL_Write


def setup_cloud(clean=False):
    TBA = read_tba.ReadTBA()
    SQL = sql.SQL(clean=clean, echo=False, local=False, cloud=True)
    SQL_Read = read.SQL_Read(SQL, cloud=True)
    SQL_Write = write.SQL_Write(SQL, SQL_Read, cloud=True)
    return TBA, SQL, SQL_Read, SQL_Write


def getSQL_Read():
    return read.SQL_Read(sql.SQL(clean=False, echo=False))
