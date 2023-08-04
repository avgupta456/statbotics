import math
from typing import Dict, List

from src.classes import Match, Pred


class Metrics:
    win_pred: Dict[str, Dict[str, float]]
    score_pred: Dict[str, Dict[str, float]]

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

    @staticmethod
    def agg_binary(metrics: List[Dict[str, float]]) -> Dict[str, float]:
        n = len(metrics)
        return {
            "n": n,
            "acc": sum([x["acc"] for x in metrics]) / n,
            "mse": sum([x["mse"] for x in metrics]) / n,
            "ll": sum([x["ll"] for x in metrics]) / n,
        }

    @staticmethod
    def agg_cont(metrics: List[Dict[str, float]]) -> Dict[str, float]:
        n = len(metrics)
        return {
            "n": n,
            "rmse": math.sqrt(sum([x["mse"] for x in metrics]) / n),
            "mae": sum([x["mae"] for x in metrics]) / n,
            "error": sum([x["error"] for x in metrics]) / n,
        }

    def __init__(self):
        # match key as index for easy lookup/merging
        self.win_pred: Dict[str, Dict[str, float]] = {}
        self.score_pred: Dict[str, Dict[str, float]] = {}

    def add_match(self, m: Match, p: Pred):
        self.win_pred[m.key] = Metrics.binary(m.winner, p.win_prob)
        self.score_pred[m.key + "_red"] = Metrics.cont(m.red_score, p.red_score)
        self.score_pred[m.key + "_blue"] = Metrics.cont(m.blue_score, p.blue_score)

    def aggregate(self):
        return {
            "win_pred": Metrics.agg_binary(list(self.win_pred.values())),
            "score_pred": Metrics.agg_cont(list(self.score_pred.values())),
        }
