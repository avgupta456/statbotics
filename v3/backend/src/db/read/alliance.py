from typing import List, Optional

from sqlalchemy.orm.session import Session as SessionType  # type: ignore
from sqlalchemy_cockroachdb import run_transaction  # type: ignore

from src.db.main import Session
from src.db.models.alliance import Alliance, AllianceORM


def get_alliances(
    team: Optional[int] = None,
    year: Optional[int] = None,
    event: Optional[str] = None,
    match: Optional[str] = None,
    alliance: Optional[str] = None,
    week: Optional[int] = None,
    elims: Optional[bool] = None,
    offseason: Optional[bool] = False,
    metric: Optional[str] = None,
    ascending: Optional[bool] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> List[Alliance]:
    def callback(session: SessionType):
        data = session.query(AllianceORM)  # type: ignore
        if team is not None:
            data = data.filter(  # type: ignore
                (AllianceORM.team_1 == team)
                | (AllianceORM.team_2 == team)
                | (AllianceORM.team_3 == team)
            )
        if year is not None:
            data = data.filter(AllianceORM.year == year)  # type: ignore
        if event is not None:
            data = data.filter(AllianceORM.event == event)  # type: ignore
        if match is not None:
            data = data.filter(AllianceORM.match == match)  # type: ignore
        if alliance is not None:
            data = data.filter(AllianceORM.alliance == alliance)  # type: ignore
        if week is not None:
            data = data.filter(AllianceORM.week == week)  # type: ignore
        if elims is not None:
            data = data.filter(AllianceORM.playoff == elims)  # type: ignore
        if offseason is not None:
            data = data.filter(AllianceORM.offseason == offseason)  # type: ignore
        if metric is not None:
            data = data.filter(AllianceORM.__dict__[metric] != None)  # type: ignore  # noqa: E711
            if ascending is not None and ascending:
                data = data.order_by(AllianceORM.__dict__[metric].asc())  # type: ignore
            else:
                data = data.order_by(AllianceORM.__dict__[metric].desc())  # type: ignore
        if limit is not None:
            data = data.limit(limit)  # type: ignore
        if offset is not None:
            data = data.offset(offset)  # type: ignore
        out_data: List[AllianceORM] = data.all()  # type: ignore

        return [Alliance.from_dict(x.__dict__) for x in out_data]  # type: ignore

    return run_transaction(Session, callback)  # type: ignore


def get_num_alliances() -> int:
    def callback(session: SessionType) -> int:
        return session.query(AllianceORM).count()  # type: ignore

    return run_transaction(Session, callback)  # type: ignore


# TODO: See if ascending/limit/offset logic can be consolidated as function decorator
