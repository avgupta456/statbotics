from datetime import datetime
from typing import Dict, Optional, Tuple

from src.db.functions import clear_year
from src.db.models import ETag, Event, Match, TeamEvent, TeamYear, Year
from src.db.read import (
    get_etags as get_etags_db,
    get_events as get_events_db,
    get_matches as get_matches_db,
    get_team_events as get_team_events_db,
    get_team_years as get_team_years_db,
    get_year as get_year_db,
)
from src.db.write.main import write_year as write_year_db

objs_type = Tuple[
    Year,
    Dict[str, TeamYear],
    Dict[str, Event],
    Dict[str, TeamEvent],
    Dict[str, Match],
    Dict[str, ETag],
]


def create_objs(year: int) -> objs_type:
    return (Year(year=year), {}, {}, {}, {}, {})


def read_objs(year: int) -> objs_type:
    year_obj = get_year_db(year)
    if year_obj is None:
        raise Exception("Year not found")

    return (
        year_obj,
        {t.pk(): t for t in get_team_years_db(year=year)},
        {e.pk(): e for e in get_events_db(year=year)},
        {te.pk(): te for te in get_team_events_db(year=year)},
        {m.pk(): m for m in get_matches_db(year=year)},
        {e.pk(): e for e in get_etags_db(year=year)},
    )


def write_objs(
    year_num: int,
    objs: objs_type,
    orig_objs: Optional[objs_type] = None,
    clean: bool = False,
) -> None:
    if clean:
        clear_year(year_num)

    if orig_objs is None:
        orig_objs = create_objs(-1)

    def changed(curr: dict, prev: dict) -> list:
        return [obj for obj in curr.values() if str(obj) != str(prev.get(obj.pk(), ""))]

    write_year_db(
        years=[objs[0]],
        team_years=changed(objs[1], orig_objs[1]),
        events=changed(objs[2], orig_objs[2]),
        team_events=changed(objs[3], orig_objs[3]),
        matches=changed(objs[4], orig_objs[4]),
        etags=changed(objs[5], orig_objs[5]),
        insert_only=clean,
    )


class Timer:
    def __init__(self):
        self.start = datetime.now()

    def print(self, label: str) -> None:
        end = datetime.now()
        print(label, "\t", end - self.start)
        self.start = end
