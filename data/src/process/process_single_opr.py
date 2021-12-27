from db.read.event import get_events as get_events_db
from db.read.match import get_matches as get_matches_db
from db.read.team_event import get_team_events as get_team_events_db
from db.read.year import get_years as get_years_db

from process.process_opr import process_event


def process_single(year_num: int, event_id: int):
    year_obj = get_years_db(year_num)[0]
    event = get_events_db(id=event_id)[0]
    matches = get_matches_db(event_id=event_id)
    team_events = get_team_events_db(event_id=event_id)

    _oprs, _ils, stats = process_event(
        event,
        team_events,
        matches,
        year_num,
        year_obj.score_mean or 0,
        year_obj.score_sd or 0,
    )

    print(stats)
