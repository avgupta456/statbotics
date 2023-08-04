from typing import Dict, List, Type

from src.models.baseline import AvgScore, Baseline
from src.models.elo import Elo
from src.models.epa import EPA
from src.models.template import Model
from src.utils import load_cache, print_table

model_name_to_class: Dict[str, Type[Model]] = {
    "avg_score": AvgScore,
    "baseline": Baseline,
    "elo": Elo,
    "epa": EPA,
}


def to_fixed(num: float, digits: int) -> str:
    return f"{num:.{digits}f}"


def run_sim(
    start_year: int, end_year: int, model_names: List[str], verbose: bool = False
):
    models: Dict[str, Model] = {m: model_name_to_class[m]() for m in model_names}

    table: List[List[str]] = []

    for year in range(start_year, end_year + 1):
        if year not in range(2005, 2024) or year == 2021:
            continue

        if verbose:
            table: List[List[str]] = []
        else:
            table.append([str(year)])

        matches, stats = load_cache(f"cache/processed/{year}")
        matches = sorted(matches, key=lambda m: m.time)

        for model_name, model in models.items():
            model.start_season(stats)
            for match in matches:
                model.process_match(match)
            model.end_season()

            metrics = model.metrics.aggregate()

            if verbose:
                table.append(
                    [
                        str(year),
                        model_name,
                        to_fixed(metrics["win_pred"]["acc"], 4),
                        to_fixed(metrics["win_pred"]["mse"], 4),
                        to_fixed(metrics["win_pred"]["ll"], 4),
                        to_fixed(metrics["score_pred"]["rmse"], 2),
                        to_fixed(metrics["score_pred"]["mae"], 2),
                        to_fixed(metrics["score_pred"]["error"], 2),
                    ]
                )
            else:
                table[-1].append(to_fixed(metrics["win_pred"]["acc"], 4))

        if verbose:
            headers = [
                "Year",
                "Model",
                "Accuracy",
                "Brier Score",
                "Log Loss",
                "Score RMSE",
                "Score MAE",
                "Score Error",
            ]
            print_table(headers, table)

    if not verbose:
        print_table(["Year", *model_names], table)
