# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working in the `backend/` directory.

## Commands (run from `backend/`)

```bash
poetry install                          # Install dependencies
uvicorn main:app --reload --port 8000  # Dev API/site server
uvicorn main:app --reload --port 8001  # Data server (emulated separately in dev)
black src/                              # Format
isort src/                              # Sort imports
flake8 src/                             # Lint
pyright                                 # Type check (config at repo root pyrightconfig.json)
```

## Router Structure

Three FastAPI routers are mounted at `/v3` in `main.py`:

| Router | Mount | Purpose |
|--------|-------|---------|
| `src/api/` | `/v3` | **Public REST API** — consumed by external users and the Python package. One file per entity: `team`, `year`, `team_year`, `event`, `team_event`, `match`, `team_match`. |
| `src/data/` | `/v3/data` | **ETL triggers** — internal endpoints that run the data pipeline. `update_curr_year` does a partial (incremental) refresh; `reset_curr_year` does a full refresh; `reset_all_years` rebuilds from 2002. |
| `src/site/` | `/v3/site` | **Frontend-optimized API** — returns pre-shaped data for the website. Also writes results to GCS so the frontend can read from the bucket instead of hitting the DB directly. |

In dev, the data router calls back to `http://localhost:8001` (a second uvicorn process). In prod, each router is deployed as a separate Cloud Run service (`deploy/`).

## Data Pipeline (`src/data/`)

For each year, `process_year()` in `src/data/main.py` runs these steps in order:

1. **`process_year_tba()`** (`src/data/tba.py`) — Fetches teams, events, and matches from The Blue Alliance API (with etag-based caching and a local `cache/` directory). Writes raw objects to DB.
2. **`process_year_avg()`** (`src/data/avg.py`) — Computes average scores for the year object.
3. **`process_year_wins()`** (`src/data/wins.py`) — Computes win/loss/tie records.
4. **`process_year_epa()`** (`src/data/epa/`) — Runs the EPA model:
   - `calc.py` — Calls `src/models/epa/` to compute per-team EPA ratings match by match.
   - `agg.py` — Aggregates match-level EPA up to event and year level.
   - `metrics.py` — Computes normalized EPA and derived statistics.

After writing to DB, if `year == CURR_YEAR`, results are also compressed (zlib) and uploaded to GCS via `src/google/storage.py`.

**Two entry points** in `src/data/main.py`:
- `update_curr_year(partial=True)` — incremental update using existing DB objects.
- `update_curr_year(partial=False)` / `reset_all_years()` — full recompute from scratch.

## EPA Model (`src/models/epa/`)

The `EPA` class (in `main.py`) extends the `Model` base class (`src/models/template.py`). The base class handles the match processing loop; subclasses implement:
- `start_season()` — initialize per-team ratings from prior years
- `predict_match()` — produce score predictions for both alliances
- `attribute_match()` — compute per-team error attribution after a match
- `update_team()` — update the team's rating distribution

Each team's rating is a `SkewNormal` distribution (`src/models/epa/math.py`).

**EPA dimensions** (for 2016+): `[total, auto, teleop, endgame, rp_1, rp_2, rp_3, tiebreaker, comp_1..comp_18]` — indices 0-25. Pre-2016 only uses `total`.

**Key constants** (`src/models/epa/constants.py`):
- `NORM_MEAN = 1500`, `NORM_SD = 250` — normalized EPA scale
- `ELIM_WEIGHT = 1/3` — elimination matches count less toward rating updates
- `MEAN_REVERSION = 0.4` — cross-season regression to mean

## Game Breakdown (`src/tba/breakdown.py`)

This is the largest file to update each season. It contains:
- `all_keys` — year-keyed dict mapping a year to its list of EPA component names
- `clean_breakdown_{year}()` — parses the raw TBA score breakdown for that year into the standard component format

When adding a new season, add a new entry to `all_keys` and a new `clean_breakdown_{year}` function.

## Database (`src/db/`)

CockroachDB via SQLAlchemy 2.0. Seven tables defined in `src/db/models/`:
`Team`, `Year`, `TeamYear`, `Event`, `TeamEvent`, `Match`, `TeamMatch`.

- Local dev: `cockroachdb://root@localhost:26257/statbotics3?sslmode=disable`
- Production: credentials via `CRDB_USER`, `CRDB_PWD`, `CRDB_HOST` env vars

`src/db/read/` and `src/db/write/` are split by entity.

## TBA API (`src/tba/`)

- `main.py` — `get_tba()` wraps TBA HTTP calls with etag support and a local pickle cache (`cache/` dir).
- `read_tba.py` — higher-level functions that call `get_tba()` and return typed objects.
- `breakdown.py` — game-specific score breakdown parsing (see above).
- Auth key is in `src/tba/constants.py` via env var `TBA_KEY`.

## Season Config

Update these at the start of each new season:
- `src/constants.py`: `CURR_YEAR`, `CURR_WEEK`
- `src/tba/breakdown.py`: add `all_keys[YEAR]` and `clean_breakdown_{year}()`

## GCS / Deployment

- Production uses three separate Cloud Run services (api, data, site) defined in `deploy/`.
- GCS buckets: `site_v1` (prod), `site_dev_v1` (dev). The frontend reads from these buckets first, falling back to the site API.
- Set env var `PROD=True` to enable production DB connection and GCS writes.
