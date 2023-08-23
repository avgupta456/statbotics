from typing import List, Optional

from sqlalchemy.orm.session import Session as SessionType
from sqlalchemy_cockroachdb import run_transaction  # type: ignore

from src.db.main import Session
from src.db.models.alliance import Alliance, AllianceORM
from src.db.read.main import common_filters


def get_alliances(
    team: Optional[str] = None,
    year: Optional[int] = None,
    event: Optional[str] = None,
    match: Optional[str] = None,
    alliance: Optional[str] = None,
    week: Optional[int] = None,
    elim: Optional[bool] = None,
    offseason: Optional[bool] = False,
    metric: Optional[str] = None,
    ascending: Optional[bool] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> List[Alliance]:
    @common_filters(AllianceORM, Alliance, metric, ascending, limit, offset)
    def callback(session: SessionType):
        data = session.query(AllianceORM)
        if team is not None:
            data = data.filter(
                (AllianceORM.team_1 == team)
                | (AllianceORM.team_2 == team)
                | (AllianceORM.team_3 == team)
            )
        if year is not None:
            data = data.filter(AllianceORM.year == year)
        if event is not None:
            data = data.filter(AllianceORM.event == event)
        if match is not None:
            data = data.filter(AllianceORM.match == match)
        if alliance is not None:
            data = data.filter(AllianceORM.alliance == alliance)
        if week is not None:
            data = data.filter(AllianceORM.week == week)
        if elim is not None:
            data = data.filter(AllianceORM.elim == elim)
        if offseason is not None:
            data = data.filter(AllianceORM.offseason == offseason)

        return data

    return run_transaction(Session, callback)  # type: ignore


def get_num_alliances() -> int:
    def callback(session: SessionType) -> int:
        return session.query(AllianceORM).count()

    return run_transaction(Session, callback)  # type: ignore
