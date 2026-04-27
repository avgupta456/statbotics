# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working in the `mcp/` directory.

## Overview

The `statbotics-mcp` package is an MCP (Model Context Protocol) server that exposes the public Statbotics API as MCP tools for LLM clients (Claude Desktop, VS Code, Cursor, etc.). It is a thin wrapper — it always targets the public production API at `https://api.statbotics.io/v3` via the existing [`statbotics`](../api) Python package, and adds no business logic of its own.

## Commands (run from `mcp/`)

```bash
pip install -e .              # Install for development (or: poetry install)
pytest                        # Run tests
python -m statbotics_mcp      # Run the server over stdio (default MCP transport)
python -m statbotics_mcp --http --host 127.0.0.1 --port 8000   # Run over streamable-HTTP
```

## Structure

- **`statbotics_mcp/server.py`** — `FastMCP("statbotics")` instance with one `@mcp.tool()` per public method on the `Statbotics` class. Tool descriptions are pulled from the underlying method docstrings via `Statbotics.<method>.__doc__`.
- **`statbotics_mcp/client.py`** — Lazily-initialized singleton `Statbotics()` instance. Honors the `STATBOTICS_API_URL` env var to override the base URL (useful for local backend testing). `reset_client()` exposed for tests.
- **`statbotics_mcp/cli.py`** — `argparse` entry point. `--http` switches from stdio to streamable-HTTP transport; `--host` / `--port` apply only to HTTP mode.
- **`statbotics_mcp/__main__.py`** — Enables `python -m statbotics_mcp`.
- **`tests/test_server.py`** — Tool-registration assertions (all 14 tools), description sanity checks, schema spot-checks, and behavior tests using a stubbed `Statbotics` instance set via `monkeypatch`.

## Key Behaviors

- **Tool surface mirrors `Statbotics` 1:1** — 14 tools matching `get_team`, `get_teams`, `get_year`, `get_years`, `get_team_year`, `get_team_years`, `get_event`, `get_events`, `get_team_event`, `get_team_events`, `get_match`, `get_matches`, `get_team_match`, `get_team_matches`. Add a new tool here whenever a method is added to the wrapper.
- **Defaults match the wrapper** — including `fields=["all"]` and per-method `limit` defaults (200 for `get_matches`, 100 elsewhere).
- **Errors propagate naturally** — `UserWarning` and `ValueError` raised by the wrapper become MCP tool errors via FastMCP's default exception handling. No custom wrapping.
- **No backend access** — this server only talks to the public REST API; it does not import `backend/`.
- **Python 3.11+** to match the repo's backend CI and FastMCP's runtime requirement.

## Publishing

Update `version` in `pyproject.toml`, then `poetry publish --build` (same flow as `api/`). The console-script entry point is `statbotics-mcp = statbotics_mcp.cli:main`, so end users can run `uvx statbotics-mcp`.
