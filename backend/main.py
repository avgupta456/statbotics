import platform
from typing import Any, Callable

from dotenv import load_dotenv  # type: ignore

# from fastapi import APIRouter, Depends, FastAPI, Request, Security
# from fastapi.exceptions import HTTPException
from fastapi import APIRouter, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.security.api_key import APIKeyHeader
from pyinstrument import Profiler

load_dotenv()

# flake8: noqa E402
from src.api.router import router as api_router

# from src.constants import AUTH_KEY_BLACKLIST, CONN_STR, PROD
from src.constants import CONN_STR, PROD
from src.data.router import (
    data_router as data_data_router,
    site_router as data_site_router,
)
from src.site.router import router as site_router

# from src.utils.utils import is_uuid

"""
SETUP
"""

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


app = FastAPI(
    title="Statbotics REST API",
    description="The REST API for Statbotics. Please be nice to our servers! If you are looking to do large-scale data science projects, use the CSV exports on the GitHub repo.",
    version="3.0.0",
    # dependencies=[Security(get_api_key)],
    swagger_ui_parameters={"persistAuthorization": True},
)

# Removed CORS to enable website integrationss
origins = [
    "http://localhost:3000",
    "https://statbotics.io",
    "https://www.statbotics.io",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if not PROD:

    @app.middleware("http")
    async def profile_request(request: Request, call_next: Callable[[Any], Any]):
        profiling = request.query_params.get("profile", False)
        if profiling:
            profiler = Profiler(interval=0.001, async_mode="enabled")
            profiler.start()
            await call_next(request)
            profiler.stop()
            return HTMLResponse(profiler.output_html())
        else:
            return await call_next(request)


router = APIRouter()


@router.get("/")
async def read_root():
    return {"Hello": "World"}


@router.get("/info")
def get_info():
    return {
        "PROD": PROD,
        "CONN_STR": "REDACTED" if PROD else CONN_STR,
        "PYTHON_VERSION": platform.python_version(),
    }


app.include_router(router, include_in_schema=False)
app.include_router(api_router, prefix="/v3")
app.include_router(data_data_router, prefix="/v3/data", include_in_schema=False)
app.include_router(data_site_router, prefix="/v3/site", include_in_schema=False)
app.include_router(site_router, prefix="/v3/site", include_in_schema=False)
