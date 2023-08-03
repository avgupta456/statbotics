import copy
import math
from typing import Any, Dict, List
from collections import defaultdict

from src.utils import print_table


class Match:
    key: str
    event: str
    week: int
    playoff: bool
    time: int
    red_1: int
    red_2: int
    red_3: int
    blue_1: int
    blue_2: int
    blue_3: int
    red_score: int
    blue_score: int
    winner: float

    def __init__(
        self,
        key: str,
        event: str,
        week: int,
        playoff: bool,
        time: int,
        red_1: int,
        red_2: int,
        red_3: int,
        blue_1: int,
        blue_2: int,
        blue_3: int,
        red_score: int,
        blue_score: int,
    ):
        self.key = key
        self.event = event
        self.week = week
        self.playoff = playoff
        self.time = time
        self.red_1 = red_1
        self.red_2 = red_2
        self.red_3 = red_3
        self.blue_1 = blue_1
        self.blue_2 = blue_2
        self.blue_3 = blue_3
        self.red_score = red_score
        self.blue_score = blue_score

        self.winner = (
            1 if red_score > blue_score else 0.5 if red_score == blue_score else 0
        )

    def red(self):
        return (self.red_1, self.red_2, self.red_3)

    def blue(self):
        return (self.blue_1, self.blue_2, self.blue_3)

    def mask(self) -> "Match":
        match_copy = copy.deepcopy(self)
        match_copy.red_score = 0
        match_copy.blue_score = 0
        return match_copy

    def __repr__(self):
        return f"Match({self.key}, {self.red_1} {self.red_2} {self.red_3} vs. {self.blue_1} {self.blue_2} {self.blue_3}, {self.red_score}-{self.blue_score})"


class Pred:
    red_score: float
    blue_score: float
    win_prob: float

    def __init__(self, red_score: float, blue_score: float, win_prob: float):
        self.red_score = red_score
        self.blue_score = blue_score
        self.win_prob = win_prob

    def __repr__(self):
        return f"Pred({self.red_score}-{self.blue_score}, {self.win_prob})"


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

    def add_match_method(self, name: str, m: Match, p: Pred):
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

        print_table(["Method", "Acc", "MSE", "LL"], win_pred_stats)

        score_pred_stats: List[List[Any]] = []
        for name, preds in self.score_pred.items():
            n = len(preds)
            rmse = math.sqrt(sum([x["mse"] for x in preds.values()]) / n)
            mae = sum([x["mae"] for x in preds.values()]) / n
            error = sum([x["error"] for x in preds.values()]) / n
            score_pred_stats.append(
                [name, str(round(rmse, 2)), str(round(mae, 2)), str(round(error, 2))]
            )

        print_table(["Method", "RMSE", "MAE", "Error"], score_pred_stats)


class Method:
    def __init__(self, name: str, metrics: Metrics):
        self.name = name
        self.metrics = metrics

    def process_match(self, match: Match) -> Pred:
        raise NotImplementedError

    def update_match(self, match: Match, pred: Pred) -> None:
        raise NotImplementedError
