from collections import defaultdict
from typing import Dict

from src.classes import Match, Pred, Attribution, YearStats
from src.models.template import Model


class Baseline(Model):
    def predict_match(self, match: Match) -> Pred:
        mean = self.stats.score_mean  # rough heuristic
        return Pred(mean, mean, 0.5)

    def attribute_match(self, match: Match, pred: Pred) -> Dict[int, Attribution]:
        return {}

    def update_team(self, team: int, attr: Attribution, playoff: bool) -> None:
        pass


class AvgScore(Model):
    counts: Dict[int, float]
    scores: Dict[int, float]

    def start_season(self, stats: YearStats) -> None:
        super().start_season(stats)

        self.counts: Dict[int, float] = defaultdict(int)
        self.scores: Dict[int, float] = defaultdict(int)

    def predict_match(self, match: Match) -> Pred:
        red_pred = sum(self.scores[t] / max(1, self.counts[t]) for t in match.red())
        blue_pred = sum(self.scores[t] / max(1, self.counts[t]) for t in match.blue())

        win_prob = 1 / (1 + 10 ** ((blue_pred - red_pred) / self.stats.score_sd))

        return Pred(red_pred, blue_pred, win_prob)

    def attribute_match(self, match: Match, pred: Pred) -> Dict[int, Attribution]:
        out: Dict[int, Attribution] = {}
        for t in match.red():
            out[t] = Attribution(match.red_score / 3)

        for t in match.blue():
            out[t] = Attribution(match.blue_score / 3)

        return out

    def update_team(self, team: int, attr: Attribution, playoff: bool) -> None:
        self.counts[team] += 1
        self.scores[team] += attr.contrib
