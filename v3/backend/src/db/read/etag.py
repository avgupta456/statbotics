from typing import List, Optional

from sqlalchemy.orm.session import Session as SessionType
from sqlalchemy_cockroachdb import run_transaction  # type: ignore

from src.db.main import Session
from src.db.models.etag import ETag, ETagORM


def get_etags(year: Optional[int] = None, path: Optional[str] = None) -> List[ETag]:
    def callback(session: SessionType):
        data = session.query(ETagORM)
        if year is not None:
            data = data.filter(ETagORM.year == year)
        if path is not None:
            data = data.filter(ETagORM.path == path)
        out_data: List[ETagORM] = data.all()
        return [ETag.from_dict(x.__dict__) for x in out_data]

    return run_transaction(Session, callback)  # type: ignore


def get_num_etags() -> int:
    def callback(session: SessionType) -> int:
        return session.query(ETagORM).count()

    return run_transaction(Session, callback)  # type: ignore
