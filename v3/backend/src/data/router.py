from fastapi import APIRouter

from src.data.main import reset_all_years, update_colors, update_curr_year

router = APIRouter()


@router.get("/")
async def read_root():
    return {"name": "Data Router"}


@router.get("/reset_all_years")
async def reset_all_years_endpoint():
    # return {"status": "skipped"}
    reset_all_years()
    return {"status": "success"}


@router.get("/reset_curr_year")
async def reset_curr_year_endpoint():
    update_curr_year(partial=False)
    return {"status": "success"}


@router.get("/update_curr_year")
async def update_curr_year_endpoint():
    update_curr_year(partial=True)
    return {"status": "success"}


@router.get("/update_colors")
async def update_colors_endpoint(use_cache: bool = True):
    update_colors(use_cache=use_cache)
    return {"status": "success"}
