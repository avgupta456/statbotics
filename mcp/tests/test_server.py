"""Tests for the Statbotics MCP server."""

from __future__ import annotations

import asyncio
import os
from typing import Any, Dict, List

import pytest

from statbotics_mcp import client as client_module
from statbotics_mcp.server import mcp

EXPECTED_TOOLS = {
    "get_team",
    "get_teams",
    "get_year",
    "get_years",
    "get_team_year",
    "get_team_years",
    "get_event",
    "get_events",
    "get_team_event",
    "get_team_events",
    "get_match",
    "get_matches",
    "get_team_match",
    "get_team_matches",
}


@pytest.fixture(autouse=True)
def _reset_client():
    client_module.reset_client()
    yield
    client_module.reset_client()


def _list_tools():
    return asyncio.run(mcp.list_tools())


def test_all_tools_registered():
    names = {t.name for t in _list_tools()}
    assert EXPECTED_TOOLS.issubset(names), EXPECTED_TOOLS - names
    assert len(EXPECTED_TOOLS & names) == 14


def test_tool_descriptions_populated():
    for tool in _list_tools():
        if tool.name in EXPECTED_TOOLS:
            assert tool.description, f"{tool.name} missing description"
            assert "param" in tool.description.lower() or "return" in tool.description.lower()


def test_tool_input_schema_has_expected_params():
    by_name = {t.name: t for t in _list_tools()}
    teams = by_name["get_teams"]
    props = teams.parameters["properties"]
    for expected in ("country", "state", "district", "active", "metric", "limit", "offset", "fields"):
        assert expected in props, f"get_teams missing {expected}"


def _stub_client(monkeypatch, payload):
    class StubStatbotics:
        BASE_URL = "https://api.statbotics.io/v3"

        def get_team(self, team: int, fields: List[str]) -> Dict[str, Any]:
            return {"team": team, "fields": fields, "payload": payload}

        def get_teams(self, **kwargs):
            return [{"kwargs": kwargs, "payload": payload}]

    stub = StubStatbotics()
    monkeypatch.setattr(client_module, "_client", stub)
    return stub


def test_get_team_tool_delegates_to_client(monkeypatch):
    _stub_client(monkeypatch, "ok")
    from statbotics_mcp.server import get_team

    result = get_team(team=254)
    assert result == {"team": 254, "fields": ["all"], "payload": "ok"}


def test_get_teams_tool_passes_kwargs(monkeypatch):
    _stub_client(monkeypatch, "ok")
    from statbotics_mcp.server import get_teams

    result = get_teams(state="CA", limit=5)
    assert result[0]["kwargs"]["state"] == "CA"
    assert result[0]["kwargs"]["limit"] == 5


def test_env_var_overrides_base_url(monkeypatch):
    monkeypatch.setenv("STATBOTICS_API_URL", "http://localhost:9999/v3")
    client_module.reset_client()
    client = client_module.get_client()
    assert client.BASE_URL == "http://localhost:9999/v3"


def test_no_env_var_uses_default(monkeypatch):
    monkeypatch.delenv("STATBOTICS_API_URL", raising=False)
    client_module.reset_client()
    client = client_module.get_client()
    assert client.BASE_URL == "https://api.statbotics.io/v3"
