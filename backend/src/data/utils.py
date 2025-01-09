from datetime import datetime
from typing import Dict, Optional, Tuple

from src.db.functions import clear_year
from src.db.models import ETag, Event, Match, TeamEvent, TeamMatch, TeamYear, Year
from src.db.read import (
    get_etags as get_etags_db,
    get_events as get_events_db,
    get_matches as get_matches_db,
    get_num_etags as get_num_etags_db,
    get_num_events as get_num_events_db,
    get_num_matches as get_num_matches_db,
    get_num_team_events as get_num_team_events_db,
    get_num_team_matches as get_num_team_matches_db,
    get_num_team_years as get_num_team_years_db,
    get_num_teams as get_num_teams_db,
    get_num_years as get_num_years_db,
    get_team_events as get_team_events_db,
    get_team_matches as get_team_matches_db,
    get_team_years as get_team_years_db,
    get_year as get_year_db,
)
from src.db.write.main import (
    update_etags as update_etags_db,
    update_events as update_events_db,
    update_matches as update_matches_db,
    update_team_events as update_team_events_db,
    update_team_matches as update_team_matches_db,
    update_team_years as update_team_years_db,
    update_years as update_years_db,
)

objs_type = Tuple[
    Year,
    Dict[str, TeamYear],
    Dict[str, Event],
    Dict[str, TeamEvent],
    Dict[str, Match],
    Dict[str, TeamMatch],
    Dict[str, ETag],
]


def create_objs(year: int) -> objs_type:
    return (Year(year=year), {}, {}, {}, {}, {}, {})


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
        {tm.pk(): tm for tm in get_team_matches_db(year=year)},
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
        # Ensure that all objects are updated
        orig_objs = create_objs(-1)

    update_years_db([objs[0]], clean)

    for prev, curr, update_func in [
        (orig_objs[1], objs[1], update_team_years_db),
        (orig_objs[2], objs[2], update_events_db),
        (orig_objs[3], objs[3], update_team_events_db),
        (orig_objs[4], objs[4], update_matches_db),
        (orig_objs[5], objs[5], update_team_matches_db),
        (orig_objs[6], objs[6], update_etags_db),
    ]:
        new_objs = [
            obj
            for obj in list(curr.values())
            if str(obj) != str(prev.get(obj.pk(), ""))
        ]

        update_func(new_objs, clean)  # type: ignore


def print_table_stats() -> None:
    print("Num Teams:", get_num_teams_db())
    print("Num Years:", get_num_years_db())
    print("Num Team Years:", get_num_team_years_db())
    print("Num Events:", get_num_events_db())
    print("Num Team Events:", get_num_team_events_db())
    print("Num Matches:", get_num_matches_db())
    print("Num Team Matches:", get_num_team_matches_db())
    print("Num ETags", get_num_etags_db())


class Timer:
    def __init__(self):
        self.start = datetime.now()

    def print(self, label: str) -> None:
        end = datetime.now()
        print(label, "\t", end - self.start)
        self.start = end
