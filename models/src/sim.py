from typing import Any, Dict, List

from src.utils import load_cache
from src.baseline import Baseline, AvgScore, MovingAvgScore
from src.classes import Metrics, Method


class Simulation:
    @staticmethod
    def get_data(year: int):
        return load_cache(f"cache/processed/{year}")

    def __init__(self, year: int, methods: List[str]):
        self.year = year

        self.metrics = Metrics()

        method_dict: Dict[str, Any] = {
            "baseline": Baseline,
            "avg_score": AvgScore,
            "moving_avg_score": MovingAvgScore,
        }

        self.methods: List[Method] = [
            method_dict[name](name, self.metrics) for name in methods
        ]

    def run(self):
        self.matches = Simulation.get_data(self.year)
        matches = sorted(self.matches, key=lambda m: m.time)
        for match in matches:
            for method in self.methods:
                pred = method.process_match(match.mask())
                self.metrics.add_match_method(method.name, match, pred)
                method.update_match(match, pred)

        self.metrics.print()
