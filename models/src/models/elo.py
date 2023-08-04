from typing import Dict
from collections import defaultdict

from src.models.template import Model
from src.classes import Match, Pred, Attribution, YearStats


class Elo(Model):
    def start_season(self, stats: YearStats) -> None:
        super().start_season(stats)

        year, mean, sd = self.stats.year, self.stats.score_mean, self.stats.score_sd

        self.elo: Dict[int, float] = defaultdict(lambda: mean / 3)
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

        return Pred(red_elo, blue_elo, win_prob)

    def attribute_match(self, match: Match, pred: Pred) -> Dict[int, Attribution]:
        out: Dict[int, Attribution] = {}

        pred_diff = pred.red_score - pred.blue_score
        actual_diff = match.red_no_fouls - match.blue_no_fouls
        error = actual_diff - pred_diff

        for t in match.red():
            out[t] = Attribution(self.elo[t] + error / 6)

        for t in match.blue():
            out[t] = Attribution(self.elo[t] - error / 6)

        return out

    def update_team(self, team: int, attr: Attribution, playoff: bool) -> None:
        update = attr.contrib - self.elo[team]
        weight = 1 / 3 if playoff else 1

        self.elo[team] += 72 / 250 * update * weight

    def end_season(self) -> None:
        super().end_season()

        year, mean, sd = self.stats.year, self.stats.score_mean, self.stats.score_sd
        for team in self.elo:
            elo = 1500 + 250 * (self.elo[team] - mean / 3) / sd
            self.end_ratings[year][team] = elo
