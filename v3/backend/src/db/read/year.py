from typing import List, Optional

from sqlalchemy.orm.session import Session as SessionType  # type: ignore
from sqlalchemy_cockroachdb import run_transaction  # type: ignore

from src.db.main import Session
from src.db.models.year import Year, YearORM


def get_year(year: int) -> Optional[Year]:
    def callback(session: SessionType):
        data = session.query(YearORM).filter(YearORM.year == year).first()  # type: ignore
        if data is None:
            return None
        return Year.from_dict(data.__dict__)  # type: ignore

    return run_transaction(Session, callback)  # type: ignore


def get_years(
    metric: Optional[str] = None,
    ascending: Optional[bool] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> List[Year]:
    def callback(session: SessionType):
        data = session.query(YearORM)  # type: ignore
        if metric is not None:
            data = data.filter(YearORM.__dict__[metric] != None)  # type: ignore  # noqa: E711
            if ascending is not None and ascending:
                data = data.order_by(YearORM.__dict__[metric].asc())  # type: ignore
            else:
                data = data.order_by(YearORM.__dict__[metric].desc())  # type: ignore
        if limit is not None:
            data = data.limit(limit)  # type: ignore
        if offset is not None:
            data = data.offset(offset)  # type: ignore
        out_data: List[YearORM] = data.all()  # type: ignore
        return [Year.from_dict(x.__dict__) for x in out_data]  # type: ignore

    return run_transaction(Session, callback)  # type: ignore


def get_num_years() -> int:
    def callback(session: SessionType) -> int:
        return session.query(YearORM).count()  # type: ignore

    return run_transaction(Session, callback)  # type: ignore
