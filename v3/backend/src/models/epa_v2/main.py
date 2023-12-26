from collections import defaultdict
from typing import Any, Dict, List, Tuple

import numpy as np

from src.types.enums import MatchWinner
from src.db.models import TeamYear, Year, Match, TeamMatch, Alliance, TeamEvent
from src.models.types import Attribution, AlliancePred, MatchPred
from src.models.epa_v2.breakdown import (
    # get_pred_rps,
    get_score_from_breakdown,
    post_process_attrib,
    post_process_breakdown,
)
from src.models.template import Model
from src.epa.main import k_func
from src.epa.init import get_init_epa
from src.epa.types import Rating


class EPAV2(Model):
    @staticmethod
    def percent_func(x: int) -> float:
        return min(0.5, max(0.3, 0.5 - 0.2 / 6 * (x - 6)))

    def start_season(
        self,
        year: Year,
        all_team_years: Dict[int, Dict[str, TeamYear]],
        team_years: Dict[str, TeamYear],
    ) -> None:
        super().start_season(year, all_team_years, team_years)

        self.year = year
        year_num = year.year

        init_rating = get_init_epa(year, None, None)
        self.counts: Dict[str, int] = defaultdict(int)
        self.epas: Dict[str, Rating] = defaultdict(lambda: init_rating)

        for team_year in team_years.values():
            num = team_year.team

            past_team_years: List[TeamYear] = []
            for past_year in range(year_num - 1, year_num - 5, -1):
                past_team_year = all_team_years.get(past_year, {}).get(num, None)
                if past_team_year is not None:
                    past_team_years.append(past_team_year)

            past_team_year_1 = past_team_years[0] if len(past_team_years) > 0 else None
            past_team_year_2 = past_team_years[1] if len(past_team_years) > 1 else None

            rating = get_init_epa(year, past_team_year_1, past_team_year_2)

            self.epas[num] = rating
            team_year.epa_start = round(rating.epa.mean[0], 2)

    def predict_match(self, match: Match) -> Tuple[float, AlliancePred, AlliancePred]:
        year_obj = self.year
        year_num = year_obj.year

        rp_1s: List[float] = []
        rp_2s: List[float] = []
        breakdowns: List[Any] = []

        for teams, opp_teams in [
            (match.get_red(), match.get_blue()),
            (match.get_blue(), match.get_red()),
        ]:
            pred_mean = np.array([self.epas[t].epa.mean for t in teams]).sum(axis=0)  # type: ignore
            # pred_sd = np.array([np.sqrt(self.epas[t].epa.var) for t in teams]).sum(axis=0)  # type: ignore
            opp_pred_mean = np.array([self.epas[t].epa.mean for t in opp_teams]).sum(axis=0)  # type: ignore

            pred_mean = post_process_breakdown(
                year_num, match.key, pred_mean, opp_pred_mean
            )
            pred_rp_1, pred_rp_2 = (
                0,
                0,
            )  # get_pred_rps(year, match.week, pred_mean, pred_sd)

            rp_1s.append(pred_rp_1)
            rp_2s.append(pred_rp_2)
            breakdowns.append(pred_mean)

        elim = match.elim

        red_score = get_score_from_breakdown(
            year_num, breakdowns[0], breakdowns[1], rp_1s[0], rp_2s[0], elim
        )

        blue_score = get_score_from_breakdown(
            year_num, breakdowns[1], breakdowns[0], rp_1s[1], rp_2s[1], elim
        )

        # # Could also use variance to get win probability
        # # But this is simpler, less noisy, and more tested

        K = k_func(year_num)
        norm_diff = (blue_score - red_score) / self.year.score_sd
        win_prob = 1 / (1 + 10 ** (K * norm_diff))

        foul_rate = year_obj.get_foul_rate()
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

        year = self.year.year
        red_bd = red_alliance.get_breakdown()
        blue_bd = blue_alliance.get_breakdown()
        for teams, bd, pred_bd in [
            (red_alliance.get_teams(), red_bd, red_pred.breakdown),
            (blue_alliance.get_teams(), blue_bd, blue_pred.breakdown),
        ]:
            for t in teams:
                attrib = self.epas[t].epa.mean + (bd - pred_bd) / 3
                attrib = post_process_attrib(
                    year, self.epas[t].epa.mean, attrib, match.elim
                )
                out[t] = Attribution(attrib)

        return out

    def update_team(
        self, team: str, attrib: Attribution, match: Match, team_match: TeamMatch
    ) -> None:
        weight = 1 / 3 if match.elim else 1
        percent = self.percent_func(self.counts[team])
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
        team_match.epa = round(self.epas[team].epa.mean[0], 2)

        if team_match.year >= 2016:
            team_match.auto_epa = round(self.epas[team].epa.mean[1], 2)
            team_match.teleop_epa = round(self.epas[team].epa.mean[2], 2)
            team_match.endgame_epa = round(self.epas[team].epa.mean[3], 2)
            team_match.tiebreaker_epa = round(self.epas[team].epa.mean[4], 2)
            team_match.comp_1_epa = round(self.epas[team].epa.mean[5], 2)
            team_match.comp_2_epa = round(self.epas[team].epa.mean[6], 2)
            team_match.comp_3_epa = round(self.epas[team].epa.mean[7], 2)
            team_match.comp_4_epa = round(self.epas[team].epa.mean[8], 2)
            team_match.comp_5_epa = round(self.epas[team].epa.mean[9], 2)
            team_match.comp_6_epa = round(self.epas[team].epa.mean[10], 2)
            team_match.comp_7_epa = round(self.epas[team].epa.mean[11], 2)
            team_match.comp_8_epa = round(self.epas[team].epa.mean[12], 2)
            team_match.comp_9_epa = round(self.epas[team].epa.mean[13], 2)
            team_match.comp_10_epa = round(self.epas[team].epa.mean[14], 2)
            team_match.comp_11_epa = round(self.epas[team].epa.mean[15], 2)
            team_match.comp_12_epa = round(self.epas[team].epa.mean[16], 2)

    def post_record_team(
        self,
        team: str,
        team_match: TeamMatch,
        team_event: TeamEvent,
        team_year: TeamYear,
    ):
        team_match.post_epa = round(self.epas[team].epa.mean[0], 2)

        team_event.epa = round(self.epas[team].epa.mean[0], 2)
        team_event.epa_sd = round(np.sqrt(self.epas[team].epa.var[0]), 2)
        team_event.epa_skew = round(self.epas[team].epa.skew, 4)

        team_year.epa = round(self.epas[team].epa.mean[0], 2)
        team_year.epa_sd = round(np.sqrt(self.epas[team].epa.var[0]), 2)
        team_year.epa_skew = round(self.epas[team].epa.skew, 4)

        if team_match.year >= 2016:
            team_event.auto_epa = round(self.epas[team].epa.mean[1], 2)
            team_event.auto_epa_sd = round(np.sqrt(self.epas[team].epa.var[1]), 2)
            team_event.teleop_epa = round(self.epas[team].epa.mean[2], 2)
            team_event.teleop_epa_sd = round(np.sqrt(self.epas[team].epa.var[2]), 2)
            team_event.endgame_epa = round(self.epas[team].epa.mean[3], 2)
            team_event.endgame_epa_sd = round(np.sqrt(self.epas[team].epa.var[3]), 2)
            team_event.tiebreaker_epa = round(self.epas[team].epa.mean[4], 2)
            team_event.tiebreaker_epa_sd = round(np.sqrt(self.epas[team].epa.var[4]), 2)
            team_event.comp_1_epa = round(self.epas[team].epa.mean[5], 2)
            team_event.comp_1_epa_sd = round(np.sqrt(self.epas[team].epa.var[5]), 2)
            team_event.comp_2_epa = round(self.epas[team].epa.mean[6], 2)
            team_event.comp_2_epa_sd = round(np.sqrt(self.epas[team].epa.var[6]), 2)
            team_event.comp_3_epa = round(self.epas[team].epa.mean[7], 2)
            team_event.comp_3_epa_sd = round(np.sqrt(self.epas[team].epa.var[7]), 2)
            team_event.comp_4_epa = round(self.epas[team].epa.mean[8], 2)
            team_event.comp_4_epa_sd = round(np.sqrt(self.epas[team].epa.var[8]), 2)
            team_event.comp_5_epa = round(self.epas[team].epa.mean[9], 2)
            team_event.comp_5_epa_sd = round(np.sqrt(self.epas[team].epa.var[9]), 2)
            team_event.comp_6_epa = round(self.epas[team].epa.mean[10], 2)
            team_event.comp_6_epa_sd = round(np.sqrt(self.epas[team].epa.var[10]), 2)
            team_event.comp_7_epa = round(self.epas[team].epa.mean[11], 2)
            team_event.comp_7_epa_sd = round(np.sqrt(self.epas[team].epa.var[11]), 2)
            team_event.comp_8_epa = round(self.epas[team].epa.mean[12], 2)
            team_event.comp_8_epa_sd = round(np.sqrt(self.epas[team].epa.var[12]), 2)
            team_event.comp_9_epa = round(self.epas[team].epa.mean[13], 2)
            team_event.comp_9_epa_sd = round(np.sqrt(self.epas[team].epa.var[13]), 2)
            team_event.comp_10_epa = round(self.epas[team].epa.mean[14], 2)
            team_event.comp_10_epa_sd = round(np.sqrt(self.epas[team].epa.var[14]), 2)
            team_event.comp_11_epa = round(self.epas[team].epa.mean[15], 2)
            team_event.comp_11_epa_sd = round(np.sqrt(self.epas[team].epa.var[15]), 2)
            team_event.comp_12_epa = round(self.epas[team].epa.mean[16], 2)
            team_event.comp_12_epa_sd = round(np.sqrt(self.epas[team].epa.var[16]), 2)

            team_year.auto_epa = round(self.epas[team].epa.mean[1], 2)
            team_year.auto_epa_sd = round(np.sqrt(self.epas[team].epa.var[1]), 2)
            team_year.teleop_epa = round(self.epas[team].epa.mean[2], 2)
            team_year.teleop_epa_sd = round(np.sqrt(self.epas[team].epa.var[2]), 2)
            team_year.endgame_epa = round(self.epas[team].epa.mean[3], 2)
            team_year.endgame_epa_sd = round(np.sqrt(self.epas[team].epa.var[3]), 2)
            team_year.tiebreaker_epa = round(self.epas[team].epa.mean[4], 2)
            team_year.tiebreaker_epa_sd = round(np.sqrt(self.epas[team].epa.var[4]), 2)
            team_year.comp_1_epa = round(self.epas[team].epa.mean[5], 2)
            team_year.comp_1_epa_sd = round(np.sqrt(self.epas[team].epa.var[5]), 2)
            team_year.comp_2_epa = round(self.epas[team].epa.mean[6], 2)
            team_year.comp_2_epa_sd = round(np.sqrt(self.epas[team].epa.var[6]), 2)
            team_year.comp_3_epa = round(self.epas[team].epa.mean[7], 2)
            team_year.comp_3_epa_sd = round(np.sqrt(self.epas[team].epa.var[7]), 2)
            team_year.comp_4_epa = round(self.epas[team].epa.mean[8], 2)
            team_year.comp_4_epa_sd = round(np.sqrt(self.epas[team].epa.var[8]), 2)
            team_year.comp_5_epa = round(self.epas[team].epa.mean[9], 2)
            team_year.comp_5_epa_sd = round(np.sqrt(self.epas[team].epa.var[9]), 2)
            team_year.comp_6_epa = round(self.epas[team].epa.mean[10], 2)
            team_year.comp_6_epa_sd = round(np.sqrt(self.epas[team].epa.var[10]), 2)
            team_year.comp_7_epa = round(self.epas[team].epa.mean[11], 2)
            team_year.comp_7_epa_sd = round(np.sqrt(self.epas[team].epa.var[11]), 2)
            team_year.comp_8_epa = round(self.epas[team].epa.mean[12], 2)
            team_year.comp_8_epa_sd = round(np.sqrt(self.epas[team].epa.var[12]), 2)
            team_year.comp_9_epa = round(self.epas[team].epa.mean[13], 2)
            team_year.comp_9_epa_sd = round(np.sqrt(self.epas[team].epa.var[13]), 2)
            team_year.comp_10_epa = round(self.epas[team].epa.mean[14], 2)
            team_year.comp_10_epa_sd = round(np.sqrt(self.epas[team].epa.var[14]), 2)
            team_year.comp_11_epa = round(self.epas[team].epa.mean[15], 2)
            team_year.comp_11_epa_sd = round(np.sqrt(self.epas[team].epa.var[15]), 2)
            team_year.comp_12_epa = round(self.epas[team].epa.mean[16], 2)
            team_year.comp_12_epa_sd = round(np.sqrt(self.epas[team].epa.var[16]), 2)

    def record_match(self, match: Match, match_pred: MatchPred) -> None:
        match.epa_win_prob = round(match_pred.win_prob, 4)
        match.epa_winner = (
            MatchWinner.RED if match_pred.win_prob >= 0.5 else MatchWinner.BLUE
        )

        match.epa_red_score_pred = round(match_pred.red_score, 2)
        match.epa_blue_score_pred = round(match_pred.blue_score, 2)

        if self.year.year >= 2016:
            match.epa_red_rp_1_pred = round(match_pred.red_rp_1 or 0, 4)
            match.epa_blue_rp_1_pred = round(match_pred.blue_rp_1 or 0, 4)
            match.epa_red_rp_2_pred = round(match_pred.red_rp_2 or 0, 4)
            match.epa_blue_rp_2_pred = round(match_pred.blue_rp_2 or 0, 4)
