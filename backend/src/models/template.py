from typing import Any, Dict, Optional, Tuple

from src.db.models import Event, Match, TeamEvent, TeamYear, Year
from src.models.types import AlliancePred, Attribution, MatchPred
from src.tba.constants import PLACEHOLDER_TEAMS
from src.types.enums import MatchStatus


class Model:
    year_obj: Year
    year_num: int
    num_teams: int

    def __init__(self):
        pass

    def start_season(
        self,
        year: Year,
        all_team_years: Dict[int, Dict[int, TeamYear]],
        team_years: Dict[str, TeamYear],
    ) -> None:
        self.year_obj = year
        self.year_num = year.year
        self.num_teams = 2 if year.year <= 2004 else 3

    def predict_match(
        self, match: Match, event: Event
    ) -> Tuple[float, AlliancePred, AlliancePred]:
        raise NotImplementedError

    def attribute_match(
        self, match: Match, red_pred: AlliancePred, blue_pred: AlliancePred
    ) -> Dict[int, Attribution]:
        raise NotImplementedError

    def update_team(self, team: int, attrib: Attribution, match: Match) -> None:
        raise NotImplementedError

    def pre_record_team(self, team: int, te: TeamEvent, ty: TeamYear) -> Dict[str, Any]:
        return {}

    def post_record_team(
        self,
        team: int,
        te: Optional[TeamEvent],
        ty: Optional[TeamYear],
    ) -> Dict[str, Any]:
        return {}

    def record_match(self, match: Match, match_pred: MatchPred) -> None:
        pass

    def process_match(
        self,
        match: Match,
        event: Event,
        team_events: Dict[int, TeamEvent],
        team_years: Dict[int, TeamYear],
    ):
        win_prob, red_pred, blue_pred = self.predict_match(match, event)
        match_pred = MatchPred(win_prob, red_pred, blue_pred)

        pre_epas: Dict[str, Any] = {}
        for team in team_events.keys():
            pre_epas[str(team)] = self.pre_record_team(
                team, team_events[team], team_years[team]
            )
        match.pre_epas = pre_epas

        self.record_match(match, match_pred)
        if match.status == MatchStatus.UPCOMING:
            return

        attributions = self.attribute_match(match, red_pred, blue_pred)

        # Don't update if 1) placeholder match, 2) elim dq, 3) all fouls
        teams = set(match.get_red() + match.get_blue())
        placeholder_match = len(set(PLACEHOLDER_TEAMS).intersection(teams)) > 0
        elim_dq = match.elim and (
            len(match.get_red_dqs()) >= self.num_teams
            or len(match.get_blue_dqs()) >= self.num_teams
        )
        all_fouls = (
            match.blue_no_foul == 0
            and (match.blue_foul or 0) > 0
            and match.red_no_foul == 0
            and (match.red_foul or 0) > 0
        )
        skip_update = placeholder_match or elim_dq or all_fouls

        epas: Dict[str, Any] = {}
        for team, attr in attributions.items():
            if not skip_update:
                self.update_team(team, attr, match)
            epas[str(team)] = self.post_record_team(
                team, team_events[team], team_years[team]
            )
        match.epas = epas
