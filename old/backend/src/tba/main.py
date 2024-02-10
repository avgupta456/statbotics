import os
from typing import Any, Optional, Tuple, Union

from requests import Session

from src.tba.constants import AUTH_KEY
from src.tba.utils import dump_cache, load_cache

read_prefix = "https://www.thebluealliance.com/api/v3/"

session = Session()
session.headers.update({"X-TBA-Auth-Key": AUTH_KEY, "X-TBA-Auth-Id": ""})


def _get_tba(
    url: str, etag: Optional[str] = None
) -> Tuple[Union[Any, bool], Optional[str]]:
    if etag is not None:
        session.headers.update({"If-None-Match": etag})
        response = session.get(read_prefix + url)
        if response.status_code == 304:
            return True, etag
        elif response.status_code == 200:
            return response.json(), response.headers.get("ETag")
    else:
        response = session.get(read_prefix + url)
        if response.status_code == 200:
            return response.json(), response.headers.get("ETag")
    return False, None


def get_tba(
    url: str, etag: Optional[str] = None, cache: bool = True
) -> Tuple[Union[Any, bool], Optional[str]]:
    if cache and os.path.exists("cache/" + url + "/data.p"):
        # Cache Hit
        return load_cache("cache/" + url), None

    data, new_etag = _get_tba(url, etag)

    # Either Etag or Invalid
    if type(data) is bool:
        return data, new_etag

    # Cache Miss
    dump_cache("cache/" + url, data)
    return data, new_etag
