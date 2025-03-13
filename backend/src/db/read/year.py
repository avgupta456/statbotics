from typing import List, Optional

from sqlalchemy.orm.session import Session as SessionType
from sqlalchemy_cockroachdb import run_transaction  # type: ignore

from src.db.main import Session
from src.db.models.year import Year, YearORM
from src.db.read.main import common_filters


def get_year(year: int) -> Optional[Year]:
    def callback(session: SessionType):
        data = session.query(YearORM).filter(YearORM.year == year).first()
        if data is None:
            return None
        return Year.from_dict(data.__dict__)

    return run_transaction(Session, callback)  # type: ignore


def get_years(
    metric: Optional[str] = None,
    ascending: Optional[bool] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> List[Year]:
    @common_filters(YearORM, Year, metric, ascending, limit, offset)
    def callback(session: SessionType):
        return session.query(YearORM)

    return run_transaction(Session, callback)  # type: ignore


def get_num_years() -> int:
    def callback(session: SessionType) -> int:
        return session.query(YearORM).count()

    return run_transaction(Session, callback)  # type: ignore
