from collections import defaultdict
from typing import Dict

from src.data.utils import objs_type
from src.db.models import Event, TeamEvent, TeamMatch, TeamYear
from src.models.epa.main import EPA
from src.utils.utils import get_team_event_key, get_team_match_key, get_team_year_key


def process_year(
    objs: objs_type, all_team_years: Dict[int, Dict[int, TeamYear]]
) -> objs_type:
    year = objs[0]
    team_years = objs[1]
    events = objs[2]
    team_events = objs[3]
    matches = objs[4]
    team_matches = objs[5]

    match_events: Dict[str, Event] = {}
    match_team_matches: Dict[str, Dict[int, TeamMatch]] = defaultdict(dict)
    match_team_events: Dict[str, Dict[int, TeamEvent]] = defaultdict(dict)
    match_team_years: Dict[str, Dict[int, TeamYear]] = defaultdict(dict)
    for match in matches.values():
        match_events[match.key] = events[match.event]
        red_teams, blue_teams = match.get_teams()
        for team in red_teams + blue_teams:
            team_match_key = get_team_match_key(team, match.key)
            match_team_matches[match.key][team] = team_matches[team_match_key]
            team_event_key = get_team_event_key(team, match.event)
            match_team_events[match.key][team] = team_events[team_event_key]
            team_year_key = get_team_year_key(team, match.year)
            match_team_years[match.key][team] = team_years[team_year_key]

    model = EPA()

    model.start_season(year, all_team_years, team_years)
    for curr_match in sorted(matches.values(), key=lambda m: m.time):
        curr_event = match_events[curr_match.key]
        curr_team_matches = match_team_matches[curr_match.key]
        curr_team_events = match_team_events[curr_match.key]
        curr_team_years = match_team_years[curr_match.key]
        model.process_match(
            curr_match,
            curr_event,
            curr_team_matches,
            curr_team_events,
            curr_team_years,
        )

    # Records TeamEvent EPA stats if no matches played yet
    for team_event in team_events.values():
        if team_event.qual_count == 0:
            model.post_record_team(team_event.team, None, team_event, None)

    return objs
