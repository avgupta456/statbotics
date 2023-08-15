# Statbotics Models

This directory contains a standalone project that loads data from The Blue Alliance (TBA) and implements the EPA model and other baselines. This repository is intended to isolate the EPA model from the broader Statbotics website. Some simplifications have been made and this code is not used in production.

## Usage

Create a Python virtual environment and install the dependencies in the `requirements.txt`. The main dependencies are `typer` (for the command line interface), `requests` (to fetch data from TBA), `numpy` (math operations) and `scipy` (statistical distributions).

To load data from TBA, run `python main.py data`. The first execution will take several minutes, but responses are cached locally so all subsequent executions will be faster.

To start a simulation, run `python main.py sim {start_year} {end_year} {method_1} {method_2} ...` (for example, `python main.py sim 2023 2023 epa_v2`). The following models are implemented:

- `baseline`: Predicts the week 1 mean score for every alliance the entire season (with a 50% win probability).
- `avg_score`: Estimates the alliance score as the average of each team's average score throughout the season.
- `elo`: Uses the Elo model to assign a rating to each team. Tries to closely follow Caleb Sykes' implementation. Used on the Statbotics website in 2022.
- `epa`: The Expected Points Added (EPA) method, used on the Statbotics website in 2023.
- `epa_v2`: The second iteration of the EPA model. Used on the Statbotics website 2024 onwards.

## Limitations

- OPR ratings are excluded. Unlike the other models, OPR cannot be iteratively calculated and is much more computationally expensive to run every match. OPR is also extremely noisy at the beginning of an event. Instead of Statbotics, refer to The Blue Alliance for OPR ratings.
- 2002-2004 is excluded since there were fewer teams per alliance. Playoff matches with red cards are excluded since the outlier scores can cause issues (handled better in production).
- End of year mean reversion is simplified for the EPA and EPA2 models due to complexity.
