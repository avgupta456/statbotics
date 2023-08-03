from typing import Dict

from src.classes import Match, Pred, Attribution, YearStats


class Model:
    def __init__(self, name: str, stats: YearStats):
        self.name = name
        self.stats = stats

    def predict_match(self, match: Match) -> Pred:
        raise NotImplementedError

    def attribute_match(self, match: Match, pred: Pred) -> Dict[int, Attribution]:
        raise NotImplementedError

    def update_team(self, team: int, attr: Attribution, playoff: bool) -> None:
        raise NotImplementedError
