import math
from collections import defaultdict
from typing import Any, Dict, List

from src.classes import Match, Pred
from src.models.baseline import AvgScore, Baseline
from src.models.template import Model
from src.models.elo import Elo
from src.models.epa import EPA
from src.utils import load_cache, print_table


class Metrics:
    win_pred: Dict[str, Dict[str, Dict[str, float]]]
    score_pred: Dict[str, Dict[str, Dict[str, float]]]

    @staticmethod
    def acc(y_true: float, y_pred: float) -> float:
        return 1 if round(y_pred) == y_true else 0

    @staticmethod
    def mse(y_true: float, y_pred: float) -> float:
        return (y_pred - y_true) ** 2

    @staticmethod
    def ll(y_true: float, y_pred: float) -> float:
        return math.log(y_pred) if y_true == 1 else math.log(1 - y_pred)

    @staticmethod
    def mae(y_true: float, y_pred: float) -> float:
        return abs(y_pred - y_true)

    @staticmethod
    def error(y_true: float, y_pred: float) -> float:
        return y_pred - y_true

    @staticmethod
    def binary(y_true: float, y_pred: float) -> Dict[str, float]:
        return {
            "pred": y_pred,
            "actual": y_true,
            "acc": Metrics.acc(y_true, y_pred),
            "mse": Metrics.mse(y_true, y_pred),
            "ll": Metrics.ll(y_true, y_pred),
        }

    @staticmethod
    def cont(y_true: float, y_pred: float) -> Dict[str, float]:
        return {
            "pred": y_pred,
            "actual": y_true,
            "mse": Metrics.mse(y_true, y_pred),
            "mae": Metrics.mae(y_true, y_pred),
            "error": Metrics.error(y_true, y_pred),
        }

    def __init__(self):
        self.win_pred: Dict[str, Dict[str, Dict[str, float]]] = defaultdict(dict)
        self.score_pred: Dict[str, Dict[str, Dict[str, float]]] = defaultdict(dict)

    def add_match_model(self, name: str, m: Match, p: Pred):
        self.win_pred[name][m.key] = Metrics.binary(m.winner, p.win_prob)
        self.score_pred[name][m.key + "_red"] = Metrics.cont(m.red_score, p.red_score)
        self.score_pred[name][m.key + "_blue"] = Metrics.cont(
            m.blue_score, p.blue_score
        )

    def print(self):
        win_pred_stats: List[List[Any]] = []
        for name, preds in self.win_pred.items():
            n = len(preds)
            acc = sum([x["acc"] for x in preds.values()]) / n
            mse = sum([x["mse"] for x in preds.values()]) / n
            ll = sum([x["ll"] for x in preds.values()]) / n
            win_pred_stats.append(
                [name, str(round(acc, 4)), str(round(mse, 4)), str(round(ll, 4))]
            )

        print_table(["Model", "Acc", "MSE", "LL"], win_pred_stats)

        score_pred_stats: List[List[Any]] = []
        for name, preds in self.score_pred.items():
            n = len(preds)
            rmse = math.sqrt(sum([x["mse"] for x in preds.values()]) / n)
            mae = sum([x["mae"] for x in preds.values()]) / n
            error = sum([x["error"] for x in preds.values()]) / n
            score_pred_stats.append(
                [name, str(round(rmse, 2)), str(round(mae, 2)), str(round(error, 2))]
            )

        print_table(["Model", "RMSE", "MAE", "Error"], score_pred_stats)


class Simulation:
    @staticmethod
    def get_data(year: int):
        return load_cache(f"cache/processed/{year}")

    def __init__(self, year: int, models: List[str]):
        self.year = year

        self.metrics = Metrics()

        self.matches, self.stats = Simulation.get_data(self.year)

        models_dict: Dict[str, Any] = {
            "baseline": Baseline("baseline", self.stats),
            "avg_score": AvgScore("avg_score", self.stats),
            "elo": Elo("elo", self.stats),
            "epa": EPA("epa", self.stats),
        }

        self.models: List[Model] = [models_dict[name] for name in models]

    def run(self):
        matches = sorted(self.matches, key=lambda m: m.time)
        for match in matches:
            for model in self.models:
                pred = model.predict_match(match.mask())
                self.metrics.add_match_model(model.name, match, pred)
                attributions = model.attribute_match(match, pred)
                for team, attr in attributions.items():
                    model.update_team(team, attr, match.playoff)

        self.metrics.print()
