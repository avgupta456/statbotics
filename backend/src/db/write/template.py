from typing import Any, Callable, Dict, List, Type

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
from src.db.models.team_match import TeamMatchORM
from src.db.models.team_year import TeamYearORM
from src.db.models.year import YearORM

CUTOFF = 1000


def update_template(
    orm_type: Type[TModelORM], obj_type: Type[TModel]
) -> Callable[[List[TModel], bool], None]:
    def upsert(items: List[obj_type], insert_only: bool = False) -> None:  # type: ignore
        def _insert(session: SessionType, data: List[Dict[str, Any]]):
            for i in range(0, len(data), CUTOFF):
                session.bulk_insert_mappings(orm_type, data[i : i + CUTOFF])  # type: ignore

        def _update(
            session: SessionType, primary_key: List[str], data: List[Dict[str, Any]]
        ):
            for i in range(0, len(data), CUTOFF):
                insert = postgresql.insert(orm_type.__table__).values(
                    data[i : i + CUTOFF]
                )
                update_cols = {
                    c.name: c for c in insert.excluded if c.name not in primary_key
                }
                update = insert.on_conflict_do_update(
                    index_elements=primary_key, set_=update_cols
                )
                session.execute(update.execution_options(synchronize_session=False))

        def callback(session: SessionType):
            new_items = [attr.asdict(x) for x in items]

            if orm_type == ETagORM:
                primary_key = ["path"]
            elif orm_type == TeamORM:
                primary_key = ["team"]
            elif orm_type == YearORM:
                primary_key = ["year"]
            elif orm_type == TeamYearORM:
                primary_key = ["team", "year"]
            elif orm_type == EventORM:
                primary_key = ["key"]
            elif orm_type == TeamEventORM:
                primary_key = ["team", "event"]
            elif orm_type == MatchORM:
                primary_key = ["key"]
            elif orm_type == TeamMatchORM:
                primary_key = ["team", "match"]
            else:
                raise Exception("Unknown orm_type: " + str(orm_type))

            if insert_only:
                return _insert(session, new_items)
            return _update(session, primary_key, new_items)

        # short circuit if no items
        if len(items) == 0:
            return

        run_transaction(Session, callback)

    return upsert
