from typing import Callable, List, Type

from sqlalchemy.orm.session import Session as SessionType
from sqlalchemy_cockroachdb import run_transaction  # type: ignore

from db.main import Session
from db.models.main import TModel, TModelORM


def update_template(
    orm_type: Type[TModelORM], obj_type: Type[TModel]
) -> Callable[[List[TModel], bool], None]:
    def _update(session: SessionType, data: List[obj_type]):
        for i in range(0, len(data), 1000):
            session.bulk_update_mappings(orm_type, data[i : i + 1000])  # type: ignore

    def _insert(session: SessionType, data: List[obj_type]):
        for i in range(0, len(data), 1000):
            session.bulk_insert_mappings(orm_type, data[i : i + 1000])  # type: ignore

    def update(items: List[obj_type], insert_only: bool = False) -> None:
        def callback(session: SessionType):
            if insert_only:
                return _insert(session, [x.__dict__ for x in items])  # type: ignore

            ids: List[int] = [item.id for item in items]  # type: ignore
            curr_ids: List[int] = [
                x[0] for x in session.query(orm_type.id).filter(orm_type.id.in_(ids)).all()  # type: ignore
            ]
            existing_ids = set(ids).intersection(set(curr_ids))
            _update(session, [x.__dict__ for x in items if x.id in existing_ids])  # type: ignore
            _insert(session, [x.__dict__ for x in items if x.id not in existing_ids])  # type: ignore

        run_transaction(Session, callback)

    return update
