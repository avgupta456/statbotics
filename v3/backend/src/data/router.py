from fastapi import APIRouter

from src.constants import CURR_YEAR
from src.data.main import reset_all_years, update_single_year

router = APIRouter()


@router.get("/")
async def read_root():
    return {"name": "Data Router"}


@router.get("/reset_all_years")
async def reset_all_years_endpoint():
    # return {"status": "skipped"}
    reset_all_years(start_year=2002, end_year=CURR_YEAR)
    return {"status": "success"}


# TODO: change naming (update_single_year)


@router.get("/update_single_year")
async def update_single_year_endpoint():
    update_single_year(year=CURR_YEAR, partial=False)
    return {"status": "success"}


@router.get("/update_year/{year}")
async def update_year_endpoint(year: int):
    update_single_year(year=year, partial=True)
    return {"status": "success"}


@router.get("/update_curr_year")
async def update_curr_year_endpoint():
    update_single_year(year=CURR_YEAR, partial=True)
    return {"status": "success"}
