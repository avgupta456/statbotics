"""FastMCP server exposing the public Statbotics API as MCP tools.

Each tool is a thin wrapper around a method on the :class:`statbotics.Statbotics`
client. Signatures, defaults, and tool descriptions mirror the underlying
methods so the LLM-facing tool descriptions stay in sync with the published
Python API.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Union

from fastmcp import FastMCP
from statbotics import Statbotics

from .client import get_client

mcp = FastMCP("statbotics")


def _doc(method_name: str) -> str:
    """Return the docstring of a Statbotics method for use as a tool description."""

    return getattr(Statbotics, method_name).__doc__ or ""


# ---------------------------------------------------------------------------
# Teams
# ---------------------------------------------------------------------------

@mcp.tool(description=_doc("get_team"))
def get_team(team: int, fields: List[str] = ["all"]) -> Dict[str, Any]:
    return get_client().get_team(team=team, fields=fields)


@mcp.tool(description=_doc("get_teams"))
def get_teams(
    country: Optional[str] = None,
    state: Optional[str] = None,
    district: Optional[str] = None,
    active: Optional[bool] = True,
    metric: str = "team",
    ascending: Optional[bool] = None,
    limit: int = 100,
    offset: int = 0,
    fields: List[str] = ["all"],
) -> List[Dict[str, Any]]:
    return get_client().get_teams(
        country=country,
        state=state,
        district=district,
        active=active,
        metric=metric,
        ascending=ascending,
        limit=limit,
        offset=offset,
        fields=fields,
    )


# ---------------------------------------------------------------------------
# Years
# ---------------------------------------------------------------------------

@mcp.tool(description=_doc("get_year"))
def get_year(year: int, fields: List[str] = ["all"]) -> Dict[str, Any]:
    return get_client().get_year(year=year, fields=fields)


@mcp.tool(description=_doc("get_years"))
def get_years(
    metric: str = "year",
    ascending: Optional[bool] = None,
    limit: int = 100,
    offset: int = 0,
    fields: List[str] = ["all"],
) -> List[Dict[str, Any]]:
    return get_client().get_years(
        metric=metric,
        ascending=ascending,
        limit=limit,
        offset=offset,
        fields=fields,
    )


# ---------------------------------------------------------------------------
# Team-Years
# ---------------------------------------------------------------------------

@mcp.tool(description=_doc("get_team_year"))
def get_team_year(
    team: int, year: int, fields: List[str] = ["all"]
) -> Dict[str, Any]:
    return get_client().get_team_year(team=team, year=year, fields=fields)


@mcp.tool(description=_doc("get_team_years"))
def get_team_years(
    team: Optional[int] = None,
    year: Optional[int] = None,
    country: Optional[str] = None,
    state: Optional[str] = None,
    district: Optional[str] = None,
    metric: str = "team",
    ascending: Optional[bool] = None,
    limit: int = 100,
    offset: int = 0,
    fields: List[str] = ["all"],
) -> List[Dict[str, Any]]:
    return get_client().get_team_years(
        team=team,
        year=year,
        country=country,
        state=state,
        district=district,
        metric=metric,
        ascending=ascending,
        limit=limit,
        offset=offset,
        fields=fields,
    )


# ---------------------------------------------------------------------------
# Events
# ---------------------------------------------------------------------------

@mcp.tool(description=_doc("get_event"))
def get_event(event: str, fields: List[str] = ["all"]) -> Dict[str, Any]:
    return get_client().get_event(event=event, fields=fields)


@mcp.tool(description=_doc("get_events"))
def get_events(
    year: Optional[int] = None,
    country: Optional[str] = None,
    state: Optional[str] = None,
    district: Optional[str] = None,
    type: Optional[Union[int, str]] = None,
    week: Optional[int] = None,
    metric: str = "year",
    ascending: Optional[bool] = None,
    limit: int = 100,
    offset: int = 0,
    fields: List[str] = ["all"],
) -> List[Dict[str, Any]]:
    return get_client().get_events(
        year=year,
        country=country,
        state=state,
        district=district,
        type=type,
        week=week,
        metric=metric,
        ascending=ascending,
        limit=limit,
        offset=offset,
        fields=fields,
    )


# ---------------------------------------------------------------------------
# Team-Events
# ---------------------------------------------------------------------------

@mcp.tool(description=_doc("get_team_event"))
def get_team_event(
    team: int, event: str, fields: List[str] = ["all"]
) -> Dict[str, Any]:
    return get_client().get_team_event(team=team, event=event, fields=fields)


@mcp.tool(description=_doc("get_team_events"))
def get_team_events(
    team: Optional[int] = None,
    year: Optional[int] = None,
    event: Optional[str] = None,
    country: Optional[str] = None,
    state: Optional[str] = None,
    district: Optional[str] = None,
    type: Optional[Union[int, str]] = None,
    week: Optional[int] = None,
    metric: str = "year",
    ascending: Optional[bool] = None,
    limit: int = 100,
    offset: int = 0,
    fields: List[str] = ["all"],
) -> List[Dict[str, Any]]:
    return get_client().get_team_events(
        team=team,
        year=year,
        event=event,
        country=country,
        state=state,
        district=district,
        type=type,
        week=week,
        metric=metric,
        ascending=ascending,
        limit=limit,
        offset=offset,
        fields=fields,
    )


# ---------------------------------------------------------------------------
# Matches
# ---------------------------------------------------------------------------

@mcp.tool(description=_doc("get_match"))
def get_match(match: str, fields: List[str] = ["all"]) -> Dict[str, Any]:
    return get_client().get_match(match=match, fields=fields)


@mcp.tool(description=_doc("get_matches"))
def get_matches(
    team: Optional[int] = None,
    year: Optional[int] = None,
    event: Optional[str] = None,
    week: Optional[int] = None,
    elims: Optional[bool] = None,
    metric: str = "time",
    ascending: Optional[bool] = None,
    limit: int = 200,
    offset: int = 0,
    fields: List[str] = ["all"],
) -> List[Dict[str, Any]]:
    return get_client().get_matches(
        team=team,
        year=year,
        event=event,
        week=week,
        elims=elims,
        metric=metric,
        ascending=ascending,
        limit=limit,
        offset=offset,
        fields=fields,
    )


# ---------------------------------------------------------------------------
# Team-Matches
# ---------------------------------------------------------------------------

@mcp.tool(description=_doc("get_team_match"))
def get_team_match(
    team: int, match: str, fields: List[str] = ["all"]
) -> Dict[str, Any]:
    return get_client().get_team_match(team=team, match=match, fields=fields)


@mcp.tool(description=_doc("get_team_matches"))
def get_team_matches(
    team: Optional[int] = None,
    year: Optional[int] = None,
    event: Optional[str] = None,
    match: Optional[str] = None,
    week: Optional[int] = None,
    elims: Optional[bool] = None,
    metric: str = "time",
    ascending: Optional[bool] = None,
    limit: int = 100,
    offset: int = 0,
    fields: List[str] = ["all"],
) -> List[Dict[str, Any]]:
    return get_client().get_team_matches(
        team=team,
        year=year,
        event=event,
        match=match,
        week=week,
        elims=elims,
        metric=metric,
        ascending=ascending,
        limit=limit,
        offset=offset,
        fields=fields,
    )


__all__ = ["mcp"]
