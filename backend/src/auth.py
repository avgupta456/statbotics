import hashlib
import os
import time
from collections import defaultdict
from typing import Optional

from fastapi import HTTPException, Request, Security
from fastapi.security.api_key import APIKeyHeader

from src.constants import AUTH_KEY_BLACKLIST

# Secret used to generate and validate API keys. Set via environment variable.
API_SECRET = os.getenv("API_SECRET", "dev-secret")

# Rate limiting: max requests per key per minute
RATE_LIMIT = int(os.getenv("API_RATE_LIMIT", "100"))

# In-memory rate limit tracking: key -> list of request timestamps
_rate_limits: dict[str, list[float]] = defaultdict(list)

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def generate_api_key(counter: int) -> str:
    """Generate a UUID-format API key from a counter value.

    Format: first 8 hex chars = zero-padded counter,
    remaining 24 hex chars = truncated SHA-256(secret + counter).
    Formatted with dashes as a UUID.
    """
    counter_hex = f"{counter:08x}"
    hash_hex = hashlib.sha256(f"{API_SECRET}{counter}".encode()).hexdigest()[:24]
    raw = counter_hex + hash_hex
    # Format as UUID: 8-4-4-4-12
    return f"{raw[0:8]}-{raw[8:12]}-{raw[12:16]}-{raw[16:20]}-{raw[20:32]}"


def validate_api_key(key: str) -> bool:
    """Validate that a UUID-format API key was generated with our secret."""
    stripped = key.replace("-", "")
    if len(stripped) != 32:
        return False

    counter_hex = stripped[:8]
    provided_hash = stripped[8:]

    try:
        counter = int(counter_hex, 16)
    except ValueError:
        return False

    expected_hash = hashlib.sha256(f"{API_SECRET}{counter}".encode()).hexdigest()[:24]
    return provided_hash == expected_hash


def _check_rate_limit(key: str) -> None:
    """Enforce per-key rate limiting using in-memory sliding window."""
    now = time.time()
    window_start = now - 60

    # Prune old entries
    _rate_limits[key] = [t for t in _rate_limits[key] if t > window_start]

    if len(_rate_limits[key]) >= RATE_LIMIT:
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Max 100 requests per minute.")

    _rate_limits[key].append(now)


async def get_api_key(
    request: Request,
    api_key: Optional[str] = Security(api_key_header),
) -> str:
    """FastAPI dependency that validates the API key and enforces rate limits."""
    # Skip auth for non-API routes (site, data, docs, root)
    path = request.url.path
    if not path.startswith("/v3/") or path.startswith("/v3/site") or path.startswith("/v3/data"):
        return ""

    if not api_key:
        raise HTTPException(status_code=401, detail="Missing API key. Pass it via the X-API-Key header.")

    if not validate_api_key(api_key):
        raise HTTPException(status_code=403, detail="Invalid API key.")

    counter_hex = api_key.replace("-", "")[:8]
    if counter_hex in AUTH_KEY_BLACKLIST:
        raise HTTPException(status_code=403, detail="API key has been revoked.")

    _check_rate_limit(api_key)

    return api_key
