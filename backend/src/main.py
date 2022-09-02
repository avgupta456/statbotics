from dotenv import load_dotenv  # type: ignore
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()


# flake8: noqa E402
from src.api.router import router as api_router
from src.constants import PROD
from src.data.router import router as data_router

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


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/info")
def get_info():
    return {"PROD": PROD}


app.include_router(api_router, prefix="/api")
app.include_router(data_router, prefix="/data")
