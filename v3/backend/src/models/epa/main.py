from collections import defaultdict
from typing import Any, Dict, List, Tuple

import numpy as np

from src.db.models import Alliance, Match, TeamEvent, TeamMatch, TeamYear, Year
from src.models.epa.breakdown import (
    get_pred_rps,
    get_score_from_breakdown,
    post_process_attrib,
    post_process_breakdown,
)
from src.models.epa.constants import ELIM_WEIGHT
from src.models.epa.init import get_init_epa
from src.models.epa.math import SkewNormal
from src.models.template import Model
from src.models.types import AlliancePred, Attribution, MatchPred
from src.types.enums import MatchWinner
from src.utils.utils import r


class EPA(Model):
    k: float

    @staticmethod
    def k_func(year: int) -> float:
        return -5 / 8 if year >= 2008 else -5 / 12

    @staticmethod
    def margin_func(year: int, x: int) -> float:
        if year in [2002, 2003]:
            return 1
        return 0

    @staticmethod
    def percent_func(year: int, x: int) -> float:
        if year <= 2010:
            return 0.3
        return min(0.5, max(0.3, 0.5 - 0.2 / 6 * (x - 6)))

    def start_season(
        self,
        year: Year,
        all_team_years: Dict[int, Dict[str, TeamYear]],
        team_years: Dict[str, TeamYear],
    ) -> None:
        super().start_season(year, all_team_years, team_years)
        self.k = EPA.k_func(self.year_num)

        init_rating = get_init_epa(year, None, None)
        self.epas: Dict[str, SkewNormal] = defaultdict(lambda: init_rating)
        self.counts: Dict[str, int] = defaultdict(int)

        for team_year in team_years.values():
            num = team_year.team

            past_team_years: List[TeamYear] = []
            for past_year in range(self.year_num - 1, self.year_num - 5, -1):
                past_team_year = all_team_years.get(past_year, {}).get(num, None)
                if past_team_year is not None:
                    past_team_years.append(past_team_year)

            past_team_year_1 = past_team_years[0] if len(past_team_years) > 0 else None
            past_team_year_2 = past_team_years[1] if len(past_team_years) > 1 else None

            rating = get_init_epa(year, past_team_year_1, past_team_year_2)

            self.epas[num] = rating
            team_year.epa_start = r(rating.mean[0], 2)

    def predict_match(self, match: Match) -> Tuple[float, AlliancePred, AlliancePred]:
        rp_1s: List[float] = []  # TODO: refactor
        rp_2s: List[float] = []
        breakdowns: List[Any] = []

        red_teams = match.get_red()[: self.num_teams]
        blue_teams = match.get_blue()[: self.num_teams]
        for teams, opp_teams in [(red_teams, blue_teams), (blue_teams, red_teams)]:
            pred_mean = np.array([self.epas[t].mean for t in teams]).sum(axis=0)  # type: ignore
            pred_sd = np.array([np.sqrt(self.epas[t].var) for t in teams]).sum(axis=0)  # type: ignore
            opp_pred_mean = np.array([self.epas[t].mean for t in opp_teams]).sum(axis=0)  # type: ignore

            pred_mean = post_process_breakdown(
                self.year_num, match.key, pred_mean, opp_pred_mean
            )

            rp_1, rp_2 = get_pred_rps(self.year_num, match.week, pred_mean, pred_sd)

            rp_1s.append(rp_1)
            rp_2s.append(rp_2)
            breakdowns.append(pred_mean)

        elim = match.elim

        red_score = get_score_from_breakdown(
            match.key,
            self.year_num,
            breakdowns[0],
            breakdowns[1],
            rp_1s[0],
            rp_2s[0],
            elim,
        )

        blue_score = get_score_from_breakdown(
            match.key,
            self.year_num,
            breakdowns[1],
            breakdowns[0],
            rp_1s[1],
            rp_2s[1],
            elim,
        )

        # Could also use variance to get win probability
        # But this is simpler, less noisy, and more tested
        # TODO: try to use variance to get win probability

        norm_diff = (red_score - blue_score) / self.year_obj.score_sd
        win_prob = 1 / (1 + 10 ** (self.k * norm_diff))

        foul_rate = self.year_obj.get_foul_rate()
        red_score_with_fouls = red_score * (1 + foul_rate)
        blue_score_with_fouls = blue_score * (1 + foul_rate)
        red_pred = AlliancePred(red_score_with_fouls, breakdowns[0], rp_1s[0], rp_2s[0])
        blue_pred = AlliancePred(
            blue_score_with_fouls, breakdowns[1], rp_1s[1], rp_2s[1]
        )

        return win_prob, red_pred, blue_pred

    def attribute_match(
        self,
        match: Match,
        red_alliance: Alliance,
        blue_alliance: Alliance,
        red_pred: AlliancePred,
        blue_pred: AlliancePred,
    ) -> Dict[str, Attribution]:
        out: Dict[str, Attribution] = {}

        red_bd = red_alliance.get_breakdown()
        blue_bd = blue_alliance.get_breakdown()
        red_teams = red_alliance.get_teams()[: self.num_teams]
        blue_teams = blue_alliance.get_teams()[: self.num_teams]
        for teams, bd, pred_bd, opp_bd, opp_pred_bd in [
            (red_teams, red_bd, red_pred.breakdown, blue_bd, blue_pred.breakdown),
            (blue_teams, blue_bd, blue_pred.breakdown, red_bd, red_pred.breakdown),
        ]:
            my_err = bd - pred_bd
            opp_err = opp_bd - opp_pred_bd
            for t in teams:
                margin = EPA.margin_func(self.year_num, self.counts[t])
                err = (my_err - margin * opp_err) / (1 + margin)
                attrib = self.epas[t].mean + err / self.num_teams
                attrib = post_process_attrib(
                    self.year_obj, self.epas[t].mean, attrib, match.elim
                )
                out[t] = Attribution(attrib)

        return out

    def update_team(
        self, team: str, attrib: Attribution, match: Match, team_match: TeamMatch
    ) -> None:
        weight = ELIM_WEIGHT if match.elim else 1
        percent = EPA.percent_func(self.year_num, self.counts[team])
        alpha = percent * weight

        self.epas[team].add_obs(attrib.epa, alpha)
        if not match.elim:
            self.counts[team] += 1

    def pre_record_team(
        self,
        team: str,
        team_match: TeamMatch,
        team_event: TeamEvent,
        team_year: TeamYear,
    ):
        team_match.epa = r(self.epas[team].mean[0], 2)

        if self.year_num >= 2016:
            team_match.auto_epa = r(self.epas[team].mean[1], 2)
            team_match.teleop_epa = r(self.epas[team].mean[2], 2)
            team_match.endgame_epa = r(self.epas[team].mean[3], 2)
            team_match.tiebreaker_epa = r(self.epas[team].mean[4], 2)
            for i in range(1, 19):
                new_value = r(self.epas[team].mean[i + 4], 2)
                setattr(team_match, f"comp_{i}_epa", new_value)

    def post_record_team(
        self,
        team: str,
        team_match: TeamMatch,
        team_event: TeamEvent,
        team_year: TeamYear,
    ):
        # TODO: refactor to vectorize
        team_match.post_epa = r(self.epas[team].mean[0], 2)

        team_event.epa = r(self.epas[team].mean[0], 2)
        team_event.epa_sd = r(np.sqrt(self.epas[team].var[0]), 2)
        team_event.epa_skew = r(self.epas[team].skew, 4)

        team_year.epa = r(self.epas[team].mean[0], 2)
        team_year.epa_sd = r(np.sqrt(self.epas[team].var[0]), 2)
        team_year.epa_skew = r(self.epas[team].skew, 4)

        if self.year_num >= 2016:
            team_event.auto_epa = r(self.epas[team].mean[1], 2)
            team_event.auto_epa_sd = r(np.sqrt(self.epas[team].var[1]), 2)
            team_event.teleop_epa = r(self.epas[team].mean[2], 2)
            team_event.teleop_epa_sd = r(np.sqrt(self.epas[team].var[2]), 2)
            team_event.endgame_epa = r(self.epas[team].mean[3], 2)
            team_event.endgame_epa_sd = r(np.sqrt(self.epas[team].var[3]), 2)
            team_event.rp_1_epa = r(self.epas[team].mean[4], 2)
            team_event.rp_1_epa_sd = r(np.sqrt(self.epas[team].var[4]), 2)
            team_event.rp_2_epa = r(self.epas[team].mean[5], 2)
            team_event.rp_2_epa_sd = r(np.sqrt(self.epas[team].var[5]), 2)
            team_event.tiebreaker_epa = r(self.epas[team].mean[6], 2)
            team_event.tiebreaker_epa_sd = r(np.sqrt(self.epas[team].var[6]), 2)
            for i in range(1, 19):
                new_value = r(self.epas[team].mean[i + 6], 2)
                setattr(team_event, f"comp_{i}_epa", new_value)
                new_sd = r(np.sqrt(self.epas[team].var[i + 6]), 2)
                setattr(team_event, f"comp_{i}_epa_sd", new_sd)

            team_year.auto_epa = r(self.epas[team].mean[1], 2)
            team_year.auto_epa_sd = r(np.sqrt(self.epas[team].var[1]), 2)
            team_year.teleop_epa = r(self.epas[team].mean[2], 2)
            team_year.teleop_epa_sd = r(np.sqrt(self.epas[team].var[2]), 2)
            team_year.endgame_epa = r(self.epas[team].mean[3], 2)
            team_year.endgame_epa_sd = r(np.sqrt(self.epas[team].var[3]), 2)
            team_year.rp_1_epa = r(self.epas[team].mean[4], 2)
            team_year.rp_1_epa_sd = r(np.sqrt(self.epas[team].var[4]), 2)
            team_year.rp_2_epa = r(self.epas[team].mean[5], 2)
            team_year.rp_2_epa_sd = r(np.sqrt(self.epas[team].var[5]), 2)
            team_year.tiebreaker_epa = r(self.epas[team].mean[6], 2)
            team_year.tiebreaker_epa_sd = r(np.sqrt(self.epas[team].var[6]), 2)
            for i in range(1, 19):
                new_value = r(self.epas[team].mean[i + 6], 2)
                setattr(team_year, f"comp_{i}_epa", new_value)
                new_sd = r(np.sqrt(self.epas[team].var[i + 6]), 2)
                setattr(team_year, f"comp_{i}_epa_sd", new_sd)

    def record_match(self, match: Match, match_pred: MatchPred) -> None:
        match.epa_win_prob = r(match_pred.win_prob, 4)
        match.epa_winner = (
            MatchWinner.RED if match_pred.win_prob >= 0.5 else MatchWinner.BLUE
        )

        match.epa_red_score_pred = r(match_pred.red_score, 2)
        match.epa_blue_score_pred = r(match_pred.blue_score, 2)

        if self.year_num >= 2016:
            match.epa_red_rp_1_pred = r(match_pred.red_rp_1 or 0, 4)
            match.epa_blue_rp_1_pred = r(match_pred.blue_rp_1 or 0, 4)
            match.epa_red_rp_2_pred = r(match_pred.red_rp_2 or 0, 4)
            match.epa_blue_rp_2_pred = r(match_pred.blue_rp_2 or 0, 4)
