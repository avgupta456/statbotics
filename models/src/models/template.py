from src.classes import Match, Pred, YearStats


class Model:
    def __init__(self, name: str, stats: YearStats):
        self.name = name
        self.stats = stats

    def process_match(self, match: Match) -> Pred:
        raise NotImplementedError

    def update_match(self, match: Match, pred: Pred) -> None:
        raise NotImplementedError
