import math
from typing import Any, Dict, List

from src.classes import Match, Pred


EPS = 1e-6


class Metrics:
    win_pred: Dict[str, Dict[str, float]]
    score_pred: Dict[str, Dict[str, float]]
    rp_1_pred: Dict[str, Dict[str, float]]
    rp_2_pred: Dict[str, Dict[str, float]]

    @staticmethod
    def conf(y_true: float, y_pred: float) -> float:
        return max(y_pred, 1 - y_pred)

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
            "conf": Metrics.conf(y_true, y_pred),
            "error": Metrics.error(y_true, y_pred),
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
    def add_metadata(metrics: Dict[str, float], match: Match) -> Dict[str, float]:
        metrics["week"] = match.week
        metrics["playoff"] = match.playoff
        return metrics

    @staticmethod
    def agg_binary(metrics: List[Dict[str, float]]) -> Dict[str, float]:
        n = len(metrics)
        if n == 0:
            return {"n": 0, "conf": 0, "error": 0, "acc": 0, "mse": 0, "ll": 0, "f1": 0}

        tp = sum([1 if x["actual"] == 1 and x["pred"] >= 0.5 else 0 for x in metrics])
        fp = sum([1 if x["actual"] == 0 and x["pred"] >= 0.5 else 0 for x in metrics])
        fn = sum([1 if x["actual"] == 1 and x["pred"] < 0.5 else 0 for x in metrics])

        p = tp / max(1, (tp + fp))
        r = tp / max(1, (tp + fn))
        f1 = 2 * p * r / (p + r) if p + r > 0 else 0

        return {
            "n": n,
            "conf": sum([x["conf"] for x in metrics]) / n,
            "error": sum([x["error"] for x in metrics]) / n,
            "acc": sum([x["acc"] for x in metrics]) / n,
            "mse": sum([x["mse"] for x in metrics]) / n,
            "ll": sum([x["ll"] for x in metrics]) / n,
            "f1": f1,
        }

    @staticmethod
    def agg_cont(metrics: List[Dict[str, float]]) -> Dict[str, float]:
        n = len(metrics)
        if n == 0:
            return {"n": 0, "rmse": 0, "mae": 0, "error": 0}

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
        self.rp_1_pred: Dict[str, Dict[str, float]] = {}
        self.rp_2_pred: Dict[str, Dict[str, float]] = {}

    def add_match(self, m: Match, p: Pred):
        win_pred = Metrics.binary(m.winner, max(min(p.win_prob, 1 - EPS), EPS))
        self.win_pred[m.key] = Metrics.add_metadata(win_pred, m)

        red_pred = Metrics.cont(m.red_score, p.red_score)
        self.score_pred[m.key + "_red"] = Metrics.add_metadata(red_pred, m)

        blue_pred = Metrics.cont(m.blue_score, p.blue_score)
        self.score_pred[m.key + "_blue"] = Metrics.add_metadata(blue_pred, m)

        if not m.playoff:
            rp_1_pred = Metrics.binary(m.red_rp_1, max(min(p.red_rp_1, 1 - EPS), EPS))
            self.rp_1_pred[m.key + "_red"] = Metrics.add_metadata(rp_1_pred, m)

            rp_1_pred = Metrics.binary(m.blue_rp_1, max(min(p.blue_rp_1, 1 - EPS), EPS))
            self.rp_1_pred[m.key + "_blue"] = Metrics.add_metadata(rp_1_pred, m)

            rp_2_pred = Metrics.binary(m.red_rp_2, max(min(p.red_rp_2, 1 - EPS), EPS))
            self.rp_2_pred[m.key + "_red"] = Metrics.add_metadata(rp_2_pred, m)

            rp_2_pred = Metrics.binary(m.blue_rp_2, max(min(p.blue_rp_2, 1 - EPS), EPS))
            self.rp_2_pred[m.key + "_blue"] = Metrics.add_metadata(rp_2_pred, m)

    def aggregate(self) -> Dict[str, Dict[str, Dict[str, float]]]:
        wp = self.win_pred.values()
        sp = self.score_pred.values()
        rp1 = self.rp_1_pred.values()
        rp2 = self.rp_2_pred.values()

        def champs_filter(x: Any):
            return x["week"] == 8

        def champs_elims_filter(x: Any):
            return x["week"] == 8 and x["playoff"]

        return {
            "all": {
                "win_pred": Metrics.agg_binary(list(wp)),
                "score_pred": Metrics.agg_cont(list(sp)),
                "rp_1_pred": Metrics.agg_binary(list(rp1)),
                "rp_2_pred": Metrics.agg_binary(list(rp2)),
            },
            "champs": {
                "win_pred": Metrics.agg_binary(list(filter(champs_filter, wp))),
                "score_pred": Metrics.agg_cont(list(filter(champs_filter, sp))),
                "rp_1_pred": Metrics.agg_binary(list(filter(champs_filter, rp1))),
                "rp_2_pred": Metrics.agg_binary(list(filter(champs_filter, rp2))),
            },
            "champs_elims": {
                "win_pred": Metrics.agg_binary(list(filter(champs_elims_filter, wp))),
                "score_pred": Metrics.agg_cont(list(filter(champs_elims_filter, sp))),
                "rp_1_pred": Metrics.agg_binary(list(filter(champs_elims_filter, rp1))),
                "rp_2_pred": Metrics.agg_binary(list(filter(champs_elims_filter, rp2))),
            },
        }
