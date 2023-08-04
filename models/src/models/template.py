from typing import Dict
from collections import defaultdict

from src.classes import Match, Pred, Attribution, YearStats
from src.metrics import Metrics


class Model:
    stats: YearStats
    metrics: Metrics

    def __init__(self):
        self.end_ratings: Dict[int, Dict[int, float]] = defaultdict(dict)

        self.stats = YearStats(0, 0, 0)
        self.metrics = Metrics()

    def start_season(self, stats: YearStats) -> None:
        self.stats = stats
        self.metrics = Metrics()

    def predict_match(self, match: Match) -> Pred:
        raise NotImplementedError

    def attribute_match(self, match: Match, pred: Pred) -> Dict[int, Attribution]:
        raise NotImplementedError

    def update_team(self, team: int, attr: Attribution, playoff: bool) -> None:
        raise NotImplementedError

    def process_match(self, match: Match) -> Pred:
        pred = self.predict_match(match.mask())
        self.metrics.add_match(match, pred)
        attribution = self.attribute_match(match, pred)
        for team, attr in attribution.items():
            self.update_team(team, attr, match.playoff)
        return pred

    def end_season(self) -> None:
        pass
