from collections import defaultdict
from typing import Dict

from src.classes import Attribution, Match, Pred, YearStats
from src.models.template import Model

import numpy as np


class EPA(Model):
    @staticmethod
    def sigmoid(x: float) -> float:
        return 1 / (1 + np.exp(-4 * (x - 0.5)))

    @staticmethod
    def percent_func(x: int) -> float:
        return min(0.5, max(0.3, 0.5 - 0.2 / 6 * (x - 6)))

    @staticmethod
    def margin_func(year: int, x: int) -> float:
        if year == 2015:
            return 0

        if year == 2018:
            return 1

        return min(1, max(0, 1 / 24 * (x - 12)))

    def start_season(self, stats: YearStats) -> None:
        super().start_season(stats)

        year, mean, sd = self.stats.year, self.stats.score_mean, self.stats.score_sd

        self.counts: Dict[int, int] = defaultdict(int)
        self.epa: Dict[int, float] = defaultdict(lambda: mean / 3 - 0.2 * sd)
        self.rp_1: Dict[int, float] = defaultdict(lambda: self.stats.rp_1_mean / 3)
        self.rp_2: Dict[int, float] = defaultdict(lambda: self.stats.rp_2_mean / 3)
        for team in set(self.end_ratings[year - 1]).union(self.end_ratings[year - 2]):
            year_1 = self.end_ratings[year - 1].get(team, 1500)
            year_2 = self.end_ratings[year - 2].get(team, 1500)
            old_epa = 0.7 * year_1 + 0.3 * year_2
            new_epa = 0.6 * old_epa + 0.4 * 1500
            self.epa[team] = mean / 3 + sd * (new_epa - 1500) / 250

    def predict_match(self, match: Match) -> Pred:
        red_epa = sum(self.epa[t] for t in match.red())
        blue_epa = sum(self.epa[t] for t in match.blue())

        K = 5 / 8
        norm_diff = (blue_epa - red_epa) / self.stats.score_sd
        win_prob = 1 / (1 + 10 ** (K * norm_diff))

        red_rp_1 = self.sigmoid(sum(self.rp_1[t] for t in match.red()))
        blue_rp_1 = self.sigmoid(sum(self.rp_1[t] for t in match.blue()))
        red_rp_2 = self.sigmoid(sum(self.rp_2[t] for t in match.red()))
        blue_rp_2 = self.sigmoid(sum(self.rp_2[t] for t in match.blue()))

        foul_rate = (
            self.stats.breakdown_mean["foul_points"]
            / self.stats.breakdown_mean["no_foul_points"]
        )

        return Pred(
            red_epa * (1 + foul_rate),
            blue_epa * (1 + foul_rate),
            win_prob,
            red_rp_1,
            blue_rp_1,
            red_rp_2,
            blue_rp_2,
        )

    def attribute_match(self, match: Match, pred: Pred) -> Dict[int, Attribution]:
        out: Dict[int, Attribution] = {}

        red_error = match.red_no_fouls - pred.red_score
        blue_error = match.blue_no_fouls - pred.blue_score

        red_rp_1_error = match.red_rp_1 - pred.red_rp_1
        blue_rp_1_error = match.blue_rp_1 - pred.blue_rp_1
        red_rp_2_error = match.red_rp_2 - pred.red_rp_2
        blue_rp_2_error = match.blue_rp_2 - pred.blue_rp_2

        for t in match.red():
            margin = self.margin_func(self.stats.year, self.counts[t])
            error = (red_error - margin * blue_error) / (1 + margin)
            out[t] = Attribution(
                self.epa[t] + error / 3,
                {
                    "rp_1": self.rp_1[t] + red_rp_1_error / 3,
                    "rp_2": self.rp_2[t] + red_rp_2_error / 3,
                },
            )

        for t in match.blue():
            margin = self.margin_func(self.stats.year, self.counts[t])
            error = (blue_error - margin * red_error) / (1 + margin)
            out[t] = Attribution(
                self.epa[t] + error / 3,
                {
                    "rp_1": self.rp_1[t] + blue_rp_1_error / 3,
                    "rp_2": self.rp_2[t] + blue_rp_2_error / 3,
                },
            )

        return out

    def update_team(self, team: int, attr: Attribution, match: Match) -> None:
        update = attr.contrib - self.epa[team]
        rp_1_update = attr.breakdown["rp_1"] - self.rp_1[team]
        rp_2_update = attr.breakdown["rp_2"] - self.rp_2[team]

        percent = self.percent_func(self.counts[team])
        weight = 1 / 3 if match.playoff else 1

        self.epa[team] += percent * weight * update

        if not match.playoff:
            self.rp_1[team] += 0.3 * weight * rp_1_update
            self.rp_2[team] += 0.3 * weight * rp_2_update

        self.counts[team] += 0 if match.playoff else 1

    def end_season(self) -> None:
        super().end_season()

        year, mean, sd = self.stats.year, self.stats.score_mean, self.stats.score_sd
        for team in self.epa:
            epa = 1500 + 250 * (self.epa[team] - mean / 3) / sd
            self.end_ratings[year][team] = epa
