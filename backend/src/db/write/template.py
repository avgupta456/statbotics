from typing import Any, Callable, Dict, List, Tuple, Type

import attr
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm.session import Session as SessionType
from sqlalchemy_cockroachdb import run_transaction  # type: ignore

from src.db.main import Session
from src.db.models.etag import ETagORM
from src.db.models.event import EventORM
from src.db.models.main import TModel, TModelORM
from src.db.models.match import MatchORM
from src.db.models.team import TeamORM
from src.db.models.team_event import TeamEventORM
from src.db.models.team_year import TeamYearORM
from src.db.models.year import YearORM

CUTOFF = 1000


def _primary_key(orm_type: Type[TModelORM]) -> List[str]:
    if orm_type == ETagORM:
        return ["path"]
    elif orm_type == TeamORM:
        return ["team"]
    elif orm_type == YearORM:
        return ["year"]
    elif orm_type == TeamYearORM:
        return ["team", "year"]
    elif orm_type == EventORM:
        return ["key"]
    elif orm_type == TeamEventORM:
        return ["team", "event"]
    elif orm_type == MatchORM:
        return ["key"]
    else:
        raise Exception("Unknown orm_type: " + str(orm_type))


def _insert(session: SessionType, orm_type: Type[TModelORM], data: List[Dict[str, Any]]) -> None:
    for i in range(0, len(data), CUTOFF):
        session.bulk_insert_mappings(orm_type, data[i : i + CUTOFF])  # type: ignore


def _update(session: SessionType, orm_type: Type[TModelORM], primary_key: List[str], data: List[Dict[str, Any]]) -> None:
    for i in range(0, len(data), CUTOFF):
        insert = postgresql.insert(orm_type.__table__).values(data[i : i + CUTOFF])
        update_cols = {c.name: c for c in insert.excluded if c.name not in primary_key}
        update = insert.on_conflict_do_update(index_elements=primary_key, set_=update_cols)
        session.execute(update.execution_options(synchronize_session=False))


def write_all(items: List[Tuple[Type[TModelORM], List[Any], bool]]) -> None:
    def callback(session: SessionType):
        for orm_type, objs, insert_only in items:
            if not objs:
                continue
            data = [attr.asdict(x) for x in objs]
            pk = _primary_key(orm_type)
            if insert_only:
                _insert(session, orm_type, data)
            else:
                _update(session, orm_type, pk, data)

    run_transaction(Session, callback)


def update_template(
    orm_type: Type[TModelORM], obj_type: Type[TModel]
) -> Callable[[List[TModel], bool], None]:
    def upsert(items: List[obj_type], insert_only: bool = False) -> None:  # type: ignore
        if not items:
            return
        write_all([(orm_type, items, insert_only)])

    return upsert
