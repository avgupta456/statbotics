from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor

# from datetime import datetime
import json
from typing import Any, List, Optional
import zlib

from google.cloud import storage

from src.constants import CURR_YEAR, PROD
from src.data.utils import objs_type
from src.db.functions import get_noteworthy_matches, get_upcoming_matches
from src.db.read.event import get_events as get_events_db
from src.db.read.team import get_teams as get_teams_db
from src.site.event import _read_all_events, _read_events, _read_event
from src.site.match import _read_noteworthy_matches, _read_upcoming_matches
from src.site.team_year import _read_team_years
from src.site.team import _read_all_teams

BUCKET_NAME = "site_v1" if PROD else "site_dev_v1"


def compress(data: Any) -> bytes:
    # start = datetime.now()
    json_bytes = json.dumps(data).encode("utf-8")
    compressed = zlib.compress(json_bytes)
    # print(
    #     f"Compressed data from {len(json_bytes)} to {len(compressed)} bytes in {datetime.now() - start}"
    # )
    return compressed


def upload_file_to_gcs(data: Any, object_name: str) -> None:
    # start = datetime.now()
    storage.Client().bucket(BUCKET_NAME).blob(object_name).upload_from_string(
        compress(data), "application/octet-stream"
    )
    # print(f"Uploaded {object_name} to GCS in {datetime.now() - start}")


def upload_files_to_gcs(data: List[Any], object_names: List[str]) -> None:
    with ThreadPoolExecutor() as executor:
        executor.map(upload_file_to_gcs, data, object_names)


def write_objs(
    objs: objs_type,
    orig_objs: Optional[objs_type] = None,
) -> None:
    # teams/all
    teams = get_teams_db()
    upload_file_to_gcs(_read_all_teams(teams), "teams/all")

    # team_years/{CURR_YEAR}
    year = CURR_YEAR
    year_obj = objs[0]
    team_years = list(objs[1].values())
    upload_file_to_gcs(
        _read_team_years(year, year_obj, team_years), f"team_years/{year}"
    )

    # team_years/{CURR_YEAR}?limit=100&metric=epa
    team_years = sorted(team_years, key=lambda x: -x.epa)[:100]
    upload_file_to_gcs(
        _read_team_years(year, year_obj, team_years),
        f"team_years/{year}.limit=100.metric=epa",
    )

    # events/all
    events = get_events_db()
    upload_file_to_gcs(_read_all_events(events), "events/all")

    # events/{CURR_YEAR}
    events = list(objs[2].values())
    upload_file_to_gcs(_read_events(year_obj, events), f"events/{year}")

    # event/{event.key}
    orig_events = orig_objs[2] if orig_objs else {}
    new_events = [e for e in events if str(e) != str(orig_events.get(e.pk(), ""))]
    if len(new_events) > 0:
        event_to_matches = defaultdict(list)
        event_to_team_events = defaultdict(list)
        event_to_team_matches = defaultdict(list)
        for m in objs[4].values():
            event_to_matches[m.event].append(m)
        for te in objs[3].values():
            event_to_team_events[te.event].append(te)
        for tm in objs[5].values():
            event_to_team_matches[tm.event].append(tm)
        data = []
        object_names = []
        for event in new_events:
            matches = event_to_matches.get(event.key, [])
            team_events = event_to_team_events.get(event.key, [])
            team_matches = event_to_team_matches.get(event.key, [])
            data.append(
                _read_event(year_obj, event, matches, team_events, team_matches)
            )
            object_names.append(f"event/{event.key}")
        upload_files_to_gcs(data, object_names)

    team_to_events = defaultdict(list)
    for team_event in objs[3].values():
        team_to_events[team_event.team].append(team_event.event)
    upload_file_to_gcs(team_to_events, "team_to_events")

    # noteworthy_matches/{year}
    noteworthy_matches = get_noteworthy_matches(
        year=year, country=None, state=None, district=None, elim=None, week=None
    )
    upload_file_to_gcs(
        _read_noteworthy_matches(noteworthy_matches), f"noteworthy_matches/{year}"
    )

    # upcoming_matches?limit=20&metric={predicted_time | max_epa | sum_epa | diff_epa}
    for metric in ["predicted_time", "max_epa", "sum_epa", "diff_epa"]:
        upcoming_matches = get_upcoming_matches(
            country=None,
            state=None,
            district=None,
            elim=None,
            minutes=-1,
            limit=20,
            metric=metric,
        )
        upload_file_to_gcs(
            _read_upcoming_matches(upcoming_matches),
            f"upcoming_matches.limit=20.metric={metric}",
        )

    return
