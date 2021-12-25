from typing import Any, Callable, Dict, List, Type

import attr

from sqlalchemy.dialects import postgresql
from sqlalchemy.orm.session import Session as SessionType
from sqlalchemy_cockroachdb import run_transaction  # type: ignore

from db.main import Session
from db.models.main import TModel, TModelORM


CUTOFF = 1000

"""
def update_template(
    orm_type: Type[TModelORM], obj_type: Type[TModel]
) -> Callable[[List[TModel], bool], None]:
    def _update(session: SessionType, data: List[Dict[str, Any]]):
        for i in range(0, len(data), CUTOFF):
            session.bulk_update_mappings(orm_type, data[i : i + CUTOFF])  # type: ignore

    def _insert(session: SessionType, data: List[Dict[str, Any]]):
        for i in range(0, len(data), CUTOFF):
            session.bulk_insert_mappings(orm_type, data[i : i + CUTOFF])  # type: ignore

    def update(items: List[obj_type], insert_only: bool = False) -> None:
        def callback(session: SessionType):
            if insert_only:
                return _insert(session, [x.__dict__ for x in items])  # type: ignore

            ids: List[int] = [item.id for item in items]  # type: ignore
            curr_ids: List[int] = [
                x[0] for x in session.query(orm_type.id).filter(orm_type.id.in_(ids)).all()  # type: ignore
            ]
            existing_ids = set(ids).intersection(set(curr_ids))
            if len(existing_ids) > 0:
                _update(session, [x.__dict__ for x in items if x.id in existing_ids])  # type: ignore
            if len(existing_ids) < len(ids):
                _insert(session, [x.__dict__ for x in items if x.id not in existing_ids])  # type: ignore

        run_transaction(Session, callback)

    return update
"""


def update_template(
    orm_type: Type[TModelORM], obj_type: Type[TModel]
) -> Callable[[List[TModel], bool], None]:
    def upsert(items: List[obj_type], insert_only: bool = False) -> None:
        def _insert(session: SessionType, data: List[Dict[str, Any]]):
            for i in range(0, len(data), CUTOFF):
                session.bulk_insert_mappings(orm_type, data[i : i + CUTOFF])  # type: ignore

        def _update(session: SessionType, data: List[Dict[str, Any]]):
            for i in range(0, len(data), CUTOFF):
                insert = postgresql.insert(orm_type.__table__).values(data[i : i + CUTOFF])  # type: ignore
                update_cols = {col.name: col for col in insert.excluded if col.name != "id"}  # type: ignore
                update = insert.on_conflict_do_update(index_elements=["id"], set_=update_cols)  # type: ignore
                session.execute(update.execution_options(synchronize_session=False))  # type: ignore

        def callback(session: SessionType):
            new_items = [attr.asdict(x) for x in items]

            if insert_only:
                return _insert(session, new_items)  # type: ignore
            return _update(session, new_items)  # type: ignore

        run_transaction(Session, callback)

    return upsert
