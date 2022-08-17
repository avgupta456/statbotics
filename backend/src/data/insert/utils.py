from datetime import datetime
from typing import Any, Callable, Dict, List, Tuple

from src.db.functions.clear_year import clear_year
from src.db.models.event import Event
from src.db.models.match import Match
from src.db.models.team_event import TeamEvent
from src.db.models.team_match import TeamMatch
from src.db.models.team_year import TeamYear
from src.db.models.year import Year
from src.db.read.event import get_num_events as get_num_events_db
from src.db.read.match import get_num_matches as get_num_matches_db
from src.db.read.team import get_num_teams as get_num_teams_db
from src.db.read.team_event import get_num_team_events as get_num_team_events_db
from src.db.read.team_match import get_num_team_matches as get_num_team_matches_db
from src.db.read.team_year import get_num_team_years as get_num_team_years_db
from src.db.read.year import get_num_years as get_num_years_db
from src.db.write.main import (
    update_events as update_events_db,
    update_matches as update_matches_db,
    update_team_events as update_team_events_db,
    update_team_matches as update_team_matches_db,
    update_team_years as update_team_years_db,
    update_years as update_years_db,
)

objs_type = Tuple[
    Year,
    List[TeamYear],
    List[Event],
    List[TeamEvent],
    List[Match],
    List[TeamMatch],
]


def write_objs(
    year_num: int,
    year: Year,
    team_years: List[TeamYear],
    events: List[Event],
    team_events: List[TeamEvent],
    matches: List[Match],
    team_matches: List[TeamMatch],
    end_year: int,
    clean: bool,
) -> None:
    # removes records with no events/matches
    # team_years = [t for t in team_years if t.elo_end is not None or t.year == end_year]
    team_ids = [t.team for t in team_years]
    team_events = [t for t in team_events if t.team in team_ids]
    event_keys = set([t.event for t in team_events])
    events = [e for e in events if e.key in event_keys]

    # writes to db
    clear_year(year_num)
    update_years_db([year], clean)
    update_team_years_db(team_years, clean)
    update_events_db(events, clean)
    update_team_events_db(team_events, clean)
    update_matches_db(matches, clean)
    update_team_matches_db(team_matches, clean)


def print_table_stats() -> None:
    print("Num Teams:", get_num_teams_db())
    print("Num Years:", get_num_years_db())
    print("Num Team Years:", get_num_team_years_db())
    print("Num Events:", get_num_events_db())
    print("Num Team Events:", get_num_team_events_db())
    print("Num Matches:", get_num_matches_db())
    print("Num Team Matches:", get_num_team_matches_db())


def time_func(
    label: str, func: Callable[..., Any], *args: List[Any], **kwargs: Dict[str, Any]
) -> Any:
    start = datetime.now()
    output = func(*args, **kwargs)
    end = datetime.now()
    print(label, "\t", end - start)
    return output
