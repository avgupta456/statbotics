import os
import random

from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()

os.environ["LOCAL_DB"] = "False"

# Set random seed, for random team matches
random.seed(5511)

app = FastAPI()

from src.process.process_main import process_main  # noqa: E402


@app.get("/")
def hello_world():
    return {"message": "Hello World!"}


@app.get("/data_refresh")
def data_refresh():
    process_main(start_year=2022, end_year=2022, clean=False, fake_matches=False)
    return {"message": "Data refreshed!"}
