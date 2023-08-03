from typing import Any, List

import typer
from rich.progress import track

from src.simulation.data import get_data
from src.simulation.main import Simulation
from src.utils import print_table

app = typer.Typer()


@app.command("data")
def items_create():

    output: List[Any] = []
    for year in track(range(2005, 2024), description="Processing..."):
        output.append((str(year), str(len(get_data(year)))))

    print_table(["Year", "Matches"], output)


@app.command("single")
def run_model(year: int, models: List[str]):
    sim = Simulation(year, models)
    sim.run()


if __name__ == "__main__":
    app()
