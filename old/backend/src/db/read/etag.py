from typing import List, Optional

from sqlalchemy.orm.session import Session as SessionType  # type: ignore
from sqlalchemy_cockroachdb import run_transaction  # type: ignore

from src.db.main import Session
from src.db.models.etag import ETag, ETagORM


def get_etags(year: Optional[int] = None, path: Optional[str] = None) -> List[ETag]:
    def callback(session: SessionType):
        data = session.query(ETagORM)  # type: ignore
        if year is not None:
            data = data.filter(ETagORM.year == year)  # type: ignore
        if path is not None:
            data = data.filter(ETagORM.path == path)  # type: ignore
        out_data: List[ETagORM] = data.all()  # type: ignore
        return [ETag.from_dict(x.__dict__) for x in out_data]  # type: ignore

    return run_transaction(Session, callback)  # type: ignore


def get_num_etags() -> int:
    def callback(session: SessionType) -> int:
        return session.query(ETagORM).count()  # type: ignore

    return run_transaction(Session, callback)  # type: ignore
