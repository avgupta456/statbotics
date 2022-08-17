import os

from typing import Any
from requests import Session

from src.tba.constants import AUTH_KEY
from src.tba.utils import dump_cache, load_cache

read_prefix = "https://www.thebluealliance.com/api/v3/"

session = Session()
session.headers.update({"X-TBA-Auth-Key": AUTH_KEY, "X-TBA-Auth-Id": ""})


def _get_tba(url: str):
    return session.get(read_prefix + url).json()


def get_tba(url: str, cache: bool = True) -> Any:
    if cache and os.path.exists("cache/" + url):
        # Cache Hit
        return load_cache("cache/" + url)

    # Cache Miss
    data = _get_tba(url)
    dump_cache("cache/" + url, data)
    return data
