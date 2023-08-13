from collections import defaultdict
from typing import Dict

import numpy as np

from src.classes import Attribution, Match, Pred, YearStats
from src.models.template import Model


class Elo(Model):
    @staticmethod
    def sigmoid(x: float) -> float:
        return 1 / (1 + np.exp(-4 * (x - 0.5)))

    def start_season(self, stats: YearStats) -> None:
        super().start_season(stats)

        year, mean, sd = self.stats.year, self.stats.score_mean, self.stats.score_sd

        self.elo: Dict[int, float] = defaultdict(lambda: mean / 3)
        self.rp_1: Dict[int, float] = defaultdict(lambda: self.stats.rp_1_mean / 3)
        self.rp_2: Dict[int, float] = defaultdict(lambda: self.stats.rp_2_mean / 3)
        for team in set(self.end_ratings[year - 1]).union(self.end_ratings[year - 2]):
            year_1 = self.end_ratings[year - 1].get(team, 1500)
            year_2 = self.end_ratings[year - 2].get(team, 1500)
            old_elo = 0.7 * year_1 + 0.3 * year_2
            new_elo = 0.8 * old_elo + 0.2 * 1500
            self.elo[team] = mean / 3 + sd * (new_elo - 1500) / 250

    def predict_match(self, match: Match) -> Pred:
        red_elo = sum(self.elo[t] for t in match.red())
        blue_elo = sum(self.elo[t] for t in match.blue())

        K = 5 / 8
        norm_diff = (blue_elo - red_elo) / self.stats.score_sd
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
            red_elo * (1 + foul_rate),
            blue_elo * (1 + foul_rate),
            win_prob,
            red_rp_1,
            blue_rp_1,
            red_rp_2,
            blue_rp_2,
        )

    def attribute_match(self, match: Match, pred: Pred) -> Dict[int, Attribution]:
        out: Dict[int, Attribution] = {}

        pred_diff = pred.red_score - pred.blue_score
        actual_diff = match.red_no_fouls - match.blue_no_fouls
        error = actual_diff - pred_diff

        red_rp_1_error = match.red_rp_1 - pred.red_rp_1
        blue_rp_1_error = match.blue_rp_1 - pred.blue_rp_1
        red_rp_2_error = match.red_rp_2 - pred.red_rp_2
        blue_rp_2_error = match.blue_rp_2 - pred.blue_rp_2

        for t in match.red():
            out[t] = Attribution(
                self.elo[t] + error / 6,
                {
                    "rp_1": self.rp_1[t] + red_rp_1_error / 3,
                    "rp_2": self.rp_2[t] + red_rp_2_error / 3,
                },
            )

        for t in match.blue():
            out[t] = Attribution(
                self.elo[t] - error / 6,
                {
                    "rp_1": self.rp_1[t] + blue_rp_1_error / 3,
                    "rp_2": self.rp_2[t] + blue_rp_2_error / 3,
                },
            )

        return out

    def update_team(self, team: int, attrib: Attribution, match: Match) -> None:
        update = attrib.contrib - self.elo[team]
        rp_1_update = attrib.breakdown["rp_1"] - self.rp_1[team]
        rp_2_update = attrib.breakdown["rp_2"] - self.rp_2[team]

        weight = 1 / 3 if match.playoff else 1

        self.elo[team] += 72 / 250 * weight * update

        if not match.playoff:
            self.rp_1[team] += 72 / 250 * weight * rp_1_update
            self.rp_2[team] += 72 / 250 * weight * rp_2_update

    def end_season(self) -> None:
        super().end_season()

        year, mean, sd = self.stats.year, self.stats.score_mean, self.stats.score_sd
        for team in self.elo:
            elo = 1500 + 250 * (self.elo[team] - mean / 3) / sd
            self.end_ratings[year][team] = elo
