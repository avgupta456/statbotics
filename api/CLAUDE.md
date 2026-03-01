# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working in the `api/` directory.

## Overview

The `statbotics` Python package (published to PyPI at version 3.0.0) provides a simple interface to the public Statbotics REST API. It is a thin wrapper — no EPA computation happens here.

## Commands (run from `api/`)

```bash
poetry install         # Install dependencies
python -m pytest       # Run tests
python -m pytest tests/test_teams.py  # Run a single test file
```

## Structure

- **`statbotics/main.py`** — The `Statbotics` class. All public methods are here:
  - `get_team()`, `get_teams()` — team-level data
  - `get_year()`, `get_years()` — year-level averages
  - `get_team_year()`, `get_team_years()` — per-team per-year EPA stats
  - `get_event()`, `get_events()` — event data
  - `get_team_event()`, `get_team_events()` — per-team per-event stats
  - `get_match()`, `get_matches()` — match data
  - `get_team_match()`, `get_team_matches()` — per-team per-match stats

  All plural methods accept filter params (team, year, event, week, etc.) and support `metric`, `ascending`, `limit`, `offset`, and `fields` arguments.

- **`statbotics/validate.py`** — Input validation helpers (`check_type`, `get_locations`).
- **`statbotics/constants.py`** — Country/state name normalization maps used by location filtering.
- **`tests/`** — Test files per entity (`test_teams.py`, etc.) using `test_framework.py` helpers.

## Key Behaviors

- Uses `CacheControl` (wrapping `requests.Session`) for HTTP-level response caching.
- Always hits `https://api.statbotics.io/v3` (hardcoded production URL).
- Plural queries require at least one scoping parameter (year, event, week, or match) for `get_team_matches()`; enforced in the method.
- `fields=["all"]` returns everything; pass a list of field names to filter the response.

## Publishing

The package is built with Poetry. To publish a new version, update `version` in `pyproject.toml`, then run `poetry publish --build`.
