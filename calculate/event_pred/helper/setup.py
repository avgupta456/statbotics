from event_pred.classes import sql, read


def setup(clean=False):
    SQL = sql.SQL(clean=clean, echo=False, local=True, cloud=False)
    SQL_Read = read.SQL_Read(SQL, cloud=False)
    return SQL, SQL_Read


def setup_cloud(clean=False):
    SQL = sql.SQL(clean=clean, echo=False, local=False, cloud=True)
    SQL_Read = read.SQL_Read(SQL, cloud=True)
    return SQL, SQL_Read
