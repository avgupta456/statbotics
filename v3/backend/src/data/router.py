from fastapi import APIRouter

from src.constants import CURR_YEAR
from src.data.main import reset_all_years, reset_curr_year, update_curr_year

router = APIRouter()


@router.get("/")
async def read_root():
    return {"name": "Data Router"}


@router.get("/reset_all_years")
async def reset_all_years_endpoint():
    return {"status": "skipped"}
    reset_all_years(start_year=2002, end_year=CURR_YEAR)
    return {"status": "success"}


@router.get("/reset_curr_year")
async def reset_curr_year_endpoint():
    reset_curr_year(curr_year=CURR_YEAR)
    return {"status": "success"}


@router.get("/update_year/{year}")
async def update_year_endpoint(year: int):
    update_curr_year(curr_year=year)
    return {"status": "success"}


@router.get("/update_curr_year")
async def update_curr_year_endpoint():
    update_curr_year(curr_year=CURR_YEAR)
    return {"status": "success"}


@router.get("/reset_curr_year_mock")
async def reset_curr_year_mock_endpoint():
    reset_curr_year(curr_year=CURR_YEAR, mock=True)
    return {"status": "success"}


@router.get("/update_curr_year_mock/{index}")
async def update_curr_year_mock_endpoint(index: int = 0):
    update_curr_year(curr_year=CURR_YEAR, mock=True, mock_index=index)
    return {"status": "success"}
