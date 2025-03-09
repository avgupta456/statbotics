from typing import Any, Callable, List, Type, Coroutine

import attr
from sqlalchemy.dialects import postgresql

from src.db.main import async_session
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
) -> Callable[[List[TModel], bool], Coroutine[Any, Any, None]]:
    async def upsert(items: List[TModel], insert_only: bool = False) -> None:
        async def _insert(session, new_items):
            for i in range(0, len(new_items), CUTOFF):
                session.add_all(
                    [orm_type(**data) for data in new_items[i : i + CUTOFF]]
                )
            await session.commit()

        async def _update(session, primary_key, new_items):
            for i in range(0, len(new_items), CUTOFF):
                insert_stmt = postgresql.insert(orm_type.__table__).values(
                    new_items[i : i + CUTOFF]
                )
                update_cols = {
                    c.name: c for c in insert_stmt.excluded if c.name not in primary_key
                }
                update_stmt = insert_stmt.on_conflict_do_update(
                    index_elements=primary_key, set_=update_cols
                )
                await session.execute(
                    update_stmt.execution_options(synchronize_session=False)
                )

            await session.commit()

        async with async_session() as session:
            new_items = [attr.asdict(x) for x in items]

            if not new_items:
                return

            primary_key = {
                ETagORM: ["path"],
                TeamORM: ["team"],
                YearORM: ["year"],
                TeamYearORM: ["team", "year"],
                EventORM: ["key"],
                TeamEventORM: ["team", "event"],
                MatchORM: ["key"],
                TeamMatchORM: ["team", "match"],
            }.get(orm_type)

            if primary_key is None:
                raise Exception("Unknown orm_type: " + str(orm_type))

            if insert_only:
                return await _insert(session, new_items)
            return await _update(session, primary_key, new_items)

    return upsert
