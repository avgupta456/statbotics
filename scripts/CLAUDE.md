# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working in the `scripts/` directory.

## Overview

Jupyter notebooks for analyzing the EPA model and demonstrating the Python API. Not part of the deployed product.

## Commands (run from `scripts/`)

```bash
poetry install     # Install dependencies
jupyter notebook   # Start notebook server at localhost:8888
```

## Contents

- **`api/Examples.ipynb`** — Demonstrates the `statbotics` Python package with example queries.
- **`baselines/Baseline Metrics.ipynb`** — Reproduces EPA model accuracy metrics and compares against Elo/OPR baselines.
- **`2023/`** — Year-specific analysis notebooks.
