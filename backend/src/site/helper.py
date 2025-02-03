import io
import json
import zlib
from typing import Any

from fastapi.responses import StreamingResponse


# TODO: implement load testing and find optimal compression that doesn't make
# the backend compute constrainted (ran into problems during 2024 season)
def compress(x: Any) -> StreamingResponse:
    return StreamingResponse(
        io.BytesIO(zlib.compress(json.dumps(x).encode(), level=1)),
        media_type="application/octet-stream",
    )
