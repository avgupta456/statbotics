"""Singleton Statbotics HTTP client used by all MCP tools.

The MCP server always targets the public API at ``https://api.statbotics.io/v3``.
The base URL can be overridden by setting the ``STATBOTICS_API_URL`` environment
variable, which is useful for pointing at a locally-running backend.
"""

from __future__ import annotations

import os
import threading
from typing import Optional

from statbotics import Statbotics

_client: Optional[Statbotics] = None
_client_lock = threading.Lock()


def get_client() -> Statbotics:
    """Return a process-wide :class:`Statbotics` instance.

    The instance is created lazily on first call. If ``STATBOTICS_API_URL`` is
    set in the environment, it overrides the wrapper's hardcoded base URL.
    Initialization is guarded by a lock so HTTP-transport mode (which serves
    concurrent requests) cannot race and create multiple instances.
    """

    global _client
    if _client is None:
        with _client_lock:
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
    with _client_lock:
        _client = None
