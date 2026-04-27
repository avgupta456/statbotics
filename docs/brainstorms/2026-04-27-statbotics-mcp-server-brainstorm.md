---
date: 2026-04-27
topic: statbotics-mcp-server
---

# Statbotics MCP Server

## What We're Building

An MCP (Model Context Protocol) server, shipped in this repo under a new top-level `mcp/` directory, that exposes the public Statbotics REST API (`https://api.statbotics.io/v3`) as MCP tools. The server is a thin wrapper that delegates HTTP work to the existing `statbotics` Python package (in `api/`), so all URL handling, caching, validation, and field filtering stay in one place.

The server is intended to be runnable directly from a fresh clone for repo users, and also publishable to PyPI as `statbotics-mcp` so end users can launch it with `uvx statbotics-mcp` from any MCP client.

## Why This Approach

- **Reuse over duplication.** The `statbotics` package already wraps the public API with caching, validation, and the canonical method surface — building on top avoids drift.
- **Public API only.** The MCP server never talks to the backend directly; it only hits `api.statbotics.io`, matching how external users consume Statbotics today.
- **Thin 1:1 tool mapping.** Mirrors the `Statbotics` class methods so the MCP tool surface tracks the documented Python API. No opinionated curation to maintain.
- **FastMCP** keeps boilerplate low and gives stdio + HTTP/SSE transports out of the box.

## Key Decisions

- **Language/runtime:** Python, importing the `statbotics` package as a dependency.
- **Location:** New top-level `mcp/` directory with its own `pyproject.toml`. Independent of `api/` packaging.
- **Transports:** Both stdio (default) and HTTP/SSE (opt-in via CLI flag).
- **Tool surface:** Thin 1:1 mapping — one MCP tool per public method on `Statbotics`:
  - `get_team`, `get_teams`
  - `get_year`, `get_years`
  - `get_team_year`, `get_team_years`
  - `get_event`, `get_events`
  - `get_team_event`, `get_team_events`
  - `get_match`, `get_matches`
  - `get_team_match`, `get_team_matches`
- **SDK:** FastMCP.
- **Resources/prompts:** None for v1 — tools only.
- **Distribution:** Runnable from clone (`python -m statbotics_mcp`) AND published to PyPI as `statbotics-mcp` (`uvx statbotics-mcp`).
- **Supporting infra:** README with copy-paste client config snippets (Claude Desktop, VS Code, Cursor). No CI workflow or Dockerfile in v1.

## Open Questions

- Package/module name on disk: `statbotics_mcp` vs `statbotics-mcp` vs nested under `statbotics.mcp`. (Leaning `statbotics_mcp` as a sibling project.)
- Minimum Python version — `statbotics` declares `^3.8`; FastMCP typically requires ≥3.10. Likely set MCP server to `>=3.10`.
- HTTP/SSE bind address/port defaults and whether to require an explicit `--http` flag.
- How to surface the upstream API base URL — fixed to `https://api.statbotics.io/v3`, or overridable via env var (e.g. `STATBOTICS_API_URL`) for local backend testing?
- Tool docstrings: auto-generate from `Statbotics` method docstrings, or hand-author for LLM clarity?

## Next Steps

→ Switch out of plan mode (or run a planning pass) to produce an implementation plan covering directory layout, `pyproject.toml`, tool definitions, transport wiring, README config snippets, and PyPI publish steps.
