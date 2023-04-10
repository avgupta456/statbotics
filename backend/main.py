import sentry_sdk
from dotenv import load_dotenv  # type: ignore
from fastapi import APIRouter, FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

# flake8: noqa E402
from src.api.router import router as api_router
from src.constants import CONN_STR, PROD
from src.data.router import router as data_router
from src.site.router import router as site_router
from src.utils.decorators import async_fail_gracefully

"""
SETUP
"""

sentry_sdk.init(
    dsn="https://d13d19b3a7c54cc79ad19ff65640088c@o4504899523575808.ingest.sentry.io/4504899684270080",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production,
    traces_sample_rate=0.2 if PROD else 1.0,
)

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


router = APIRouter()


@router.get("/")
async def read_root():
    return {"Hello": "World"}


@router.get("/info")
def get_info():
    return {"PROD": PROD, "CONN_STR": "REDACTED" if PROD else CONN_STR}


@app.get("/sentry-debug")
@async_fail_gracefully
async def trigger_error(response: Response):
    return 1 / 0


app.include_router(router, prefix="", include_in_schema=False)
app.include_router(api_router, prefix="/v2")
app.include_router(data_router, prefix="/data", include_in_schema=False)
app.include_router(site_router, prefix="/site", include_in_schema=False)
