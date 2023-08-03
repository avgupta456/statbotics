from typing import Any, Dict
from collections import defaultdict

from src.models.template import Model
from src.classes import Match, Pred, Attribution


class EPA(Model):
    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)

        self.counts: Dict[int, int] = defaultdict(int)
        self.epa: Dict[int, float] = defaultdict(lambda: self.stats.score_mean / 3)

    @staticmethod
    def percent_func(x: int) -> float:
        return min(0.5, max(0, 3, 0.5 - 0.2 / 6 * (x - 6)))

    @staticmethod
    def margin_func(year: int, x: int) -> float:
        if year == 2015:
            return 0

        if year == 2018:
            return 1

        return min(1, max(0, 1 / 24 * (x - 12)))

    def predict_match(self, match: Match) -> Pred:
        red_epa = sum(self.epa[t] for t in match.red())
        blue_epa = sum(self.epa[t] for t in match.blue())

        k = 5 / 8 * self.stats.score_sd
        win_prob = 1 / (1 + 10 ** ((blue_epa - red_epa) / k))

        return Pred(red_epa, blue_epa, win_prob)

    def attribute_match(self, match: Match, pred: Pred) -> Dict[int, Attribution]:
        out: Dict[int, Attribution] = {}

        red_error = match.red_score - pred.red_score
        blue_error = match.blue_score - pred.blue_score

        for t in match.red():
            margin = self.margin_func(self.stats.year, self.counts[t])
            error = (red_error - margin * blue_error) / (1 + margin)
            out[t] = Attribution(self.epa[t] + error / 3)

        for t in match.blue():
            margin = self.margin_func(self.stats.year, self.counts[t])
            error = (blue_error - margin * red_error) / (1 + margin)
            out[t] = Attribution(self.epa[t] + error / 3)

        return out

    def update_team(self, team: int, attr: Attribution, playoff: bool) -> None:
        update = attr.contrib - self.epa[team]

        percent = self.percent_func(self.counts[team])
        weight = 1 / 3 if playoff else 1

        self.epa[team] += percent * weight * update
        self.counts[team] += 1
