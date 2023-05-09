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


app.include_router(router, prefix="", include_in_schema=False)
app.include_router(api_router, prefix="/v2")
app.include_router(data_router, prefix="/data", include_in_schema=False)
app.include_router(site_router, prefix="/site", include_in_schema=False)
