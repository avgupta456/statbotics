from collections import defaultdict
from typing import Dict

from src.classes import Attribution, Match, Pred, YearStats
from src.models.template import Model


class Baseline(Model):
    def predict_match(self, match: Match) -> Pred:
        mean = self.stats.score_mean  # rough heuristic
        rp_1_mean = self.stats.rp_1_mean
        rp_2_mean = self.stats.rp_2_mean
        return Pred(mean, mean, 0.5, rp_1_mean, rp_1_mean, rp_2_mean, rp_2_mean)

    def attribute_match(self, match: Match, pred: Pred) -> Dict[int, Attribution]:
        return {}

    def update_team(self, team: int, attrib: Attribution, match: Match) -> None:
        pass


class AvgScore(Model):
    counts: Dict[int, float]
    scores: Dict[int, float]

    def start_season(self, stats: YearStats) -> None:
        super().start_season(stats)

        self.counts: Dict[int, float] = defaultdict(int)
        self.scores: Dict[int, float] = defaultdict(int)
        self.rp_1s: Dict[int, float] = defaultdict(int)
        self.rp_2s: Dict[int, float] = defaultdict(int)

    def predict_match(self, match: Match) -> Pred:
        red_pred = sum(self.scores[t] / max(1, self.counts[t]) for t in match.red())
        blue_pred = sum(self.scores[t] / max(1, self.counts[t]) for t in match.blue())

        win_prob = 1 / (1 + 10 ** ((blue_pred - red_pred) / self.stats.score_sd))

        red_rp_1 = sum(self.rp_1s[t] / max(1, self.counts[t]) for t in match.red())
        blue_rp_1 = sum(self.rp_1s[t] / max(1, self.counts[t]) for t in match.blue())

        red_rp_2 = sum(self.rp_2s[t] / max(1, self.counts[t]) for t in match.red())
        blue_rp_2 = sum(self.rp_2s[t] / max(1, self.counts[t]) for t in match.blue())

        return Pred(
            red_pred, blue_pred, win_prob, red_rp_1, blue_rp_1, red_rp_2, blue_rp_2
        )

    def attribute_match(self, match: Match, pred: Pred) -> Dict[int, Attribution]:
        out: Dict[int, Attribution] = {}
        for t in match.red():
            out[t] = Attribution(
                match.red_score / 3,
                {
                    "rp_1": match.red_rp_1 / 3,
                    "rp_2": match.red_rp_2 / 3,
                },
            )

        for t in match.blue():
            out[t] = Attribution(
                match.blue_score / 3,
                {
                    "rp_1": match.blue_rp_1 / 3,
                    "rp_2": match.blue_rp_2 / 3,
                },
            )

        return out

    def update_team(self, team: int, attrib: Attribution, match: Match) -> None:
        self.counts[team] += 1
        self.scores[team] += attrib.contrib
        self.rp_1s[team] += attrib.breakdown["rp_1"]
        self.rp_2s[team] += attrib.breakdown["rp_2"]
