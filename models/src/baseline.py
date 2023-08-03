from typing import Any, Dict
from collections import defaultdict

from src.classes import Method, Pred, Match


class Baseline(Method):
    def process_match(self, match: Match) -> Pred:
        return Pred(100, 100, 0.5)

    def update_match(self, match: Match, pred: Pred):
        pass


class AvgScore(Method):
    counts: Dict[int, float]
    scores: Dict[int, float]

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)

        self.counts: Dict[int, float] = defaultdict(int)
        self.scores: Dict[int, float] = defaultdict(int)

    def process_match(self, match: Match) -> Pred:

        red_pred = sum(self.scores[t] for t in match.red())
        red_pred /= max(1, sum(self.counts[t] for t in match.red()))

        blue_pred = sum(self.scores[t] for t in match.blue())
        blue_pred /= max(1, sum(self.counts[t] for t in match.blue()))

        win_prob = 1 / (1 + 10 ** ((blue_pred - red_pred) / 15))

        return Pred(red_pred, blue_pred, win_prob)

    def update_match(self, match: Match, pred: Pred):
        for t in match.red():
            self.counts[t] += 1
            self.scores[t] += match.red_score

        for t in match.blue():
            self.counts[t] += 1
            self.scores[t] += match.blue_score


class MovingAvgScore(AvgScore):
    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.decay = 0.9

    def update_match(self, match: Match, pred: Pred):
        for t in match.red():
            self.counts[t] = self.counts[t] * self.decay + 1
            self.scores[t] = self.scores[t] * self.decay + match.red_score

        for t in match.blue():
            self.counts[t] = self.counts[t] * self.decay + 1
            self.scores[t] = self.scores[t] * self.decay + match.blue_score
