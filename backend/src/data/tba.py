from datetime import datetime, timedelta
from typing import Callable, Dict, List, Optional, Set, Tuple, TypeVar

from src.constants import CURR_WEEK, CURR_YEAR
from src.data.utils import objs_type
from src.db.functions import remove_teams_with_no_events, update_team_districts
from src.db.models import ETag, Event, Team, TeamEvent, TeamYear, match_dict_to_objs
from src.tba.constants import DISTRICT_MAPPING
from src.tba.read_tba import (
    EventDict,
    MatchDict,
    get_district_rankings as get_district_rankings_tba,
    get_district_teams as get_district_teams_tba,
    get_districts as get_districts_tba,
    get_event_alliances as get_event_alliances_tba,
    get_event_matches as get_event_matches_tba,
    get_event_rankings as get_event_rankings_tba,
    get_event_teams as get_event_teams_tba,
    get_events as get_events_tba,
    get_teams as get_teams_tba,
)
from src.types.enums import CompLevel, EventStatus, MatchStatus, MatchWinner
from src.utils.utils import get_team_event_key, get_team_year_key

OS = Optional[str]

"""
HELPER FUNCTIONS
"""


def load_teams(cache: bool = True) -> List[Team]:
    teams = get_teams_tba(cache=cache)
    team_objs = [
        Team(
            team=int(team["team"]),
            name=team["name"],
            country=team["country"],
            state=team["state"],
            rookie_year=team["rookie_year"],
        )
        for team in teams
    ]
    return team_objs


def get_event_status(matches: List[MatchDict], year: int) -> EventStatus:
    num_matches = len(matches)
    num_qual_matches = len([m for m in matches if m["comp_level"] == CompLevel.QUAL])
    finals_matches = [m for m in matches if m["comp_level"] == CompLevel.FINAL]

    red_final_match_wins = len(
        [m for m in finals_matches if m["winner"] == MatchWinner.RED]
    )
    blue_final_match_wins = len(
        [m for m in finals_matches if m["winner"] == MatchWinner.BLUE]
    )
    max_finals_winner = max(red_final_match_wins, blue_final_match_wins)

    num_upcoming_matches = 0
    for match in matches:
        if match["status"] == MatchStatus.UPCOMING:
            num_upcoming_matches += 1

    elim_started = num_matches > num_qual_matches
    finals_finished = num_upcoming_matches == 0 or max_finals_winner >= 2

    event_status: EventStatus = EventStatus.COMPLETED
    if year == CURR_YEAR:
        if num_matches == 0:
            event_status = EventStatus.UPCOMING
        elif not elim_started or not finals_finished:
            event_status = EventStatus.ONGOING
        else:
            event_status = EventStatus.COMPLETED
    elif num_matches == 0:
        return EventStatus.INVALID
    return event_status


"""
MAIN FUNCTIONS
"""


def check_year_partial(
    year_num: int, event_objs: List[Event], etags: List[ETag]
) -> bool:
    etags_dict = {etag.path: etag for etag in etags}
    default_etag = ETag(year_num, "NA", "NA")

    prev_etag = etags_dict.get(str(year_num) + "/events", default_etag).etag
    _, new_etag = get_events_tba(year_num, etag=prev_etag, cache=False)
    if new_etag != prev_etag:
        return True  # If any new events

    for event_obj in event_objs:
        if event_obj.status == EventStatus.COMPLETED:
            continue

        start_date = datetime.strptime(event_obj.start_date, "%Y-%m-%d")
        end_date = datetime.strptime(event_obj.end_date, "%Y-%m-%d")
        if start_date - timedelta(days=1) > datetime.now():
            continue

        if end_date + timedelta(days=1) < datetime.now():
            continue

        prev_etag = etags_dict.get(event_obj.key + "/matches", default_etag).etag
        _, new_etag = get_event_matches_tba(
            year_num,
            event_obj.key,
            event_obj.time,
            prev_etag,
            cache=False,
        )
        if new_etag != prev_etag and new_etag is not None:
            return True  # If any event has new matches, return True

        if event_obj.status == EventStatus.UPCOMING:
            continue

        prev_etag = etags_dict.get(event_obj.key + "/rankings", default_etag).etag
        _, new_etag = get_event_rankings_tba(event_obj.key, prev_etag, cache=False)
        if new_etag != prev_etag and new_etag is not None:
            return True  # If any event has new rankings, return True

        qual_matches = event_obj.qual_matches or 0
        current_match = event_obj.current_match or 0
        if qual_matches == 0 or current_match < qual_matches:
            continue

        _, new_etag = get_event_alliances_tba(event_obj.key, prev_etag, cache=False)
        if new_etag != prev_etag and new_etag is not None:
            return True  # If any event has new alliances, return True

    return False  # Otherwise return False


def process_year(
    year_num: int,
    teams: List[Team],
    objs: objs_type,
    partial: bool,
    cache: bool = True,
) -> Tuple[List[Team], objs_type]:
    (
        year_obj,
        team_year_objs_dict,
        event_objs_dict,
        team_event_objs_dict,
        match_objs_dict,
        team_match_objs_dict,
        etags_dict,
    ) = objs

    default_etag = ETag(year_num, "NA", "NA")
    new_etags_dict: Dict[str, ETag] = {}

    T = TypeVar("T")

    def call_tba(func: Callable[..., Tuple[T, OS]], path: str) -> Tuple[T, bool]:
        prev_etag = etags_dict.get(path, default_etag).etag
        if partial:
            out, new_etag = func(prev_etag, False)
            if new_etag is not None:
                new_etag_obj = ETag(year_num, path, new_etag)
                new_etags_dict[new_etag_obj.pk()] = new_etag_obj
        else:
            out, new_etag = func(None, cache)
        return out, new_etag is not None and new_etag != prev_etag

    teams_dict: Dict[int, Team] = {team.team: team for team in teams}
    team_competing_this_week_dict: Dict[int, bool] = {}
    team_first_event_dict: Dict[int, Tuple[OS, int]] = {}

    # maps team to district_abbrev (or None if not in a district)
    team_to_district: Dict[int, OS] = {}
    team_to_district_points: Dict[int, int] = {}
    team_to_district_rank: Dict[int, int] = {}
    team_event_to_district_points: Dict[str, int] = {}

    all_teams: Set[int] = set()

    if not partial:

        def get_districts_tba_year(
            etag: OS, cache: bool
        ) -> Tuple[List[Tuple[str, str]], OS]:
            return get_districts_tba(year_num, etag=etag, cache=cache)

        districts, _ = call_tba(get_districts_tba_year, str(year_num) + "/districts")

        for district_key, district_abbrev in districts:
            district_teams, _ = get_district_teams_tba(district_key, cache=cache)
            for team in district_teams:
                team_to_district[team] = DISTRICT_MAPPING.get(
                    district_abbrev, district_abbrev
                )
            (
                team_to_points,
                team_to_rank,
                team_event_to_points,
            ), _ = get_district_rankings_tba(district_key, cache=cache)
            for team in team_to_points:
                team_to_district_points[team] = team_to_points[team]
                team_to_district_rank[team] = team_to_rank[team]
            for team_event in team_event_to_points:
                team_event_to_district_points[team_event] = team_event_to_points[
                    team_event
                ]

    def get_events_tba_year(etag: OS, cache: bool) -> Tuple[List[EventDict], OS]:
        return get_events_tba(year_num, etag=etag, cache=cache)

    events, _ = call_tba(get_events_tba_year, str(year_num) + "/events")

    for event in events:
        key = event["key"]
        curr_obj = event_objs_dict.get(key, None)
        curr_status = EventStatus.UPCOMING if curr_obj is None else curr_obj.status
        event_objs_dict[key] = Event(
            key=key,
            year=year_num,
            name=event["name"],
            time=event["time"],
            country=event["country"],
            state=event["state"],
            district=event["district"],
            start_date=event["start_date"],
            end_date=event["end_date"],
            type=event["type"],
            week=event["week"],
            video=event["video"],
            status=curr_status,
        )

    for event_obj in event_objs_dict.values():
        if partial:
            if event_obj.week != CURR_WEEK and event_obj.status != EventStatus.ONGOING:
                continue

        event_key, event_time = event_obj.key, event_obj.time

        def get_event_matches_tba_year(
            etag: OS, cache: bool
        ) -> Tuple[List[MatchDict], OS]:
            # TODO: use etag to avoid querying every time (needed to get matches)
            return get_event_matches_tba(year_num, event_key, event_time, None, cache)

        matches, _ = call_tba(get_event_matches_tba_year, event_key + "/matches")
        event_status = get_event_status(matches, year_num)
        event_obj.status = event_status

        event_teams: Set[int] = set()
        rankings: Dict[int, int] = {}
        alliance_dict: Dict[int, str] = {}
        captain_dict: Dict[int, bool] = {}

        def add_team_event(team: int):
            all_teams.add(team)
            event_teams.add(team)
            event_week = event_obj.week
            event_year = event_obj.year

            # Stores whether a team is competing this week
            if event_year == CURR_YEAR and event_week == CURR_WEEK:
                team_competing_this_week_dict[team] = True

            # Store first event
            if team not in team_first_event_dict:
                # first event for team
                team_first_event_dict[team] = (event_key, event_week)
            elif (team_first_event_dict[team][1] or -1) > event_week:
                # event is closer than previous closest event
                team_first_event_dict[team] = (event_key, event_week)

        if event_status == EventStatus.INVALID:
            continue

        elif event_status == EventStatus.UPCOMING:

            def get_event_teams_tba_year(etag: OS, cache: bool) -> Tuple[List[int], OS]:
                return get_event_teams_tba(event_key, etag, cache)

            temp_event_teams, _ = call_tba(
                get_event_teams_tba_year, event_key + "/teams"
            )

            for team in temp_event_teams:
                add_team_event(team)

        elif event_status in [EventStatus.ONGOING, EventStatus.COMPLETED]:
            # Update event_obj, accumulate match_obj, alliance_objs, team_match_objs
            for match in matches:
                (match_obj, curr_team_match_objs) = match_dict_to_objs(
                    match, year_num, event_obj.week
                )

                # Replace even if present, since may be Upcoming -> Completed
                match_objs_dict[match_obj.key] = match_obj
                for team_match_obj in curr_team_match_objs:
                    add_team_event(team_match_obj.team)
                    team_match_objs_dict[team_match_obj.pk()] = team_match_obj

            def get_event_rankings_tba_year(
                etag: OS, cache: bool
            ) -> Tuple[Dict[int, int], OS]:
                # TODO: use etag to avoid querying every time (needed to get rankings)
                return get_event_rankings_tba(event_key, None, cache)

            rankings, _ = call_tba(get_event_rankings_tba_year, event_key + "/rankings")

            def get_event_alliances_tba_year(
                etag: OS, cache: bool
            ) -> Tuple[Tuple[Dict[int, str], Dict[int, bool]], OS]:
                # TODO: use etag to avoid querying every time (needed to get alliances)
                return get_event_alliances_tba(event_key, None, cache)

            (alliance_dict, captain_dict), _ = call_tba(
                get_event_alliances_tba_year, event_key + "/alliances"
            )

        # For Upcoming, Ongoing, and Completed events
        for team in event_teams:
            if team not in teams_dict:
                teams_dict[team] = Team(
                    team=team,
                    name=str(team),
                    country=None,
                    state=None,
                    rookie_year=None,
                )

            team_obj = teams_dict[team]

            team_event_key = get_team_event_key(team, event_key)
            curr_te = team_event_objs_dict.get(team_event_key, None)
            if curr_te is None:
                curr_te = TeamEvent(
                    id=None,
                    team=team,
                    year=year_num,
                    event=event_key,
                    time=event_time,
                    team_name=team_obj.name,
                    event_name=event_obj.name,
                    country=event_obj.country,
                    state=event_obj.state,
                    district=event_obj.district,
                    type=event_obj.type,
                    week=event_obj.week,
                    status=event_status,
                    first_event=False,
                    rank=None,
                    num_teams=None,
                    elim_alliance=None,
                    is_captain=None,
                    district_points=None,
                )

            curr_te.rank = rankings.get(team, curr_te.rank)
            curr_te.num_teams = len(event_teams)
            curr_te.elim_alliance = alliance_dict.get(team, curr_te.elim_alliance)
            curr_te.is_captain = captain_dict.get(team, curr_te.is_captain)
            curr_te.district_points = team_event_to_district_points.get(
                team_event_key, curr_te.district_points
            )
            team_event_objs_dict[team_event_key] = curr_te

    if not partial:
        # update is_first_event after iterating through all events
        for pk, team_event in team_event_objs_dict.items():
            team_event_objs_dict[pk].first_event = (
                team_first_event_dict[team_event.team][0] == team_event.event
            )

    for team in all_teams:
        team_obj = teams_dict[team]
        competing_this_week = team_competing_this_week_dict.get(team, False)

        team_year_key = get_team_year_key(team, year_num)
        curr_ty = team_year_objs_dict.get(team_year_key, None)
        if curr_ty is None:
            curr_ty = TeamYear(
                id=None,
                year=year_num,
                team=team,
                name=team_obj.name,
                country=team_obj.country,
                state=team_obj.state,
                district=None,
                rookie_year=team_obj.rookie_year,
                district_points=None,
                district_rank=None,
                competing_this_week=competing_this_week,
                next_event_key=None,
                next_event_name=None,
                next_event_week=None,
            )

        curr_ty.district = team_to_district.get(team, curr_ty.district)
        curr_ty.district_points = team_to_district_points.get(
            team, curr_ty.district_points
        )
        curr_ty.district_rank = team_to_district_rank.get(team, curr_ty.district_rank)
        team_year_objs_dict[team_year_key] = curr_ty

    orig_teams = set([team.team for team in teams])
    new_teams = [team for team in teams_dict.values() if team.team not in orig_teams]

    return new_teams, (
        year_obj,
        team_year_objs_dict,
        event_objs_dict,
        team_event_objs_dict,
        match_objs_dict,
        team_match_objs_dict,
        new_etags_dict,
    )


def post_process():
    remove_teams_with_no_events()
    update_team_districts()
