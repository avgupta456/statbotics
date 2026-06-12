import platform
from typing import Any, Callable

from dotenv import load_dotenv  # type: ignore

from fastapi import APIRouter, Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pyinstrument import Profiler

load_dotenv()

# flake8: noqa E402
from src.api.router import router as api_router
from src.auth import generate_api_key, get_api_key
from src.constants import CONN_STR, PROD
from src.data.router import (
    data_router as data_data_router,
    site_router as data_site_router,
)
from src.site.router import router as site_router

"""
SETUP
"""

app = FastAPI(
    title="Statbotics REST API",
    description="The REST API for Statbotics. Please be nice to our servers! If you are looking to do large-scale data science projects, use the CSV exports on the GitHub repo.",
    version="3.0.0",
    dependencies=[Depends(get_api_key)],
    swagger_ui_parameters={"persistAuthorization": True},
)

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


@router.get("/generate_key/{counter}")
def get_generate_key(counter: int, request: Request):
    origin = request.headers.get("origin", "")
    if origin not in origins:
        raise HTTPException(status_code=403, detail="Forbidden")
    return {"key": generate_api_key(counter)}


app.include_router(router, include_in_schema=False)
app.include_router(api_router, prefix="/v3")
app.include_router(data_data_router, prefix="/v3/data", include_in_schema=False)
app.include_router(data_site_router, prefix="/v3/site", include_in_schema=False)
app.include_router(site_router, prefix="/v3/site", include_in_schema=False)
