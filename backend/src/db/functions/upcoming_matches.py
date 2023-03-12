from datetime import datetime
from typing import Dict, List, Tuple

from sqlalchemy.orm import Session as SessionType
from sqlalchemy_cockroachdb import run_transaction  # type: ignore

from src.constants import CURR_YEAR, CURR_WEEK
from src.db.main import Session
from src.db.models.event import EventORM
from src.db.models.match import MatchORM, Match
from src.db.models.team_event import TeamEventORM


def get_upcoming_matches() -> List[Tuple[Match, str, Dict[int, float]]]:
    curr_timestamp = int(datetime.now().timestamp())

    def callback(session: SessionType):
        matches = (
            session.query(MatchORM, EventORM.name)  # type: ignore
            .filter(
                (MatchORM.year == CURR_YEAR)  # type: ignore
                & (MatchORM.status == "Upcoming")
                & (MatchORM.predicted_time > curr_timestamp)
                & (MatchORM.event == EventORM.key)  # type: ignore
            )
            .limit(100)
            .all()
        )

        match_teams = [
            [
                match.red_1,
                match.red_2,
                match.red_3,
                match.blue_1,
                match.blue_2,
                match.blue_3,
            ]
            for (match, _) in matches
        ]
        match_teams = set([team for team_list in match_teams for team in team_list])

        team_events = (
            session.query(TeamEventORM.team, TeamEventORM.epa_end)  # type: ignore
            .filter(
                (TeamEventORM.year == CURR_YEAR)  # type: ignore
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
            for (match, event_name) in matches
        ]

    return run_transaction(Session, callback)  # type: ignore
