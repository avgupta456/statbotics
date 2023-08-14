from typing import Dict, List, Tuple, Type

from src.classes import Match, YearStats
from src.metrics import Metrics
from src.models.baseline import AvgScore, Baseline
from src.models.elo import Elo
from src.models.epa import EPA
from src.models.epa_v2 import EPAV2
from src.models.template import Model
from src.utils import load_cache, print_table

model_name_to_class: Dict[str, Type[Model]] = {
    "avg_score": AvgScore,
    "baseline": Baseline,
    "elo": Elo,
    "epa": EPA,
    "epa_v2": EPAV2,
}


def get_matches(year: int) -> Tuple[List[Match], YearStats]:
    matches, stats = load_cache(f"cache/processed/{year}")
    matches = sorted(matches, key=lambda m: m.time)
    return matches, stats


def to_fixed(num: float, digits: int) -> str:
    return f"{num:.{digits}f}"


def get_table_headers() -> List[str]:
    return [
        "Year",
        "Model",
        "Matches",
        "",
        "Conf",
        "Acc",
        "MSE",
        "LL",
        "",
        "Score RMSE",
        "Score MAE",
        "Score Error",
        "",
        "RP1 Err",
        "RP1 MSE",
        "RP1 LL",
        "RP1 F1",
        "",
        "RP2 Err",
        "RP2 MSE",
        "RP2 LL",
        "RP2 F1",
    ]


def get_table_rows(metrics: Metrics, year: int, model_name: str) -> List[List[str]]:
    out: List[List[str]] = []

    data = metrics.aggregate()
    for filter, filter_name in [
        ("all", ""),
        ("champs", " (C)"),
        ("champs_elims", " (CE)"),
    ]:
        out.append(
            [
                str(year) + filter_name,
                model_name,
                str(data[filter]["win_pred"]["n"]),
                "",
                to_fixed(data[filter]["win_pred"]["conf"], 4),
                to_fixed(data[filter]["win_pred"]["acc"], 4),
                to_fixed(data[filter]["win_pred"]["mse"], 4),
                to_fixed(data[filter]["win_pred"]["ll"], 4),
                "",
                to_fixed(data[filter]["score_pred"]["rmse"], 2),
                to_fixed(data[filter]["score_pred"]["mae"], 2),
                to_fixed(data[filter]["score_pred"]["error"], 2),
                "",
                to_fixed(data[filter]["rp_1_pred"]["error"], 4),
                to_fixed(data[filter]["rp_1_pred"]["mse"], 4),
                to_fixed(data[filter]["rp_1_pred"]["ll"], 4),
                to_fixed(data[filter]["rp_1_pred"]["f1"], 4),
                "",
                to_fixed(data[filter]["rp_2_pred"]["error"], 4),
                to_fixed(data[filter]["rp_2_pred"]["mse"], 4),
                to_fixed(data[filter]["rp_2_pred"]["ll"], 4),
                to_fixed(data[filter]["rp_2_pred"]["f1"], 4),
            ]
        )

    return out


def run_sim(start_year: int, end_year: int, model_names: List[str]):
    models: Dict[str, Model] = {m: model_name_to_class[m]() for m in model_names}

    for year in range(start_year, end_year + 1):
        if year not in range(2005, 2024) or year == 2021:
            continue

        table: List[List[str]] = []

        matches, stats = get_matches(year)
        for model_name, model in models.items():
            model.start_season(stats)
            for match in matches:
                model.process_match(match)
            model.end_season()

            table.extend(get_table_rows(model.metrics, year, model_name))

        headers = get_table_headers()
        table += [[str(year)], [f"{year} (C)"], [f"{year} (CE)"]]
        table = sorted(table, key=lambda row: row[0])
        print_table(headers, table)
