from dotenv import load_dotenv  # type: ignore
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

# flake8: noqa E402
from src.constants import CONN_STR, PROD
from src.data.router import router as data_router
from src.site.router import router as site_router

"""
SETUP
"""

app = FastAPI()

origins = [
    "http://localhost:3000",
    "https://statbotics.io",
    "https://www.statbotics.io",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
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
app.include_router(site_router, prefix="/site", include_in_schema=False)
app.include_router(data_router, prefix="/data", include_in_schema=False)
