import io
import json
import zlib
from typing import Any

from fastapi.responses import StreamingResponse


def compress(x: Any) -> StreamingResponse:
    return StreamingResponse(
        io.BytesIO(zlib.compress(json.dumps(x).encode())),
        media_type="application/octet-stream",
    )
