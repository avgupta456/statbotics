from typing import List, Optional

from sqlalchemy.orm.session import Session as SessionType
from sqlalchemy_cockroachdb import run_transaction  # type: ignore

from src.db.main import Session
from src.db.models.year import Year, YearORM


def get_years(year: Optional[int] = None) -> List[Year]:
    def callback(session: SessionType):
        data = session.query(YearORM)  # type: ignore
        if year is not None:
            data = data.filter(YearORM.year == year)  # type: ignore
        data: List[YearORM] = data.all()  # type: ignore
        return [Year.from_dict(x.__dict__) for x in data]

    return run_transaction(Session, callback)  # type: ignore


def get_num_years() -> int:
    def callback(session: SessionType):
        return session.query(YearORM).count()  # type: ignore

    return run_transaction(Session, callback)  # type: ignore