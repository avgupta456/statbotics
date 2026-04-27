# statbotics-mcp

An [MCP](https://modelcontextprotocol.io) (Model Context Protocol) server for
the public [Statbotics](https://statbotics.io) API. It exposes the same surface
as the [`statbotics`](https://pypi.org/project/statbotics/) Python package —
team, year, event, and match EPA data for FIRST Robotics Competition (FRC) — as
MCP tools that any MCP-aware LLM client can call.

The server always targets the public production API at
`https://api.statbotics.io/v3`. It is published as a convenience for users of
this repo and for end users who want a ready-made MCP integration.

## Install

### From PyPI (recommended for end users)

```bash
uvx statbotics-mcp           # one-off run, no install
# or
pipx install statbotics-mcp
```

### From a clone (for repo contributors)

```bash
cd mcp
pip install -e .
python -m statbotics_mcp
```

Requires Python **3.11+**.

### Docker (no Python toolchain required)

If `statbotics-mcp` is not on PyPI yet — or you'd rather not install Python at
all — build the image from the cloned repo:

```bash
cd mcp
docker build -t statbotics-mcp .
```

Then run it over stdio:

```bash
docker run -i --rm statbotics-mcp
```

Or in HTTP mode:

```bash
docker run --rm -p 8000:8000 statbotics-mcp --http --host 0.0.0.0 --port 8000
```

## Run

### stdio (default — used by Claude Desktop, VS Code, Cursor, etc.)

```bash
statbotics-mcp
# or
python -m statbotics_mcp
```

### Streamable-HTTP (for remote/hosted use)

```bash
statbotics-mcp --http --host 127.0.0.1 --port 8000
```

## Client configuration

All snippets below configure the server over **stdio** — the right choice
when the MCP client and server live on the same machine. Use HTTP only when
you genuinely need a remote/hosted deployment (see [Run](#run)).

### Claude Desktop

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "statbotics": {
      "command": "uvx",
      "args": ["statbotics-mcp"]
    }
  }
}
```

### VS Code

Add to `.vscode/mcp.json` (or your user-level MCP config):

```json
{
  "servers": {
    "statbotics": {
      "command": "uvx",
      "args": ["statbotics-mcp"]
    }
  }
}
```

### Cursor

Add to `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "statbotics": {
      "command": "uvx",
      "args": ["statbotics-mcp"]
    }
  }
}
```

### GitHub Copilot CLI

Either run `/mcp add` inside an interactive `copilot` session and fill in the
fields, or edit `~/.copilot/mcp-config.json` directly (override the location
with the `COPILOT_HOME` environment variable):

```json
{
  "mcpServers": {
    "statbotics": {
      "type": "local",
      "command": "uvx",
      "args": ["statbotics-mcp"],
      "tools": ["*"]
    }
  }
}
```

After saving, run `/mcp` inside Copilot CLI to confirm the `statbotics` server
is listed and its tools are enabled.

If you installed from a clone instead of PyPI, swap `command` / `args` for
something like:

```json
{
  "command": "python",
  "args": ["-m", "statbotics_mcp"]
}
```

### Using the Docker image

If you built the Docker image (see [Docker](#docker-no-python-toolchain-required)
above), every client config above works by swapping `command` / `args` for:

```json
{
  "command": "docker",
  "args": ["run", "-i", "--rm", "statbotics-mcp"]
}
```

The `-i` flag is required so the container keeps stdin open for the MCP
stdio transport. To point at a non-default backend, append
`-e STATBOTICS_API_URL=...` before the image name.

## Tools

The server exposes a 1:1 mapping of the methods on the
[`Statbotics`](../api/statbotics/main.py) Python client:

| Tool | Description |
| ---- | ----------- |
| `get_team` | Retrieve a single team's metadata and EPA stats. |
| `get_teams` | List teams, filterable by country/state/district/active, sortable by metric. |
| `get_year` | Retrieve aggregate stats for a specific season. |
| `get_years` | List per-year aggregates, sortable by metric. |
| `get_team_year` | A team's stats in a specific year. |
| `get_team_years` | List (team, year) pairs with filtering and sorting. |
| `get_event` | Retrieve a single event by key (e.g. `2019cur`). |
| `get_events` | List events, filterable by year/location/type/week. |
| `get_team_event` | A team's stats at a specific event. |
| `get_team_events` | List (team, event) pairs with filtering and sorting. |
| `get_match` | Retrieve a single match by key (e.g. `2019cur_qm1`). |
| `get_matches` | List matches, filterable by team/year/event/week/elims. |
| `get_team_match` | A team's stats in a specific match. |
| `get_team_matches` | List (team, match) pairs with filtering and sorting. |

All tools accept a `fields` parameter (defaults to `["all"]`) that selects
which response fields to return, and plural tools accept `limit`, `offset`,
`metric`, and `ascending` for paging and sorting.

## Configuration

| Environment variable | Purpose |
| -------------------- | ------- |
| `STATBOTICS_API_URL` | Override the API base URL (default `https://api.statbotics.io/v3`). Useful for pointing at a locally-running backend. |

## Development

```bash
cd mcp
pip install -e .[dev]   # or: poetry install
pytest
```

## License

MIT — same as the parent repository.
