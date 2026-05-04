# Statbotics Models

Standalone match prediction models and evaluation framework for FRC.

## Setup

```bash
cd models
poetry install
```

## Export data from the DB

```bash
psql "postgresql://root@localhost:26257/statbotics3?sslmode=disable" -c "\copy (SELECT year,event,comp_level,elim,time,red_1,red_2,red_3,blue_1,blue_2,blue_3,red_score,red_no_foul,blue_score,blue_no_foul,winner FROM matches WHERE winner IS NOT NULL AND red_score IS NOT NULL AND blue_score IS NOT NULL ORDER BY year,time) TO 'matches.csv' WITH CSV HEADER"
```

```bash
psql "postgresql://root@localhost:26257/statbotics3?sslmode=disable" -c "\copy (SELECT year,score_mean,score_sd,no_foul_mean FROM years ORDER BY year) TO 'years.csv' WITH CSV HEADER"
```

## Run evaluation

```bash
poetry run python runner.py --model epa --matches-csv matches.csv --years-csv years.csv
poetry run python runner.py --model wins --matches-csv matches.csv --years-csv years.csv
```

Or directly against the DB (no CSV export needed):

```bash
poetry run python runner.py --model epa
```

## Models

### `EPAModel` (`epa_model.py`)

Simplified EPA using total match score. Reproduces the core statbotics EPA logic:

- **Cross-year initialization** — normalized EPA carries across seasons with 0.4 mean reversion toward a slightly-below-average baseline (1450 on a 1500±250 scale).
- **EWMA update** — `epa += weight * percent * (error / num_teams)`, where `percent` starts at ~33% and decays to ~20% after 12+ qual matches.
- **Win probability** — `1 / (1 + 10^(k * norm_diff))` with `k = -5/8` (2008+) or `-5/12` (pre-2008).
- Elimination matches count at 1/3 weight and do not increment the match count.

### `WinsModel` (`wins_model.py`)

Win-rate baseline. Each team accumulates a win rate with a 1W/1L Laplace prior (starts at 0.5). Predicts via:

```
P(red wins) = avg_red_rate / (avg_red_rate + avg_blue_rate)
```

## Adding a new model

Subclass `Model` from `base.py` and implement three methods:

```python
from base import Model

class MyModel(Model):
    def start_year(self, year, score_mean, score_sd, **kwargs): ...
    def predict(self, red1, red2, red3, blue1, blue2, blue3) -> float: ...
    def update(self, red1, red2, red3, blue1, blue2, blue3,
               winner, red_score, blue_score, elim=False): ...
```

Then evaluate it:

```python
from runner import load_from_csv, evaluate, report

matches, years = load_from_csv("matches.csv", "years.csv")
preds = evaluate(MyModel(), matches, years)
report(preds)
```

## Output format

```
  year       n    acc   brier    champs_n  champs_acc  champs_brier
------------------------------------------------------------------------
  2002     ...  0.xxx  0.xxxx         ...       0.xxx        0.xxxx
  ...
------------------------------------------------------------------------
   ALL     ...  0.xxx  0.xxxx         ...       0.xxx        0.xxxx
```

- **acc** — fraction of matches where the predicted winner (prob > 0.5) was correct (ties excluded)
- **brier** — mean squared error on win probability (lower is better; 0.25 = random)
- **champs** — same metrics filtered to championship events only
