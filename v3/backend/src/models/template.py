from typing import Dict, Tuple

from src.models.types import Attribution, MatchPred, AlliancePred
from src.db.models import Year, TeamYear, Match, Alliance, TeamMatch, TeamEvent


class Model:
    def __init__(self):
        pass

    def start_season(
        self,
        year: Year,
        all_team_years: Dict[int, Dict[str, TeamYear]],
        team_years: Dict[str, TeamYear],
    ) -> None:
        pass

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
        for team, attr in attributions.items():
            team_match = team_matches[team]
            team_event = team_events[team]
            team_year = team_years[team]
            self.pre_record_team(team, team_match, team_event, team_year)
            self.update_team(team, attr, match, team_match)
            self.post_record_team(team, team_match, team_event, team_year)

        self.record_match(match, match_pred)

    def end_season(self, year: Year, team_years: Dict[str, TeamYear]) -> None:
        pass
