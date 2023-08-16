from typing import List

from src.db.models.etag import ETag, ETagORM
from src.db.models.event import Event, EventORM
from src.db.models.match import Match, MatchORM
from src.db.models.team import Team, TeamORM
from src.db.models.team_event import TeamEvent, TeamEventORM
from src.db.models.team_match import TeamMatch, TeamMatchORM
from src.db.models.team_year import TeamYear, TeamYearORM
from src.db.models.year import Year, YearORM
from src.db.write.template import update_template


def update_etags(items: List[ETag], only_insert: bool = False) -> None:
    return update_template(ETagORM, ETag)(items, only_insert)


def update_events(items: List[Event], only_insert: bool = False) -> None:
    return update_template(EventORM, Event)(items, only_insert)


def update_matches(items: List[Match], only_insert: bool = False) -> None:
    return update_template(MatchORM, Match)(items, only_insert)


def update_teams(items: List[Team], only_insert: bool = False) -> None:
    return update_template(TeamORM, Team)(items, only_insert)


def update_years(items: List[Year], only_insert: bool = False) -> None:
    return update_template(YearORM, Year)(items, only_insert)


def update_team_events(items: List[TeamEvent], only_insert: bool = False) -> None:
    return update_template(TeamEventORM, TeamEvent)(items, only_insert)


def update_team_matches(items: List[TeamMatch], only_insert: bool = False) -> None:
    return update_template(TeamMatchORM, TeamMatch)(items, only_insert)


def update_team_years(items: List[TeamYear], only_insert: bool = False) -> None:
    return update_template(TeamYearORM, TeamYear)(items, only_insert)
