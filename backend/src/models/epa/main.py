from collections import defaultdict
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

from src.db.models import Event, Match, TeamEvent, TeamMatch, TeamYear, Year
from src.models.epa.breakdown import (
    # get_pred_rps,
    get_score_from_breakdown,
    post_process_attrib,
    post_process_breakdown,
)
from src.models.epa.constants import ELIM_WEIGHT
from src.models.epa.init import get_init_epa
from src.models.epa.math import SkewNormal

# from src.models.epa.math import t_prob_gt_0
from src.models.template import Model
from src.models.types import AlliancePred, Attribution, MatchPred
from src.tba.breakdown import all_keys
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
        prev = min(0.5, max(0.3, 0.5 - 0.2 / 6 * (x - 6)))
        if year <= 2015:
            return 1 / 2 * prev
        return 2 / 3 * prev

    def start_season(
        self,
        year: Year,
        all_team_years: Dict[int, Dict[int, TeamYear]],
        team_years: Dict[str, TeamYear],
    ) -> None:
        super().start_season(year, all_team_years, team_years)
        self.k = EPA.k_func(self.year_num)

        init_rating = get_init_epa(year, None, None)
        self.epas: Dict[int, SkewNormal] = defaultdict(lambda: init_rating)
        self.counts: Dict[int, int] = defaultdict(int)

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
            # Records TeamYear EPA stats if no matches played yet
            self.post_record_team(num, None, None, team_year)

    def predict_match(
        self, match: Match, event: Event
    ) -> Tuple[float, AlliancePred, AlliancePred]:
        year, key, elim = self.year_num, match.key, match.elim
        # week = event.week
        # event_type = event.type

        rp_1s: List[float] = []
        rp_2s: List[float] = []
        rp_3s: List[float] = []

        breakdowns: List[Any] = []

        red_teams = match.get_red()[: self.num_teams]
        blue_teams = match.get_blue()[: self.num_teams]
        for teams, opp_teams in [(red_teams, blue_teams), (blue_teams, red_teams)]:
            pred_mean = np.array([self.epas[t].mean for t in teams]).sum(axis=0)  # type: ignore
            # pred_sd = np.array([np.sqrt(self.epas[t].var) for t in teams]).sum(axis=0)  # type: ignore
            opp_pred_mean = np.array([self.epas[t].mean for t in opp_teams]).sum(axis=0)  # type: ignore

            pred_mean = post_process_breakdown(year, key, pred_mean, opp_pred_mean)

            keys = all_keys[year]
            rp_1, rp_2, rp_3 = 0, 0, 0
            if year >= 2016:
                rp_1 = pred_mean[keys.index("rp_1")]
                rp_2 = pred_mean[keys.index("rp_2")]
                if year >= 2025:
                    rp_3 = pred_mean[keys.index("rp_3")]

            rp_1s.append(rp_1)
            rp_2s.append(rp_2)
            rp_3s.append(rp_3)

            breakdowns.append(pred_mean)

        red_score = get_score_from_breakdown(
            key, year, breakdowns[0], breakdowns[1], rp_1s[0], rp_2s[0], rp_3s[0], elim
        )

        blue_score = get_score_from_breakdown(
            key, year, breakdowns[1], breakdowns[0], rp_1s[1], rp_2s[1], rp_3s[1], elim
        )

        """
        # Assumes 100% correlation on each alliance
        red_sd = np.sum([np.sqrt(self.epas[t].var[0]) for t in red_teams])
        blue_sd = np.sum([np.sqrt(self.epas[t].var[0]) for t in blue_teams])
        # assume no correlation across alliances except in 2018
        corr = 0 if year != 2018 else 0.5
        total_sd = np.sqrt(red_sd**2 + blue_sd**2 + 2 * corr * red_sd * blue_sd)

        if year == 2018:
            # Your variance affects your score and your opponent's score
            total_sd *= 2

        avg_n = np.mean([self.epas[t].n for t in red_teams + blue_teams])

        win_prob = t_prob_gt_0(red_score - blue_score, total_sd, avg_n)
        """

        norm_diff = (red_score - blue_score) / self.year_obj.score_sd
        win_prob = 1 / (1 + 10 ** (self.k * norm_diff))

        foul_rate = self.year_obj.get_foul_rate()
        red_score_with_fouls = red_score * (1 + foul_rate)
        blue_score_with_fouls = blue_score * (1 + foul_rate)
        red_pred = AlliancePred(
            red_score_with_fouls, breakdowns[0], rp_1s[0], rp_2s[0], rp_3s[0]
        )
        blue_pred = AlliancePred(
            blue_score_with_fouls, breakdowns[1], rp_1s[1], rp_2s[1], rp_3s[1]
        )

        return win_prob, red_pred, blue_pred

    def attribute_match(
        self,
        match: Match,
        red_pred: AlliancePred,
        blue_pred: AlliancePred,
    ) -> Dict[int, Attribution]:
        out: Dict[int, Attribution] = {}

        red_bd, blue_bd = match.get_breakdowns()
        red_teams = match.get_red()[: self.num_teams]
        blue_teams = match.get_blue()[: self.num_teams]
        for teams, bd, pred_bd, opp_bd, opp_pred_bd in [
            (red_teams, red_bd, red_pred.breakdown, blue_bd, blue_pred.breakdown),
            (blue_teams, blue_bd, blue_pred.breakdown, red_bd, red_pred.breakdown),
        ]:
            my_err = bd - pred_bd
            opp_err = opp_bd - opp_pred_bd
            for t in teams:
                margin = EPA.margin_func(self.year_num, self.counts[t])
                err = (my_err - margin * opp_err) / (1 + margin)
                attrib = post_process_attrib(
                    self.year_obj, self.epas[t].mean, err / self.num_teams, match.elim
                )
                out[t] = Attribution(attrib)

        return out

    def update_team(
        self, team: int, attrib: Attribution, match: Match, team_match: TeamMatch
    ) -> None:
        weight = ELIM_WEIGHT if match.elim else 1
        percent = EPA.percent_func(self.year_num, self.counts[team])
        self.epas[team].add_obs(attrib.epa, percent, weight)
        if not match.elim:
            self.counts[team] += 1

    def pre_record_team(self, team: int, tm: TeamMatch, te: TeamEvent, ty: TeamYear):
        rounded_mean: Any = np.round(self.epas[team].mean, 2)
        tm.epa = rounded_mean[0]

        if self.year_num >= 2016:
            tm.auto_epa = rounded_mean[1]
            tm.teleop_epa = rounded_mean[2]
            tm.endgame_epa = rounded_mean[3]
            tm.rp_1_epa = round(self.epas[team].mean[4], 4)
            tm.rp_2_epa = round(self.epas[team].mean[5], 4)
            tm.rp_3_epa = round(self.epas[team].mean[6], 4)
            tm.tiebreaker_epa = rounded_mean[7]
            for i in range(1, 19):
                new_value = rounded_mean[i + 7]
                setattr(tm, f"comp_{i}_epa", new_value)

    def post_record_team(
        self,
        team: int,
        tm: Optional[TeamMatch],
        te: Optional[TeamEvent],
        ty: Optional[TeamYear],
    ):
        rounded_mean: Any = np.round(self.epas[team].mean, 2)
        rounded_sd: Any = np.round(np.sqrt(self.epas[team].var), 2)

        if tm is not None:
            tm.post_epa = rounded_mean[0]

        if te is not None:
            te.epa = rounded_mean[0]
            te.epa_sd = rounded_sd[0]
            te.epa_skew = r(self.epas[team].skew, 4)
            te.epa_n = r(self.epas[team].n, 4)

            if self.year_num >= 2016:
                te.auto_epa = rounded_mean[1]
                te.teleop_epa = rounded_mean[2]
                te.endgame_epa = rounded_mean[3]
                te.rp_1_epa = round(self.epas[team].mean[4], 4)
                te.rp_2_epa = round(self.epas[team].mean[5], 4)
                te.rp_3_epa = round(self.epas[team].mean[6], 4)
                te.tiebreaker_epa = rounded_mean[7]
                for i in range(1, 19):
                    setattr(te, f"comp_{i}_epa", rounded_mean[i + 7])

        if ty is not None:
            ty.epa = rounded_mean[0]
            ty.epa_sd = rounded_sd[0]
            ty.epa_skew = r(self.epas[team].skew, 4)
            ty.epa_n = r(self.epas[team].n, 4)

            if self.year_num >= 2016:
                ty.auto_epa = rounded_mean[1]
                ty.teleop_epa = rounded_mean[2]
                ty.endgame_epa = rounded_mean[3]
                ty.rp_1_epa = round(self.epas[team].mean[4], 4)
                ty.rp_2_epa = round(self.epas[team].mean[5], 4)
                ty.rp_3_epa = round(self.epas[team].mean[6], 5)
                ty.tiebreaker_epa = rounded_mean[7]
                for i in range(1, 19):
                    setattr(ty, f"comp_{i}_epa", rounded_mean[i + 7])

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
            if self.year_num >= 2025:
                match.epa_red_rp_3_pred = r(match_pred.red_rp_3 or 0, 4)
                match.epa_blue_rp_3_pred = r(match_pred.blue_rp_3 or 0, 4)
