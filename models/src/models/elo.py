from typing import Any, Dict
from collections import defaultdict

from src.models.template import Model
from src.classes import Match, Pred, Attribution


class Elo(Model):
    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)

        self.elo: Dict[int, float] = defaultdict(lambda: self.stats.score_mean / 3)

    def predict_match(self, match: Match) -> Pred:
        red_elo = sum(self.elo[t] for t in match.red())
        blue_elo = sum(self.elo[t] for t in match.blue())

        k = 5 / 8 * self.stats.score_sd
        win_prob = 1 / (1 + 10 ** ((blue_elo - red_elo) / k))

        return Pred(red_elo, blue_elo, win_prob)

    def attribute_match(self, match: Match, pred: Pred) -> Dict[int, Attribution]:
        out: Dict[int, Attribution] = {}

        pred_diff = pred.red_score - pred.blue_score
        actual_diff = match.red_score - match.blue_score
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
