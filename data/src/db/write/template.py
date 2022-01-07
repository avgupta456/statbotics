from typing import Any, Callable, Dict, List, Type

import attr

from sqlalchemy.dialects import postgresql
from sqlalchemy.orm.session import Session as SessionType
from sqlalchemy_cockroachdb import run_transaction  # type: ignore

from db.main import Session
from db.models.main import TModel, TModelORM
from db.models.team import TeamORM
from db.models.year import YearORM


CUTOFF = 1000


def update_template(
    orm_type: Type[TModelORM], obj_type: Type[TModel]
) -> Callable[[List[TModel], bool], None]:
    def upsert(items: List[obj_type], insert_only: bool = False) -> None:
        def _insert(session: SessionType, data: List[Dict[str, Any]]):
            for i in range(0, len(data), CUTOFF):
                session.bulk_insert_mappings(orm_type, data[i : i + CUTOFF])  # type: ignore

        def _update(session: SessionType, primary_key: str, data: List[Dict[str, Any]]):
            for i in range(0, len(data), CUTOFF):
                insert = postgresql.insert(orm_type.__table__).values(data[i : i + CUTOFF])  # type: ignore
                update_cols = {col.name: col for col in insert.excluded if col.name != primary_key}  # type: ignore
                update = insert.on_conflict_do_update(index_elements=[primary_key], set_=update_cols)  # type: ignore
                session.execute(update.execution_options(synchronize_session=False))  # type: ignore

        def callback(session: SessionType):
            new_items = [attr.asdict(x) for x in items]

            primary_key = "id"
            if orm_type == TeamORM:
                primary_key = "team"
            elif orm_type == YearORM:
                primary_key = "year"

            if insert_only:
                return _insert(session, new_items)  # type: ignore
            return _update(session, primary_key, new_items)  # type: ignore

        # short circuit if no items
        if len(items) == 0:
            return

        run_transaction(Session, callback)

    return upsert
