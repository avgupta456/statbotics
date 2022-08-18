from fastapi import APIRouter

from src.data.main import (
    reset_all_years,
    reset_curr_year,
    update_curr_year,
)

router = APIRouter()


@router.get("/")
async def read_root():
    return {"name": "Data Router"}


@router.get("/reset_all_years")
async def reset_all_years_endpoint():
    reset_all_years(start_year=2002, end_year=2022)
    return {"status": "success"}


@router.get("/reset_curr_year")
async def reset_curr_year_endpoint():
    reset_curr_year(curr_year=2022)
    return {"status": "success"}


@router.get("/update_curr_year")
async def update_curr_year_endpoint():
    update_curr_year(curr_year=2022)
    return {"status": "success"}
