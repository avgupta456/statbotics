from typing import Any, Callable

from dotenv import load_dotenv  # type: ignore
from fastapi import APIRouter, Depends, FastAPI, Request, Security
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.security.api_key import APIKeyHeader
from pyinstrument import Profiler

load_dotenv()

from src.api.router import router as api_router

# flake8: noqa E402
from src.api.v2.router import router as api_v2_router
from src.constants import AUTH_KEY_BLACKLIST, CONN_STR, PROD
from src.data.router import router as data_router
from src.site.router import router as site_router
from src.utils.utils import is_uuid

"""
SETUP
"""

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def get_api_key(request: Request, api_key_header: str = Depends(api_key_header)):
    url: str = request.url.__str__()
    if "localhost:8000" in url:
        return
    if "v3/api" not in url:
        return

    if api_key_header:
        if not is_uuid(api_key_header) or api_key_header in AUTH_KEY_BLACKLIST:
            raise HTTPException(
                status_code=401,
                detail="Invalid API key header. Generate a new API key at https://statbotics.io/api/generate_key",
            )
        return
    else:
        raise HTTPException(
            status_code=401,
            detail="API key not provided. If you are using the interactive docs, please click the 'Authorize' button in the top right corner. Otherwise, please add an 'X-API-Key' header with your API key. Generate a new API key at https://statbotics.io/api/generate_key.",
        )


app = FastAPI(
    title="Statbotics REST API",
    description="The REST API for Statbotics. Please be nice to our servers! If you are looking to do large-scale data science projects, use the CSV exports on the GitHub repo.",
    version="3.0.0",
    dependencies=[Security(get_api_key)],
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
    return {"PROD": PROD, "CONN_STR": "REDACTED" if PROD else CONN_STR}


app.include_router(router, prefix="/v3", include_in_schema=False)
app.include_router(api_router, prefix="/v3")
app.include_router(api_v2_router, prefix="/v2")
app.include_router(data_router, prefix="/v3/data", include_in_schema=False)
app.include_router(site_router, prefix="/v3/site", include_in_schema=False)
