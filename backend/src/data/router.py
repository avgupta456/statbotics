import requests
from fastapi import APIRouter, BackgroundTasks

from src.constants import BACKEND_URL, CURR_YEAR
from src.data.main import reset_all_years, update_curr_year
from src.data.tba import check_year_partial as check_year_partial_tba
from src.db.read import get_etags as get_etags_db, get_events as get_events_db

data_router = APIRouter()
site_router = APIRouter()


@data_router.get("/")
async def read_root():
    return {"name": "Data Router"}


@data_router.get("/reset_all_years")
async def reset_all_years_endpoint():
    # return {"status": "skipped"}
    reset_all_years()
    return {"status": "success"}


@data_router.get("/reset_curr_year")
async def reset_curr_year_endpoint():
    update_curr_year(partial=False)
    return {"status": "success"}


@data_router.get("/update_curr_year")
async def update_curr_year_endpoint():
    update_curr_year(partial=True)
    return {"status": "success"}


def update_curr_year_background():
    requests.get(f"{BACKEND_URL}/v3/data/update_curr_year")


@site_router.get("/update_curr_year")
async def update_curr_year_site_endpoint(background_tasks: BackgroundTasks):
    event_objs = get_events_db(year=CURR_YEAR)
    etags = get_etags_db(CURR_YEAR)
    is_new_data = check_year_partial_tba(CURR_YEAR, event_objs, etags)
    if not is_new_data:
        return {"status": "skipped"}

    background_tasks.add_task(update_curr_year_background)
    return {"status": "backgrounded"}
