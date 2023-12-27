from typing import Any, Callable

from dotenv import load_dotenv  # type: ignore
from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pyinstrument import Profiler

load_dotenv()

# flake8: noqa E402
from src.api.router import router as api_router
from src.constants import CONN_STR, PROD
from src.data.router import router as data_router
from src.site.router import router as site_router

"""
SETUP
"""

app = FastAPI(
    title="Statbotics REST API",
    description="The REST API for Statbotics. Please be nice to our servers! If you are looking to do large-scale data science projects, use the CSV exports on the GitHub repo.",
    version="1.0.0",
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
    return {"PROD": PROD, "CONN_STR": "REDACTED" if PROD else CONN_STR}


app.include_router(router, prefix="/v3", include_in_schema=False)
app.include_router(api_router, prefix="/v3")
app.include_router(data_router, prefix="/v3/data", include_in_schema=False)
app.include_router(site_router, prefix="/v3/site", include_in_schema=False)
