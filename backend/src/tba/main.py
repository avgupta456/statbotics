import os
from typing import Any, Optional

from requests import Session

from src.tba.constants import AUTH_KEY
from src.tba.utils import dump_cache, load_cache

read_prefix = "https://www.thebluealliance.com/api/v3/"

session = Session()
session.headers.update({"X-TBA-Auth-Key": AUTH_KEY, "X-TBA-Auth-Id": ""})


def _get_tba(url: str, etag: Optional[str] = None) -> Any:
    if etag:
        session.headers.update({"If-None-Match": etag})
        response = session.get(read_prefix + url)
        if response.status_code == 304:
            return True
        elif response.status_code == 200:
            return response.json()
    else:
        response = session.get(read_prefix + url)
        if response.status_code == 200:
            return response.json()
    return False


def get_tba(url: str, etag: Optional[str] = None, cache: bool = True) -> Any:
    if cache and os.path.exists("cache/" + url):
        # Cache Hit
        return load_cache("cache/" + url)

    data = _get_tba(url, etag)

    # Either Etag or Invalid
    if type(data) == bool:
        return data

    # Cache Miss
    dump_cache("cache/" + url, data)
    return data
