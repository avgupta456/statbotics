# type: ignore

from datetime import datetime
from typing import Dict, List, Tuple, Optional

from sqlalchemy import func, text
from sqlalchemy.orm import Session as SessionType
from sqlalchemy_cockroachdb import run_transaction

from src.constants import CURR_YEAR, CURR_WEEK
from src.db.main import Session
from src.db.models.event import EventORM
from src.db.models.match import MatchORM, Match
from src.db.models.team_event import TeamEventORM


def get_upcoming_matches(
    country: Optional[str],
    state: Optional[str],
    district: Optional[str],
    playoff: Optional[bool],
    minutes: int,
    limit: int,
    metric: str,
) -> List[Tuple[Match, str, Dict[int, float]]]:
    curr_timestamp = int(datetime.now().timestamp()) - 100000  # 5 minutes

    if minutes == -1:
        minutes = 60 * 24 * 7  # 1 week

    def callback(session: SessionType):
        matches = session.query(
            MatchORM,
            EventORM.name,
            EventORM.country,
            EventORM.state,
            EventORM.district,
        ).add_columns(
            func.greatest(MatchORM.red_epa_sum, MatchORM.blue_epa_sum).label("max_epa"),
            (MatchORM.red_epa_sum + MatchORM.blue_epa_sum).label("sum_epa"),
            func.abs(MatchORM.red_epa_sum - MatchORM.blue_epa_sum).label("diff_epa"),
        )

        matches = matches.filter(
            (MatchORM.year == CURR_YEAR)
            & (MatchORM.status == "Upcoming")
            & (MatchORM.predicted_time > curr_timestamp)
            & (MatchORM.predicted_time < curr_timestamp + 60 * minutes)
            & (MatchORM.event == EventORM.key)
        )

        if country is not None:
            matches = matches.filter(EventORM.country == country)

        if state is not None:
            matches = matches.filter(EventORM.state == state)

        if district is not None:
            matches = matches.filter(EventORM.district == district)

        if playoff is not None:
            matches = matches.filter(MatchORM.playoff == playoff)

        if metric in ["max_epa", "sum_epa"]:
            # sort desc
            matches = matches.order_by(text(f"{metric} DESC"))
        else:
            # sort asc
            matches = matches.order_by(text(f"{metric} ASC"))

        matches = matches.limit(limit).all()

        match_teams: List[List[int]] = [
            [
                match.red_1,
                match.red_2,
                match.red_3,
                match.blue_1,
                match.blue_2,
                match.blue_3,
            ]
            for (match, *args) in matches
        ]
        match_teams = set([team for team_list in match_teams for team in team_list])

        team_events = (
            session.query(TeamEventORM.team, TeamEventORM.epa_end)
            .filter(
                (TeamEventORM.year == CURR_YEAR)
                & (TeamEventORM.week == CURR_WEEK)
                & (TeamEventORM.team.in_(match_teams))
            )
            .all()
        )

        team_events_dict = {team: epa for (team, epa) in team_events}

        return [
            (
                Match.from_dict(match.__dict__),
                event_name,
                {
                    team: team_events_dict.get(team, 0)
                    for team in [
                        match.red_1,
                        match.red_2,
                        match.red_3,
                        match.blue_1,
                        match.blue_2,
                        match.blue_3,
                    ]
                },
            )
            for (match, event_name, *args) in matches
        ]

    return run_transaction(Session, callback)
