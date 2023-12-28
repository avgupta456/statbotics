from typing import Dict, Tuple

from src.db.models import Alliance, Match, TeamEvent, TeamMatch, TeamYear, Year
from src.models.types import AlliancePred, Attribution, MatchPred
from src.tba.constants import PLACEHOLDER_TEAMS


class Model:
    year_obj: Year
    year_num: int
    num_teams: int

    def __init__(self):
        pass

    def start_season(
        self,
        year: Year,
        all_team_years: Dict[int, Dict[str, TeamYear]],
        team_years: Dict[str, TeamYear],
    ) -> None:
        self.year_obj = year
        self.year_num = year.year
        self.num_teams = 2 if year.year <= 2004 else 3

    def predict_match(self, match: Match) -> Tuple[float, AlliancePred, AlliancePred]:
        raise NotImplementedError

    def attribute_match(
        self,
        match: Match,
        red_alliance: Alliance,
        blue_alliance: Alliance,
        red_pred: AlliancePred,
        blue_pred: AlliancePred,
    ) -> Dict[str, Attribution]:
        raise NotImplementedError

    def update_team(
        self, team: str, attrib: Attribution, match: Match, team_match: TeamMatch
    ) -> None:
        raise NotImplementedError

    def pre_record_team(
        self,
        team: str,
        team_match: TeamMatch,
        team_event: TeamEvent,
        team_year: TeamYear,
    ) -> None:
        pass

    def post_record_team(
        self,
        team: str,
        team_match: TeamMatch,
        team_event: TeamEvent,
        team_year: TeamYear,
    ) -> None:
        pass

    def record_match(self, match: Match, match_pred: MatchPred) -> None:
        pass

    def process_match(
        self,
        match: Match,
        red_alliance: Alliance,
        blue_alliance: Alliance,
        team_matches: Dict[str, TeamMatch],
        team_events: Dict[str, TeamEvent],
        team_years: Dict[str, TeamYear],
    ):
        win_prob, red_pred, blue_pred = self.predict_match(match)
        match_pred = MatchPred(win_prob, red_pred, blue_pred)

        attributions = self.attribute_match(
            match, red_alliance, blue_alliance, red_pred, blue_pred
        )

        # Don't update if 1) placeholder match, 2) elim dq, 3) offseason
        teams = set(match.get_red() + match.get_blue())
        placeholder_match = len(set(PLACEHOLDER_TEAMS).intersection(teams)) > 0
        elim_dq = match.elim and (
            len(match.get_red_dqs()) >= self.num_teams
            or len(match.get_blue_dqs()) >= self.num_teams
        )
        skip_update = placeholder_match or elim_dq or match.offseason

        for team, attr in attributions.items():
            team_match = team_matches[team]
            team_event = team_events[team]
            team_year = team_years[team]
            self.pre_record_team(team, team_match, team_event, team_year)
            if not skip_update:
                self.update_team(team, attr, match, team_match)
            self.post_record_team(team, team_match, team_event, team_year)

        self.record_match(match, match_pred)

    def end_season(self, year: Year, team_years: Dict[str, TeamYear]) -> None:
        pass
