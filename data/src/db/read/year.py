from typing import List

from sqlalchemy.orm.session import Session as SessionType
from sqlalchemy_cockroachdb import run_transaction  # type: ignore

from db.main import Session
from db.models.year import Year, YearORM


def get_years() -> List[Year]:
    def callback(session: SessionType):
        data = session.query(YearORM).all()  # type: ignore
        return [Year.from_dict(x.__dict__) for x in data]

    return run_transaction(Session, callback)  # type: ignore


def get_num_years() -> int:
    def callback(session: SessionType):
        return session.query(YearORM).count()  # type: ignore

    return run_transaction(Session, callback)  # type: ignore
