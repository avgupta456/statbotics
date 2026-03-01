# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Statbotics is an open-source data analytics platform for the FIRST Robotics Competition (FRC). It computes and serves **EPA (Expected Points Added)** ratings — a team performance metric in point units built on top of Elo — for all FRC teams, years, events, and matches from 2002 to present.

## Repository Structure

| Directory | Description | Details |
|-----------|-------------|---------|
| `backend/` | FastAPI server: fetches data from TBA, computes EPA, serves REST + site APIs | See `backend/CLAUDE.md` |
| `frontend/` | Next.js 13 frontend — the active, deployed website | See `frontend/CLAUDE.md` |
| `new/frontend/` | **Paused** Next.js 14 rewrite — do not read or modify unless explicitly asked | — |
| `api/` | `statbotics` Python package published to PyPI | See `api/CLAUDE.md` |
| `scripts/` | Jupyter notebooks for EPA model analysis and API demos | See `scripts/CLAUDE.md` |

## Season Prep Checklist

When preparing for a new FRC season (year N), update these in order:

1. `backend/src/constants.py` — update `CURR_YEAR` and `CURR_WEEK`
2. `backend/src/tba/breakdown.py` — add `all_keys[N]` and a `clean_breakdown_{N}()` function with game-specific score parsing
3. `frontend/src/constants.tsx` — update `CURR_YEAR`, `CURR_WEEK`, add year to `RP_KEYS`/`RP_NAMES`
