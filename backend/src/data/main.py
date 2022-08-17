from fastapi import APIRouter

from src.data.insert.main import reset_all_years, reset_current_year

router = APIRouter()


@router.get("/")
async def read_root():
    return {"name": "Data Router"}


@router.get("/reset_all_years")
async def reset_all_years_endpoint():
    reset_all_years(start_year=2002, end_year=2022)
    return {"status": "success"}


@router.get("/reset_current_year")
async def reset_current_year_endpoint():
    reset_current_year(curr_year=2022)
    return {"status": "success"}
