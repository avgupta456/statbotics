"""Singleton Statbotics HTTP client used by all MCP tools.

The MCP server always targets the public API at ``https://api.statbotics.io/v3``.
The base URL can be overridden by setting the ``STATBOTICS_API_URL`` environment
variable, which is useful for pointing at a locally-running backend.
"""

from __future__ import annotations

import os
from typing import Optional

from statbotics import Statbotics

_client: Optional[Statbotics] = None


def get_client() -> Statbotics:
    """Return a process-wide :class:`Statbotics` instance.

    The instance is created lazily on first call. If ``STATBOTICS_API_URL`` is
    set in the environment, it overrides the wrapper's hardcoded base URL.
    """

    global _client
    if _client is None:
        client = Statbotics()
        override = os.environ.get("STATBOTICS_API_URL")
        if override:
            client.BASE_URL = override.rstrip("/")
        _client = client
    return _client


def reset_client() -> None:
    """Reset the cached client. Intended for tests."""

    global _client
    _client = None
